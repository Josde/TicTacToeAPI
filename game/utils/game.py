import constants

def convert_to_array(board : str):
    if len(board < constants.BOARD_SIZE ** 2):
        raise Exception("Board string is too small")
    array = [ [] * 3 ]
    for i in range(0, constants.BOARD_SIZE ** 2):
        idx = i+1 // constants.BOARD_SIZE # El indice de la fila del array al que tenemos que añadir nuestro carácter.
        array[idx].append(board[i])
        
    return array

def can_place(board : str, x : int, y : int):
    conv_board = convert_to_array(board)
    return conv_board[y][x] == constants.BLANK
    
def check_victory(board : str, player_piece : str):
    """Comprueba si algún jugador ha ganado

    Args:
        board (str): El estado del juego representado como string.
        player_piece(str): La pieza del jugador ("X" o "O")

    Returns:
        bool : Si true, el jugador ha ganado. Si no, no.
    """    
    conv_board = convert_to_array(board)
    victory = check_horizontals(conv_board, player_piece) or check_verticals(conv_board, player_piece) or check_diagonals(conv_board, player_piece)
    return victory

def check_horizontals(board, player_piece : str):
    # Horizontales:
    # 0 1 2 ->
    # 3 4 5 ->
    # 6 7 8 ->
    return any(all(board[y][x] == player_piece for x in range(constants.BOARD_SIZE) for y in range(constants.BOARD_SIZE)))
def check_verticals(board, player_piece : str):
    # Verticales:
    # 0 1 2 
    # 3 4 5 
    # 6 7 8 
    # | | |
    # v v v
    # Lo mismo que check_horizontals pero cambiamos el orden de x e y para que vaya en vertical.
    return any(all(board[y][x] == player_piece for y in range(constants.BOARD_SIZE) for x in range(constants.BOARD_SIZE)))

def check_diagonals(board, player_piece : str):
    # Diagonales:
    # 0 1 2 
    # 3 4 5 
    # 6 7 8 
    #!     ! (i = i)
    #(i, board_size - i - 1)
    if (all(board[i][i] == player_piece for i in range(constants.BOARD_SIZE))):
        return True
    if (all(board[i][constants.BOARD_SIZE - i - 1] == player_piece for i in range(constants.BOARD_SIZE))): 
        return True