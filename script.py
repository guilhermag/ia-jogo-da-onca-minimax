from game.jaguar_game import JaguarGame


def main(name):
    game = JaguarGame()

    # game.move_player('o m 3 3 4 3')
    # # game.print_current_board()
    # game.move_player('c m 3 5 4 4')
    # # game.print_current_board()
    # game.move_player('o m 4 3 5 3')
    # # game.print_current_board()
    # game.move_player('c m 3 1 4 1')
    # game.print_current_board()
    # valid_moves = game.get_valid_moves('c')
    # for move in valid_moves:
    #     print(move)
    # game.move_player('o s 3 5 3 3 5 3 3 3 1')
    # game.print_current_board()

def minimax(game: JaguarGame, depth, isMaximizingPlayer, alpha, beta):
    if depth == 0 or game.score_board['c'] or game.score_board['o'] >= 5:
        return game.heuristic_evaluation()

    if isMaximizingPlayer:
        maxEval = float('-inf')
        for child in game.get_children(isMaximizingPlayer):
            eval = minimax(child, depth - 1, False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for child in game.get_children(isMaximizingPlayer):
            eval = minimax(child, depth - 1, True, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def find_best_move(game: JaguarGame, depth: int, isMaximizingPlayer: bool):
    best_move = None
    best_score = float('-inf')
    player = 'o' if isMaximizingPlayer else 'c'
    moves = game.get_valid_moves(player)

    for move in moves:
        cloned_game = game.clone_game()
        cloned_game.check_move_valid(move)
        score = minimax(cloned_game, depth - 1,  not isMaximizingPlayer, float('-inf'), float('inf'))
        
        if isMaximizingPlayer:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
            
    return best_move.to_string() if best_move else None

if __name__ == '__main__':
    main('main')


