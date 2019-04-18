from rest_framework import serializers
from .models import  PlayerInfo,GameInfo,TeamInfo
from django.db.models import Q

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class PostSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PlayerInfo
        fields = '__all__'

class GameSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = GameInfo
        fields = '__all__'

class TeamSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TeamInfo
        fields = '__all__'

    def create(self,validated_data):
        if validated_data.get('player_1') == validated_data.get('player_2'):
            raise serializers.ValidationError("Player 1 and Player 2 cannot be same")

        elif ((TeamInfo.objects.filter(
                (Q(player_1=validated_data.get('player_1')) | Q(player_1=validated_data.get('player_2'))) & Q(
                    game_name=validated_data.get('game_name')))) or (TeamInfo.objects.filter(
            (Q(player_2=validated_data.get('player_1')) | Q(player_2=validated_data.get('player_2'))) & Q(
                game_name=validated_data.get('game_name'))))):
            raise serializers.ValidationError("Player Already Registerd in the Same game")

        elif GameInfo.objects.filter(game_name=validated_data.get('game_name')).values_list(
                'max_teams', flat=True)[0] <= 0:
            raise serializers.ValidationError("No Slots Left")

        return TeamInfo.objects.create(**validated_data)



