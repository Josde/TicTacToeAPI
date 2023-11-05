# TicTacToe API

TicTacToe written in Django Rest Framework as a coding exercise. Includes unit tests and configurable board size.

# Endpoints
- /users/ - GET (user list, requires authentication) and POST (register user)
- /games/ - GET (game list) and POST (pass player_1 and player_2 ids to create a game)
- /games/<id> - GET (game data) and PUT (pass x and y, 0-indexed to place a piece)