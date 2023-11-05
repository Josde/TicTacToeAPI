from . import constants

def convert_to_array(board : str):
    """Convierte un string al menos longitud constants.BOARD_SIZE^2 (es decir, el tamaño de nuestro tablero) a array bidimensional

    Args:
        board (str): La representación en string del tablero

    Raises:
        Exception: Puede lanzar una excepción si se le pasa un objeto que no sea string o si este string es demasiado pequeño

    Returns:
        array: Lista bidimensional que representa nuestro array, ya en la forma de tablero cuadriculado que esperariamos. 
    """    
    if len(board) < constants.BOARD_SIZE ** 2 or not isinstance(board, str):
        raise Exception("Board string is too small or not a string.")
    array = [ [] for i in range(constants.BOARD_SIZE) ]
    for i in range(0, constants.BOARD_SIZE ** 2):
        idx = i // constants.BOARD_SIZE # El indice de la fila del array al que tenemos que añadir nuestro carácter.
        array[idx].append(board[i])
        
    return array

def convert_to_string(board) -> str:
    """Función inversa a convert_to_array

    Args:
        board (List[List[str]]): Array de array de strings, que representa el tablero en forma bidimensional.
    Returns:
        str: String que representa nuestro tablero de forma plana
    """       
    board_string = ""
    for i in range(0, constants.BOARD_SIZE):
        for j in range(0, constants.BOARD_SIZE):
            board_string += (board[i][j])
    return board_string

def can_place(board : str, x : int, y : int) -> bool:
    """Hace las comprobaciones necesarias para saber si se puede poner una ficha en determinado sitio del tablero.

    Args:
        board (str): Estado del tablero, como string
        x (int): Posición X (horizontal) del tablero, empezando por la izquierda y por el 0.
        y (int): Posición Y (vertical) del tablero, empezando por arriba y por el 0.

    Returns:
        bool: Verdadero si podemos poner ficha, falso si no.
    """    
    if (x > constants.BOARD_SIZE or x < 0 or y > constants.BOARD_SIZE or y < 0):
        return False
    conv_board = convert_to_array(board)
    return conv_board[y][x] == constants.BLANK

def place(board : str, x : int, y : int, player_piece : str) -> str:
    """Pone una ficha en el tablero.

    Args:
        board (str): Estado del tablero, como string.
        x (int): Posición X (horizontal) del tablero, empezando por la izquierda y por el 0.
        y (int): Posición Y (vertical) del tablero, empezando por arriba y por el 0.
        player_piece (str): El caracter que representa la ficha de nuestro jugador.

    Returns:
        str: El nuevo estado de nuestro tablero. Si no se puede poner ficha, simplemente es el estado original.
    """    
    conv_board = convert_to_array(board)
    if (can_place(board, x, y)):
        conv_board[y][x] = player_piece
    return convert_to_string(conv_board)
    
def check_victory(board : str, player_piece : str) -> bool:
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
    return any(all(board[y][x] == player_piece for x in range(constants.BOARD_SIZE)) for y in range(constants.BOARD_SIZE))
def check_verticals(board, player_piece : str):
    # Verticales:
    # 0 1 2 
    # 3 4 5 
    # 6 7 8 
    # | | |
    # v v v
    # Lo mismo que check_horizontals pero cambiamos el orden de x e y para que vaya en vertical.
    return any(all(board[y][x] == player_piece for y in range(constants.BOARD_SIZE)) for x in range(constants.BOARD_SIZE))

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
    return False