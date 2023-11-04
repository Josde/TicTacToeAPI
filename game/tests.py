from django.test import TestCase
from .utils import game, constants
# Create your tests here.
class BoardTestCase(TestCase):
    def horizontal_check_test(self):
        board = "." * constants.BOARD_SIZE**2
        self.assertFalse(game.check_horizontals(board, constants.PLAYER_1_PIECE))
        board[0] = constants.PLAYER_1_PIECE
        board[1] = constants.PLAYER_1_PIECE
        board[2] = constants.PLAYER_1_PIECE
        self.assertTrue(game.check_horizontals(board, constants.PLAYER_1_PIECE))
    
    def vertical_check_test(self):
        board = "." * constants.BOARD_SIZE**2
        self.assertFalse(game.check_verticals(board, constants.PLAYER_1_PIECE))
        board[0] = constants.PLAYER_1_PIECE
        board[3] = constants.PLAYER_1_PIECE
        board[6] = constants.PLAYER_1_PIECE
        self.assertTrue(game.check_verticals(board, constants.PLAYER_1_PIECE))
        
    def diagonal_check_test(self):
        board = "." * constants.BOARD_SIZE**2
        self.assertFalse(game.check_verticals(board, constants.PLAYER_1_PIECE))
        board[0] = constants.PLAYER_1_PIECE
        board[4] = constants.PLAYER_1_PIECE
        board[8] = constants.PLAYER_1_PIECE
        self.assertTrue(game.check_verticals(board, constants.PLAYER_1_PIECE))
        board[2] = constants.PLAYER_2_PIECE
        board[4] = constants.PLAYER_2_PIECE
        board[6] = constants.PLAYER_2_PIECE
        self.assertTrue(game.check_verticals(board, constants.PLAYER_2_PIECE))
    
    def can_place_test(self):
        board = "." * constants.BOARD_SIZE**2
        self.assertTrue(game.can_place(board, 1, 1))
        game.place(board, 1, 1, constants.PLAYER_1_PIECE)
        self.assertFalse(game.can_place(board, 1, 1))
    
    def place_test(self):
        board = "." * constants.BOARD_SIZE**2
        game.place(board, 0, 0, constants.PLAYER_1_PIECE)
        self.assertTrue(board[0] == constants.PLAYER_1_PIECE)
        game.place(board, constants.BOARD_SIZE - 1, constants.BOARD_SIZE - 1, constants.PLAYER_2_PIECE)
        self.assertTrue(board[constants.BOARD_SIZE**2 - 1] == constants.PLAYER_2_PIECE)