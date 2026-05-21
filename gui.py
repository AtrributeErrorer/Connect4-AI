import pygame
import sys
import math, connect4

pygame.init()

DROP_SPEED = 10
PREVIEW_SPEED = 5


class GUI:
    def __init__(self, width, height):
        self.screen_width = 700
        self.screen_height = 800
        self.SQUARE_SIZE = min(self.screen_width//width, self.screen_height//height)
        self.width = width * self.SQUARE_SIZE
        self.height = height * self.SQUARE_SIZE
        self.BOARD_Y_OFFSET = self.SQUARE_SIZE

        self.circle_radius = int(self.SQUARE_SIZE/2 - 5)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.BlueRGB = (0,0,255)
        self.WhiteRGB = (255, 255, 255)
        self.YellowRGB = (255, 255, 0)
        self.DarkYellowRGB = (155, 122, 1)
        self.RedRGB = (255, 0, 0)
        self.BlackRGB = (0,0,0)
        

    def draw_board(self, board, cols, rows):
        self.screen.fill("white")
        
        for x in range(cols):
            for r in range(rows):
                circle_y = int(r*self.SQUARE_SIZE+self.BOARD_Y_OFFSET+(self.SQUARE_SIZE/2))
                circle_x = int(x * self.SQUARE_SIZE+(self.SQUARE_SIZE/2))
                pygame.draw.rect(self.screen, self.BlueRGB, (x * self.SQUARE_SIZE, r*self.SQUARE_SIZE + self.BOARD_Y_OFFSET, self.SQUARE_SIZE, self.SQUARE_SIZE))
                if(board[r][x] == 0):
                    pygame.draw.circle(self.screen, self.WhiteRGB, (circle_x, circle_y), self.circle_radius)
                elif(board[r][x] == 1):
                    pygame.draw.circle(self.screen, self.RedRGB, (circle_x, circle_y), self.circle_radius)
                else:
                    pygame.draw.circle(self.screen, self.YellowRGB, (circle_x, circle_y), self.circle_radius)

    def animation_fall(self, posx, moveRow, game: 'connect4.Connect4'):
        col = int(math.floor(posx/self.SQUARE_SIZE))
        x = int(col * self.SQUARE_SIZE + self.SQUARE_SIZE//2)
        start_y = self.SQUARE_SIZE//2
        end_y = moveRow * self.SQUARE_SIZE + self.BOARD_Y_OFFSET + self.SQUARE_SIZE // 2
        game.undo_move(game.last_move, game.board)
        if(game.player == 1):
            color = self.RedRGB
        else:
            color = self.YellowRGB

        y = int(start_y)
        start_y_next_move = 0 - self.SQUARE_SIZE
        start_x_next_move = posx

        while y <= end_y:
            self.draw_board(game.board, game.cols, game.rows)
            pygame.draw.circle(self.screen, color, (x, y), self.circle_radius)
            if(color == self.RedRGB): colorDrop = self.YellowRGB
            else: colorDrop = self.RedRGB
            pygame.draw.circle(self.screen, colorDrop, (start_x_next_move, start_y_next_move), self.circle_radius)
            pygame.display.update()
            pygame.time.delay(1)
            if(start_y_next_move <= self.SQUARE_SIZE//2 - 5): 
                start_y_next_move += PREVIEW_SPEED
            y+= DROP_SPEED
        game.make_play(game.last_move, game.board, game.player)
        self.draw_board(game.board, game.cols, game.rows)

    
    def animate_cursor(self, posx, player):
        pygame.draw.rect(self.screen, self.WhiteRGB, (0,0, self.screen_width, self.SQUARE_SIZE))
        if player == 1:
            pygame.draw.circle(self.screen, self.RedRGB, (posx, int(self.SQUARE_SIZE/2)), self.circle_radius)
            pygame.display.update()
        else:
            pygame.draw.circle(self.screen, self.YellowRGB, (posx, int(self.SQUARE_SIZE/2)), self.circle_radius)
        pygame.display.update()

    def clicked_move(self, game) -> list:
        posx = 0
        self.clock.tick(120)  # limits FPS to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.animate_cursor(event.pos[0], game.player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx/self.SQUARE_SIZE)) + 1
                if(col > game.cols): return []
                
                return [col, posx]
        return []
            
        

    def show_winner(self, game):
        myfont = pygame.font.SysFont("monospace", int(self.SQUARE_SIZE*0.75))
        if(game.winner!="Draw"):
            if(game.player == 1):
                color = self.RedRGB
            else:
                color = self.DarkYellowRGB
            pygame.draw.rect(self.screen, self.WhiteRGB, (0,0, self.width, self.SQUARE_SIZE))
            label = myfont.render("Player " + str(game.winner) + " wins", True, color)
            self.screen.blit(label,(40,10))
        else:
            pygame.draw.rect(self.screen, self.WhiteRGB, (0,0, self.width, self.SQUARE_SIZE))
            label = myfont.render("Game is a " + str(game.winner), True, self.BlueRGB)
            self.screen.blit(label,(40,10))

    def render_information(self, player, rows):
        font = pygame.font.SysFont("monospace", 30)
        current_player = font.render("Player " + str(player) + "'s turn", True, self.BlackRGB)
        self.screen.blit(current_player,(20,rows*self.SQUARE_SIZE + self.BOARD_Y_OFFSET))

    def restart_game(self):
        self.screen.fill("white")
        restart = False
        restart_text = pygame.font.SysFont("monospace", 30)
        label = restart_text.render("Left click to play again", True, self.BlackRGB)
        label2 = restart_text.render("Right click to quit", True, self.BlackRGB)
        pygame.display.flip()
        pygame.event.clear()
        while(not restart):
            self.screen.blit(label,(40,10))
            self.screen.blit(label2,(40,70))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button  == 1:
                        restart = True
                        return True
                    elif event.button == 3:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    sys.exit()
