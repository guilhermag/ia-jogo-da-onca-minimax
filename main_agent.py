import sys
import redis
import time
from multiprocessing import Pool
from typing import Tuple
import os

from game.jaguar_game import JaguarGame 
from game.move import Move     


def parse_redis_message(message_string: str) -> Tuple[JaguarGame, str]:
    """
    Analisa a string bruta recebida, que é estruturada por LINHAS.
    A string contém o Lado, o Movimento do Adv, e o Bloco do Tabuleiro.
    """
    
    lines = message_string.split('\n')
    
    lines = [line.strip() for line in lines if line.strip()] 
    
    if len(lines) < 4:
        raise ValueError("Mensagem de Redis muito curta. Protocolo inválido.")

    player_side = lines[0].strip()
    
    start_index = -1
    for i, line in enumerate(lines):
        if '#' in line:
            start_index = i
            break
            
    if start_index == -1:
        raise ValueError("Erro de Parsing: Não foi encontrada a marcação do tabuleiro ('#').")

    board_lines_block = lines[start_index : start_index + 9] 

    if len(board_lines_block) < 9:
        raise ValueError("Erro de Parsing: O bloco do tabuleiro está incompleto (menos de 9 linhas).")

    new_board_state = []
    for i in range(1, 8):
        line = board_lines_block[i].strip()
        
        content_line = line[1:-1]
        
        row = []
        for char in content_line:
            if char in ['c', 'o']:
                row.append(char)
            elif char == '-':  # O controlador C usa '-' para vazio
                row.append('v')
            elif char == ' ':  # O controlador C usa ' ' para posição nula/espaço
                row.append('')
            else:
                row.append('v') # Default para evitar erros
                
        if len(row) == 5:
            new_board_state.append(row)
            
    if len(new_board_state) != 7:
        raise ValueError(f"Erro de Parsing: O tabuleiro reconstruído tem {len(new_board_state)} linhas, não 7.")

    current_game = JaguarGame(board_state=new_board_state)
    return current_game, player_side


def run_agent_loop(player_side: str, depth: int):
    r = redis.Redis(host='127.0.0.1', port=10001) 
    print(f"Agente da {player_side.upper()} conectado ao Redis na porta 10001.")
    
    queue_rec = f'tabuleiro_{player_side}'  # Ex: 'tabuleiro_o'
    queue_sen = f'jogada_{player_side}'    # Ex: 'jogada_o'
    
    is_maximizing = (player_side == 'o') 
    game_counter = 0
    while True:
        print(f"Esperando turno ({queue_rec})...")
        
        try:
            result = r.blpop(queue_rec, timeout=0) 
        except Exception as e:
            print(f"Erro de Conexão/BLPOP: {e}")
            break

        if result is None:
            continue 
            
        message = result[1].decode('utf-8')
        lines = message.split('\n')
        
        try:
            last_move = lines[1].strip()
        except IndexError:
            last_move = "" 

        if ' n' in last_move and game_counter > 0: 
            print(f"SINAL DE FIM DE JOGO RECEBIDO: {last_move}")
            break

        try:
            current_game, received_side = parse_redis_message(message)
            
            if received_side != player_side:
                print(f"ERRO: Recebido turno para {received_side} quando deveria ser {player_side}")
                continue
                
        except Exception as e:
            print(f"Erro ao fazer parsing da mensagem: {e}. Mensagem: {message}")
            continue 

        print(f"Calculando jogada... Profundidade: {depth}")
        start_time = time.time()
        
        best_move_string = find_best_move(current_game, depth, is_maximizing)
        
        end_time = time.time()
        print(f"Tempo de busca: {end_time - start_time:.2f}s")
        game_counter = game_counter + 1
        if best_move_string:
            play_to_send = best_move_string + '\n' 
            
            r.rpush(queue_sen, play_to_send)
            print(f"Jogada enviada: {play_to_send.strip()}")
        else:
            print("FIM: Não há movimentos válidos. Enviando movimento nulo (se o protocolo permitir).")
            r.rpush(queue_sen, f'{player_side} n\n')
            break

def evaluate_child_state(args):
    """Função auxiliar para a busca paralela."""
    cloned_game, depth, is_maximizing_player = args
    score = minimax(cloned_game, depth - 1, not is_maximizing_player, float('-inf'), float('inf'))
    return score

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
    tasks = []
    for move in moves:
        cloned_game = game.clone_game()
        cloned_game.check_move_valid(move)
        tasks.append((cloned_game, depth, isMaximizingPlayer))

    #ufpr
    # num_cores = min(os.cpu_count(), 16)
    #notebook pessoal
    num_cores = min(os.cpu_count(), 1)
    with Pool(processes=num_cores) as pool:
            scores = pool.map(evaluate_child_state, tasks)
    
    for score, move in zip(scores, moves):
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
    
    if len(sys.argv) < 3:
        print("Uso: python main_agent.py [o|c] [profundidade]")
        sys.exit(1)
        
    player_side = sys.argv[1].lower() # 'o' ou 'c'
    try:
        depth = int(sys.argv[2])
    except ValueError:
        print("Profundidade deve ser um número inteiro.")
        sys.exit(1)
        
    if player_side not in ['o', 'c']:
        print("Lado inválido. Use 'o' ou 'c'.")
        sys.exit(1)
        
    run_agent_loop(player_side, depth)