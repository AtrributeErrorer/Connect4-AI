import player

class PlayerManager():
    def __init__(self, player_1, player_2, graphics, square_size):
        if(player_1 == 1):
            self.player_1 = player.Human(graphics)
        if(player_2 == 1):
            self.player_2 = player.Human(graphics)
        if(player_1 == 2):
            self.player_1 = player.Ai(square_size)
        if(player_2 == 2):
            self.player_2 = player.Ai(square_size)
        self.players = [self.player_1, self.player_2]
    