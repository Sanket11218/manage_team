# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from manage_team.models import PlayerInfo, GameInfo, TeamInfo
from manage_team.serializers import PostSerializer, GameSerializer, \
    TeamSerializer


# Create your views here.

def index(request):
    return render(request, 'manage_team/index.html')


def player_registration(request):
    return render(request, 'manage_team/player_registration.html')


def create_game(request):
    return render(request, 'manage_team/create_game.html')


def create_team(request):
    return render(request, 'manage_team/create_team.html')


def team_decider(request):
    return render(request, 'manage_team/team_decider.html')


@csrf_exempt
@api_view(['GET', 'POST'])
def player_info(request):
    if request.method == 'GET':
        fields = ('alias',)
        player_data = PlayerInfo.objects.all()
        serializer = PostSerializer(player_data, many=True, fields=fields)
        return Response(serializer.data)

    if request.method == 'POST':
        fields = ('player_name', 'email_id', 'age', 'alias')
        post_data = PostSerializer(data=request.data, fields=fields)
        if post_data.is_valid():
            post_data.save()
            return Response(post_data.data, status=status.HTTP_201_CREATED)
        return Response(post_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def game_info(request):
    if request.method == 'GET':
        fields = ('game_name',)
        game_data = GameInfo.objects.all()
        serializer = GameSerializer(game_data, many=True, fields=fields)
        return Response(serializer.data)

    if request.method == 'POST':
        fields = (
            'game_name', 'max_teams', 'winning_points', 'game_description')
        post_data = GameSerializer(data=request.data, fields=fields)
        if post_data.is_valid():
            post_data.save()
            return Response(post_data.data, status=status.HTTP_201_CREATED)
        return Response(post_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def team_info(request):
    if request.method == 'GET':
        fields = ('team_name', 'team_points')
        team_data = TeamInfo.objects.all()
        serializer = TeamSerializer(team_data, many=True, fields=fields)
        return Response(serializer.data)

    if request.method == 'POST':
        fields = ('team_name', 'player_1', 'player_2', 'game_name')
        post_data = TeamSerializer(data=request.data, fields=fields)
        if post_data.is_valid():
            post_data.save()
            return Response(post_data.data, status=status.HTTP_201_CREATED)
        return Response(post_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def team_game_info(request):
    if request.method == 'GET':
        game_obj = GameInfo.objects.all()
        game_dict = {}
        for game in game_obj:
            team_list = []
            team_obj = TeamInfo.objects.filter(game_name=game)
            for team in team_obj:
                team_list.append(team.team_name)
            game_dict[game.game_name] = team_list
        return Response(game_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
def player_game_info(request):
    if request.method == 'GET':
        game_obj = GameInfo.objects.all()
        player_dict = {}
        for game in game_obj:
            player_list = []
            team_obj = TeamInfo.objects.filter(game_name=game)
            for team in team_obj:
                player_list.append(team.player_1.alias)
                player_list.append(team.player_2.alias)

            player_dict[game.game_name] = player_list
        return Response(player_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
def leaderboard(request):
    if request.method == 'GET':
        team_dict = {}
        team_obj = TeamInfo.objects.all().order_by('-team_points')
        for item in team_obj:
            if item.game_name_id not in team_dict:
                team_dict[item.game_name_id] = {item.team_name: item.team_points}
            else:
                team_dict[item.game_name_id].update(
                    {item.team_name: item.team_points})
        return Response(team_dict, status=status.HTTP_200_OK)


@api_view(['POST'])
def point_decider(request):
    if request.method == 'POST':
        allowed_fields = ['team1', 'team2', 'winning_team', 'game_name']
        for data in allowed_fields:
            if data not in request.data.keys():
                return Response('Missing Key',
                                status=status.HTTP_400_BAD_REQUEST)
        team_1 = request.data.get('team1')
        team_2 = request.data.get('team2')
        winning_team = request.data.get('winning_team')
        game_name = request.data.get('game_name')

        if team_1 == team_2:
            return Response('Team1 and Team2 cant be same',
                            status=status.HTTP_400_BAD_REQUEST)

        if (winning_team != team_1 and winning_team != team_2) or not \
                winning_team:
            return Response('Invalid Data', status=status.HTTP_400_BAD_REQUEST)

        if winning_team == team_1:
            loosing_team = team_2

        if winning_team == team_2:
            loosing_team = team_1

        team_1_obj = TeamInfo.objects.filter(pk=team_1).first()
        team_2_obj = TeamInfo.objects.filter(pk=team_2).first()
        winning_team_obj = TeamInfo.objects.filter(pk=winning_team).first()
        game_obj = GameInfo.objects.filter(pk=game_name).first()
        loosing_team_obj = TeamInfo.objects.filter(pk=loosing_team).first()

        if not team_1_obj:
            return Response('Invalid team1',
                            status=status.HTTP_400_BAD_REQUEST)

        if not team_2_obj:
            return Response('Invalid team2',
                            status=status.HTTP_400_BAD_REQUEST)

        if not winning_team:
            return Response('Invalid winning_team',
                            status=status.HTTP_400_BAD_REQUEST)

        if not game_obj:
            return Response('Invalid game_name',
                            status=status.HTTP_400_BAD_REQUEST)

        if not (str(team_1_obj.game_name) == str(team_2_obj.game_name) ==
                game_name):
            return Response('Invalid Data',
                            status=status.HTTP_400_BAD_REQUEST)

        fetch_point = game_obj.winning_points
        winning_team_obj.team_points = winning_team_obj.team_points + \
                                       fetch_point
        loosing_team_obj.team_points = loosing_team_obj.team_points - \
                                       fetch_point
        winning_team_obj.save()
        loosing_team_obj.save()

        response_data = {
            winning_team_obj.team_name: int(winning_team_obj.team_points),
            loosing_team_obj.team_name: int(loosing_team_obj.team_points)}

        return Response(response_data, status=status.HTTP_201_CREATED)
