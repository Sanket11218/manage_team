# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.



class PlayerInfo(models.Model):
    player_name = models.CharField(max_length=200)
    email_id = models.EmailField(max_length=70)
    age = models.PositiveIntegerField()
    alias = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.alias


class GameInfo(models.Model):
    game_name = models.CharField(max_length=100, primary_key=True)
    max_teams = models.PositiveIntegerField()
    game_description = models.CharField(max_length=200)
    winning_points = models.IntegerField(default=0)

    def __str__(self):
        return self.game_name


class TeamInfo(models.Model):
    team_name = models.CharField(max_length=50, primary_key=True)
    player_1 = models.ForeignKey(PlayerInfo, related_name='player1', null=True,
                                 on_delete=models.CASCADE)
    player_2 = models.ForeignKey(PlayerInfo, related_name='player2', null=True,
                                 on_delete=models.CASCADE)
    game_name = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    team_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        game_info_obj = GameInfo.objects.filter(game_name=self.game_name).first()
        game_info_obj.max_teams = game_info_obj.max_teams - 1
        game_info_obj.save()
        super(TeamInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.team_name



