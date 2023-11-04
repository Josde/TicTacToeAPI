from django.db import models
from utils import constants
# Create your models here.

class Game(models.Model):  
    game_id = models.AutoField(primary_key=True)
    player_1 = models.ForeignKey(models.User)
    player_2 = models.ForeignKey(models.User)
    # Podríamos separar esto en Game (la parte superior, datos sobre usuarios)
    # y GameState (la parte inferior, estado de la partida), para hacer cosas como guardar historiales completos jugada por jugada de cada partida. 
    # Sin embargo, lo dejo para el futuro.
    board = models.CharField(max_length=constants.BOARD_SIZE**2)
    turn = models.IntegerField()