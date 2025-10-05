from game.jaguar_game import JaguarGame


def main(name):
    game = JaguarGame()

    game.move_player('o m 3 3 4 3')
    # game.print_current_board()
    game.move_player('c m 3 5 4 4')
    # game.print_current_board()
    game.move_player('o m 4 3 5 3')
    # game.print_current_board()
    game.move_player('c m 3 1 4 1')
    game.print_current_board()
    valid_moves = game.get_valid_moves('c')
    for move in valid_moves:
        print(move)
    game.move_player('o s 3 5 3 3 5 3 3 3 1')
    # game.print_current_board()

if __name__ == '__main__':
    main('main')


