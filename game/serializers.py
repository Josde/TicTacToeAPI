from django.contrib.auth.models import User
from .models import Game
from .utils import game, constants
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['game_id', 'player_1', 'player_2', 'board', 'turn', 'winner']
