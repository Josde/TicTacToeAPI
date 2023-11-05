from django.contrib.auth.models import User
from django.http import Http404
from .models import Game
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, GameSerializer
from .utils import game, constants
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameList(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)  
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
class GameDetail(APIView):
    def get_game(self, id):
        try: 
            instance = Game.objects.get(game_id=id)
            return instance
        except Game.DoesNotExist:
            raise Http404
    
    def get(self, request, id):
        instance = self.get_game(id)
        serializer = GameSerializer(instance)
        return Response(serializer.data)
    
    def put(self, request, id):
        
        instance = self.get_game(id)
        player = request.user
        if (player is None or (player != instance.player_1 and player != instance.player_2) or instance.winner != 0):
            return Response(status=status.HTTP_403_FORBIDDEN)
        player_turn = 1 if player == instance.player_1 else 2
        x = request.data.get('x')
        y = request.data.get('y')
        if (game.can_place(instance.board, x, y)):
            piece = constants.PLAYER_1_PIECE if player_turn == 1  else constants.PLAYER_2_PIECE
            instance.board = game.place(instance.board, x, y, piece)
            winner = game.check_victory(instance.board, piece)
            if (winner != 0):
                instance.winner = winner
            instance.turn = 1 if instance.turn != 1 else 2
            instance.save()
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = GameSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    