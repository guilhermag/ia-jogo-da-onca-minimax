from game.jaguar_game import JaguarGame
from game.move import Move
import redis
import time

def main(name):
    game = JaguarGame()
    current_player_is_maximizing = True 
    depth = 5
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("Conectado ao Redis.")
    except redis.exceptions.ConnectionError as e:
        print("Não foi possível conectar ao Redis. Rodando em modo offline.")
    while game.check_winner() is None:
        print(game.score_board)
        print(f"\n--- Turno da {'Onça' if current_player_is_maximizing else 'Cães'} ---")
        

        best_move = find_best_move(game, depth, current_player_is_maximizing)

        if best_move:
            print(f"A IA escolhe: {best_move}")
            
            # Aplica o movimento no tabuleiro
            move = Move.from_string(best_move)
            game.check_move_valid(move)
            
            # Alterna para o próximo jogador
            current_player_is_maximizing = not current_player_is_maximizing
        else:
            print("Não há movimentos válidos. Fim de jogo inesperado.")
            break
        
        # time.sleep(1) # Pausa para facilitar a visualização
        
    winner = game.check_winner()
    print("\n--- Fim do Jogo ---")
    print(f"O vencedor é: {winner}!")
    
    

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
    if isMaximizingPlayer:
        player = 'o'
        best_score = float('-inf')
    else:
        player = 'c'
        best_score = float('inf')
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


