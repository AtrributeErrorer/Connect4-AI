import connect4 , gui, playerManager
import pygame
import threading, transpositionTable
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    Player_1 = config.getint('SETTINGS', "Player_1")
    Player_2 = config.getint('SETTINGS', "Player_2")
    
    game = connect4.Connect4()
    width = game.cols
    height = (game.rows + 2)
    graphics = gui.GUI(width, height)
    
    players_manager = playerManager.PlayerManager(Player_1, Player_2, graphics, graphics.SQUARE_SIZE)
    transposition_table = transpositionTable.TranspositionTable(game)

    pygame.event.clear()
    while True:
        col_posx_moverow = [None,0,0]
        while game.winner == None:
            graphics.draw_board(game.board, game.cols, game.rows)
            graphics.render_information(game.player, game.rows)
            graphics.animate_cursor(col_posx_moverow[1], game.player)
            pygame.display.flip()
            ## THREAD
            result = []
            def long_computation():
                move = players_manager.players[game.player - 1].get_move(game, transposition_table)
                result.append(move)
            if(players_manager.players[game.player - 1].is_ai() == False):
                move = players_manager.players[game.player - 1].get_move(game, transposition_table)
                result.append(move)
            else:
                thread = threading.Thread(target=long_computation, daemon= True)
                thread.start()
                while thread.is_alive():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    graphics.clock.tick(120)
                ## END
            col_posx_moverow = result[0]
            if(game.check_winner(col_posx_moverow[0], col_posx_moverow[2], game.board, game.player)):
                game.winner = game.player  # type: ignore[assignment]
            if(game.check_draw() and game.winner == None): game.winner = "Draw" # type: ignore[assignment]
            graphics.animation_fall(col_posx_moverow[1], col_posx_moverow[2], game)
            if(game.winner != None): 
                graphics.show_winner(game)
                pygame.display.update()
                pygame.time.wait(3000)
                if(graphics.restart_game()): 
                    game = connect4.Connect4()
                    continue
                break
            game.switch_player()

main()