# Connect4-AI
Connect4 with an AI opponent that uses negamax search with alpha-beta pruning, and a Zobrist transposition table to avoid re-evaluating board states

Note: This program was made in a newer version of python: Python 3.14 and uses pygame-ce (Community Edition)

![image alt](https://github.com/AtrributeErrorer/Connect4-AI/blob/750ed0872573640263ead42f3f8fc3b3f7e3ef26/pygame%20window.jpg)

To change the settings, you can do so in config.ini:
[SETTINGS]
Player_1 = (VALUES: 1 or 2, DEFAULT: 1) 1 is a human player, 2 is an AI player
Player_2 = (VALUES: 1 or 2, DEFAULT: 2) 1 is a human player, 2 is an AI player
Rows = (VALUES: Any positive number, DEFAULT: 6) Rows of the board
Columns = (VALUES: Any positive number, DEFAULT: 7) Columns of the board
Depth = (VALUES: Any positive number, DEFAULT: 10) How deep the search should be, lower is faster but less intelligent, higher is smarter but more computationally expensive

##How it works:
If Player_1 in config.ini is set to a value of 1, then a human will make a move,
To make a move as a human, you simply click on the column you want to play in

If Player_2 in config.ini is set to a value of 2, then the AI will make a move,
The AI emulates future moves by using the **negamax algorithm** (a variation of the *Minimax algorithm*), 
it looks for *depth* moves ahead emulating opponent responses and AI responses, the *fastest* win gets the highest score possible
while slower wins get less score. The AI *prunes* bad plays it would never pick to reduce computation time using **Alpha-Beta pruning**.
Once the function finishes evaluating a board state, it saves information of the node to a **Zobrist transposition table** 
to avoid re-evaluating the same board states in the future, as its almost garunteed to happen.
Once the specified depth hits 0 and the AI can not search any further, it **heuristically evaluates** the board to determine if the position is 
considered good or bad for the current player, a positive score is better and a negative score is worse 
