from django.db import models
from .utils import constants
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):  
    game_id = models.AutoField(primary_key=True)
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_1")
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_2")
    # Podríamos separar esto en Game (la parte superior, datos sobre usuarios)
    # y GameState (la parte inferior, estado de la partida), para hacer cosas como guardar historiales completos jugada por jugada de cada partida. 
    # Sin embargo, lo dejo para el futuro.
    board = models.CharField(max_length=constants.BOARD_SIZE**2, default="." * constants.BOARD_SIZE**2)
    turn = models.IntegerField(default=1) # 1 = player 1, 2 = player 2
    winner = models.IntegerField(default=0) # 0 = not finished, 1 = player 1, 2 = player 2