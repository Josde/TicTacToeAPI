from django.contrib.auth.models import User
from .models import Game
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    
    def create(self, validated_data):
        email = validated_data.get("email")
        username = validated_data.get("username")
        password = validated_data.get("password")
        return User.objects.create(email=email, username=username, password=make_password(password))
         

class GameSerializer(serializers.ModelSerializer):
    player_1 = serializers.SlugField(required=True)
    player_2 = serializers.SlugField(required=True)
    board = serializers.CharField(read_only=True)
    turn = serializers.IntegerField(read_only=True)
    winner = serializers.IntegerField(read_only=True)
    class Meta:
        model = Game
        fields = ['game_id', 'player_1', 'player_2', 'board', 'turn', 'winner']

    def create(self, validated_data):
        player_1 = self.validate_user(validated_data.get("player_1"))
        player_2 = self.validate_user(validated_data.get("player_2"))
        return Game.objects.create(player_1=player_1, player_2=player_2)

    def validate_user(self, user_id):
        query = User.objects.all().filter(id=user_id)
        if not (query.exists()):
            raise ValidationError(f"User {user_id} does not exist, check ids and try again.")
        return query.get()