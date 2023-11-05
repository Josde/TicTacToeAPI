from django.contrib.auth.models import User
from .models import Game
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['game_id', 'player_1', 'player_2', 'board', 'turn', 'winner']

    def create(self, validated_data):
        return Game.objects.create(**validated_data)
