import random, connect4


class TranspositionTable():
    def __init__(self, game: 'connect4.Connect4'):
        self.game = game
        self.ZobristTable = [[[self.randomInt() for k in range(2)] for j in range(game.cols)] for x in range(game.rows)]
        self.count = 0
        self.table = {}
    
    def randomInt(self):
        #Random number between 0 and 2^64, astronomically unlikely to get the same number twice
        min = 0
        max = pow(2, 64)
        return random.randint(min,max)

    def computeHash(self, board):
        #encode the board into a hash using bit operators
        h = 0
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                if(board[i][j] != 0):
                    piece = board[i][j] - 1
                    h ^= self.ZobristTable[i][j][piece]
        return h

    def store(self, score, alpha, beta, best_move, hash, depth):
        #Stores the current node into the table
        if(len(self.table) >= 2000000): 
            self.table = {} #if the table is too big, we can clear all older boards
            return -1
        if(score <= alpha):
            flag = 'UPPERBOUND'
        elif(score >= beta):
            flag = "LOWERBOUND"
        else:
            flag = "EXACT"
        self.table[hash] = {
            "score": score,
            "flag": flag,
            "best_move": best_move,
            "depth": depth
            }
        
    def retrieve(self, hash):
        #Retrieves the node and returns it if found
        if hash in self.table:
            return self.table[hash]["score"], self.table[hash]["flag"], self.table[hash]["best_move"], self.table[hash]["depth"]
        return None, None, None, None
