from abc import ABC, abstractmethod
import math
import connect4
import transpositionTable
import configparser

class Player(ABC): #Abstract Class
    def __init__(self, graphics):
        self.graphics = graphics
        
    @abstractmethod
    def get_move(self, game, transposition_table) -> list:
        return []

    @abstractmethod
    def is_ai(self) -> bool:
        return False

class Human(Player): 
    def __init__(self, graphics):
        super().__init__(graphics)
    def get_move(self, game: 'connect4.Connect4', transposition_table) -> list:
        #Returns clicked move
        clicked = []
        result = -1
        moved = False   
        while not moved:
            while clicked == []:
                clicked = self.graphics.clicked_move(game)
            result = game.make_play(clicked[0], game.board, game.player)
            if result == -1:
                clicked = []
                continue
            else:
                moved = True
        clicked.append(result)
        return clicked

    def is_ai(self) -> bool:
        return False

class Ai(Player):
    def __init__(self, square_size):
        self.square_size = square_size
        self.gui_offset = square_size/2
        self.prioritize_column = {}
        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.depth = config.getint('SETTINGS', "Depth")
    
    def initialize_column_order(self, game: 'connect4.Connect4'):
        #Orders the columns which are worth the most, for game.column = 7, the ordering is: 
        #column_order = [4, 3, 5, 2, 6, 1, 7] for game.column = 7
        column_order = []
        for x in range(0, game.cols):
            if(math.ceil(game.cols/2 + (1-2*(x%2))*(x+1)/2) != 0):
                column_order.append(math.ceil(game.cols/2 + (1-2*(x%2))*(x+1)/2))
                if(game.cols%2 == 0 and x == 0): column_order.append(int(game.cols/2))
        return column_order

    def heuristic_eval_of_board(self, game: 'connect4.Connect4', column_order):
        #Gives an evaluation for how good a games board is for the current player
        #board_eval: Positive is good for the current player, negative is final
        board_eval = 0
        board_eval_opponent = 0
        for x in range(0, len(column_order)):
            can_move_row = game.can_place(column_order[x], game.board)
            if(can_move_row == -1): continue
            board_eval += game.check_eval_at_pos(column_order[x], can_move_row, game.board, game.player) 
            game.switch_player()
            board_eval_opponent += game.check_eval_at_pos(column_order[x], can_move_row, game.board, game.player) 
            game.switch_player()
        for x in range(0, game.rows):
            for y in range(len(column_order)):
                if(game.board[x][y] == game.player):
                    board_eval += self.prioritize_column[y + 1]
                elif(game.board[x][y] != game.player and game.board[x][y] != 0):
                        board_eval_opponent += self.prioritize_column[y + 1]
        board_eval = board_eval - board_eval_opponent
        return board_eval

    def get_move(self, game: 'connect4.Connect4', transposition_table) -> list:
        #Gets the move from the AI 
        column_order = self.initialize_column_order(game)
        column_score = (game.rows * game.cols - game.moves)//8
        #The loop below assigns a point to each of the columns
        #The column_order holds the best columns to start with, so columns in the middle will be assigned higher points
        #This is done so we can heuristically evaluate board at the end of depth search
        for x in range(len(column_order)):
            if(x == 1 and game.cols%2 == 0): continue
            if(x == 0):
                self.prioritize_column[column_order[x]] = column_score # pyright: ignore[reportAttributeAccessIssue]
                if(game.cols%2 == 0 and x == 0): 
                    self.prioritize_column[column_order[x + 1]] = column_score
                column_score = column_score / 2
                continue
            elif (x % 2 == 0 and x > 0):
                self.prioritize_column[column_order[x]] = column_score
                column_score = column_score / 2
                continue
            else:
                self.prioritize_column[column_order[x]] = column_score
                continue
        self.count = 0
        score, best_col = self.negamax(game, -10000, 10000, column_order,transposition_table, self.depth)
        col_posx_moverow = [best_col, best_col*self.square_size - self.gui_offset]
        col_posx_moverow.append(game.make_play(col_posx_moverow[0], game.board, game.player))
        return col_posx_moverow

    def negamax(self, game: 'connect4.Connect4', alpha, beta, column_order, transposition_table: 'transpositionTable.TranspositionTable',depth) -> tuple[int, int]:
        #Recursively searches the tree with the given depth and returns the score and the best column to play in
        hash = transposition_table.computeHash(game.board) #Turns board into a hash 
        rscore, rflag, rbest_move, rdepth = transposition_table.retrieve(hash) #Calls storage for given board

        #If the board exists in the table, we pull its score and best moves
        if(rscore is not None and rflag is not None and rbest_move is not None and rdepth is not None and rdepth >= depth):
            if(rflag == "EXACT"):
                return rscore, rbest_move
            if(rflag == "LOWERBOUND"):
                alpha = max(alpha, rscore)
            if(rflag == "UPPERBOUND"):
                beta = min(beta, rscore)
            if(alpha >= beta): return rscore, rbest_move

        if(game.check_draw()): return 0,0 #If the game is a draw, we return a neutral score and there is not best column to play so we return 0
        if(depth == 0): #If the depth is 0, we use a heuristic evaluation of the board
            return self.heuristic_eval_of_board(game, column_order), 0
        
        #If the game is a winner, we return the max points possible
        #The more moves in, the less points you get, so earlier wins are rewarded more points
        for x in range(0, len(column_order)):
            can_move_row = game.can_place(column_order[x], game.board)
            if(can_move_row == -1): continue
            if(game.check_winner(column_order[x], can_move_row, game.board, game.player)):
                return ((game.rows * game.cols - game.moves) // 2), column_order[x]
            
        #We clamp beta to allow more pruning, since we can't score higher than beta
        max_score_possible = (game.rows * game.cols - game.moves) // 2
        if(beta > max_score_possible): 
            beta = max_score_possible
            if(alpha >= beta): return beta, -1 

        best_col = -1
        score = 0
        #Loop through all the columns, emulate the depth moves deep, and return the final score
        #Since the score will be coming from the opposite player, we negate the score
        #A score of 5 from our opponenent is a score of -5 for us.
        for x in range(0, len(column_order)):
            can_move_row = game.can_place(column_order[x], game.board)
            if(can_move_row == -1): continue
            game.make_play(column_order[x], game.board, game.player)
            game.switch_player()
            child_score, _ = self.negamax(game, -beta, -alpha, column_order, transposition_table,depth - 1)
            game.undo_move(column_order[x], game.board)
            game.switch_player()
            score = -child_score 
            if(score > alpha): #alpha is our best score, beta is the opponenets best score, if we surpass alpha, set our alpha to the score and set the best column 
                alpha = score
                best_col = column_order[x]
            if(alpha >= beta): return alpha, best_col #Prune the child tree if we already have a much better score, theres no point in searching if we would never make a move worse than what we already have
        #Stores the information of the node in the table below so we can retrieve it later
        if(rscore is None and rflag is None and rbest_move is None and rdepth is None): transposition_table.store(score, alpha, beta, best_col, hash, depth)
        return alpha, best_col
            
    def is_ai(self) -> bool:
        return True
