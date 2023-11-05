from django.contrib.auth.models import User
from django.http import Http404
from .models import Game
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer, GameSerializer
from .utils import game, constants
# Create your views here.


class UserList(APIView):
    def get(self, request : Request) -> Response:
        users = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    def post(self, request : Request) -> Response:
        """Registra a un usuario.

        Args:
            request (Request): Ha de contener los datos de username, email y contraseña.

        Returns:
            Response: Los datos del nuevo usuario o errores. 
        """        
        serializer = UserSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GameList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request: Request) -> Response:
        games = Game.objects.all().order_by('-game_id')
        serializer = GameSerializer(games, many=True)  
        return Response(serializer.data)
    
    def post(self, request: Request) -> Response:
        """Crea una nueva partida

        Args:
            request (Request): Ha de contener los IDs de player_1 y player_2.

        Returns:
            Response: Los datos de la nueva partida o errores.
        """        
        serializer = GameSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
class GameDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_game(self, id : int) -> Game:
        try: 
            instance = Game.objects.get(game_id=id)
            return instance
        except Game.DoesNotExist:
            raise Http404
    
    def get(self, request : Request, id : int) -> Response:
        instance = self.get_game(id)
        serializer = GameSerializer(instance)
        return Response(serializer.data)
    
    def put(self, request : Request, id : int) -> Response:
        """Pone una ficha en el tablero

        Args:
            request (Request): Ha de contener x e y, ambos de 0 a 2 y empezando por la izquierda y arriba.
            id (int): El ID de la partida en la que queremos poner ficha. 
                        Para que el metodo funcione, dicha partida ha de:
                            - No estar acabada
                            - Tenernos como jugador
                            - Y debemos tener el turno.

        Returns:
            Response: El nuevo estado del tablero, o errores.
        """        
        instance = self.get_game(id)
        player = request.user
        if (not isinstance(request.user, User) or (player != instance.player_1 and player != instance.player_2) or instance.winner != 0):
            return Response(status=status.HTTP_403_FORBIDDEN)
        player_turn = 1 if player == instance.player_1 else 2
        x = request.data.get('x')
        y = request.data.get('y')
        if not isinstance(x, int) or not isinstance(y, int):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if (player_turn == instance.turn and game.can_place(instance.board, x, y)):
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
        
    