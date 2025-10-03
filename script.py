from game.jaguar_game import JaguarGame


def main(name):
    game = JaguarGame()
    game.move_player('o m 3 3 4 3')
    print(game.board)
    game.move_player('c m 3 5 4 4')
    print(game.board)
    game.move_player('o m 4 3 5 3')
    print(game.board)
    game.move_player('c m 3 1 4 1')
    print(game.board)
    game.move_player('o s 3 5 3 3 5 3 3 3 1')
    print(game.board)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
