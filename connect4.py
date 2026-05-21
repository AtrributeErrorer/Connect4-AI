import configparser

class Connect4:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.rows = config.getint('SETTINGS', "Rows")
        self.cols = config.getint('SETTINGS', "Columns")
        self.player = 1
        self.moves = 0
        self.last_move = 0
        self.winner = None
        self.board = [[0 for x in range(self.cols)] for x in range(self.rows)]
        self.previous_board = [[0 for x in range(self.cols)] for x in range(self.rows)]

    def print_board(self):
        #Prints the board
        for x in range(self.cols):
            print(f" {x+1} ", end="")
        print()
        for r in range(self.rows):
            for x in range(self.cols):
                if(self.board[r][x] == 0):
                    print(f"O  ", end="")
                else:
                    print(f"{self.board[r][x]}  ", end="")
            print(f"  {r+1}")
    
    def undo_move(self, col, board) -> None:
        #Undo's a move on a board
        for row in (range(self.rows)):
            if(board[row][col-1] != 0):
                board[row][col-1] = 0
                self.moves -= 1
                return
        return
    
    def switch_player(self):
        #Switches the member variable 'player' on the Connect4 Object
        if(self.player == 1):
            self.player = 2
        else:
            self.player = 1

    def place_move(self, move_col, board, player) -> int:
        #Places a move on the board 
        mark_move = player
        for row in reversed(range(self.rows)):
            if(board[row][move_col-1] == 0):
                board[row][move_col-1] = mark_move
                return row
        return -1
    
    def can_place(self, move_col, board) -> int:
        #Checks legal move on the specified column
        if(move_col > self.cols): return -1
        for row in reversed(range(self.rows)):
            if(board[row][move_col-1] == 0):
                return row
        return -1
    
    def make_play(self, move_col, board, player) -> int:
        #Places a move on the board
        self.last_move = move_col
        move_row = -1
        move_row = self.place_move(move_col, board, player)
        if(move_row == -1):
            print("That column is full")
            return -1
            
        self.moves += 1
        return move_row
    
    def check_winner(self, move_col, move_row, board, player) -> bool:
        #Checks if the player has already won the game

        current_piece = 1
        #check right
        count_r = self.check_points(0, 1, move_row, move_col, board, player)
        #check left
        count_l = self.check_points(0, -1, move_row, move_col, board, player)
        #check down
        count_d = self.check_points(1, 0, move_row, move_col, board, player)
        #check up right
        count_up_right = self.check_points(-1, 1, move_row, move_col, board, player)
        #check up left
        count_up_left = self.check_points(-1, -1, move_row, move_col, board, player)
        #check down right
        count_down_right = self.check_points(1, 1, move_row, move_col, board, player)
        #check down left
        count_down_left = self.check_points(1, -1, move_row, move_col, board, player)

        if(count_r + count_l + current_piece >= 4):
            return True
        elif (count_d + current_piece >= 4):
            return True
        elif (count_up_right + count_down_left + current_piece >= 4):
            return True
        elif (count_up_left + count_down_right + current_piece >= 4):
            return True
        return False
    
    def check_draw(self) -> bool:
        #Checks if no more legal moves are left
        count = 0
        for x in range(self.cols):
            if(self.board[0][x] != 0): count += 1
            else: return False
        if(count == self.cols): return True
        return False
    
    def check_points(self, dirR, dirC, move_row, move_col, board, player):
        #Directionally checks for pieces belonging to the player
        count = 0
        mark_move = player
        for x in range(1, 4):
            if(move_col - 1 + (x * dirC) >= self.cols): break
            if(move_col - 1 + (x * dirC) < 0): break
            if(move_row + (x * dirR) >= self.rows): break
            if(move_row + (x * dirR) < 0): break
            if(board[move_row + (x * dirR)][move_col - 1 + (x * dirC)] == mark_move):
                count += 1
            else:
                break
        return count

    def check_eval_at_pos(self, move_col, move_row, board, player) -> int:
        #Checks how good a position is worth (for evaluating heuristically)
        
        current_piece = 1
        winning_move = 0
        #check right
        count_r = self.check_points(0, 1, move_row, move_col, board, player)
        #check left
        count_l = self.check_points(0, -1, move_row, move_col, board, player)
        #check down
        count_d = self.check_points(1, 0, move_row, move_col, board, player)
        #check up right
        count_up_right = self.check_points(-1, 1, move_row, move_col, board, player)
        #check up left
        count_up_left = self.check_points(-1, -1, move_row, move_col, board, player)
        #check down right
        count_down_right = self.check_points(1, 1, move_row, move_col, board, player)
        #check down left
        count_down_left = self.check_points(1, -1, move_row, move_col, board, player)
        if(count_r + count_l + current_piece >= 4):
            winning_move = 5
        if (count_d + current_piece >= 4):
            winning_move = 5
        if (count_up_right + count_down_left + current_piece >= 4):
            winning_move = 5
        if (count_up_left + count_down_right + current_piece >= 4):
            winning_move = 5
        return count_r + count_l + count_d + count_up_right +count_up_left + count_down_right + count_down_left + current_piece + winning_move