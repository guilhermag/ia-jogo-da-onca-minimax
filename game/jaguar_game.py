import copy
from game.move import Move

class JaguarGame:
    # board = [
    #     # (1,1), (1,2), (1,3), (1,4), (1,5)
    #     ['c', 'c', 'c', 'c', 'c'],
    #     # (2,1), (2,2), (2,3), (2,4), (2,5)
    #     ['c', 'c', 'c', 'c', 'c'],
    #     # (3,1), (3,2), (3,3), (3,4), (3,5)
    #     ['c', 'c', 'o', 'c', 'c'],
    #     # (4,1), (4,2), (4,3), (4,4), (4,5)
    #     ['v', 'v', 'v', 'v', 'v'],
    #     # (5,1), (5,2), (5,3), (5,4), (5,5)
    #     ['v', 'v', 'v', 'v', 'v'],
    #     # (6,1), (6,2), (6,3), (6,4), (6,5)
    #     ['', 'v', 'v', 'v', ''],
    #     # (7,1), (7,2), (7,3), (7,4), (7,5)
    #     ['v', '', 'v', '', 'v'],
    # ]

    board = [
        # (1,1), (1,2), (1,3), (1,4), (1,5)
        ['c', 'c', 'c', 'c', 'c'],
        # (2,1), (2,2), (2,3), (2,4), (2,5)
        ['c', 'c', 'c', 'c', 'c'],
        # (3,1), (3,2), (3,3), (3,4), (3,5)
        ['v', 'c', 'v', 'c', 'v'],
        # (4,1), (4,2), (4,3), (4,4), (4,5)
        ['c', 'v', 'v', 'c', 'v'],
        # (5,1), (5,2), (5,3), (5,4), (5,5)
        ['v', 'v', 'o', 'v', 'v'],
        # (6,1), (6,2), (6,3), (6,4), (6,5)
        ['', 'v', 'v', 'v', ''],
        # (7,1), (7,2), (7,3), (7,4), (7,5)
        ['v', '', 'v', '', 'v'],
    ]
    moveset = {
        ('1', '1'): [('1', '2'), ('2', '1'), ('2', '2')],
        ('1', '2'): [('1', '1'), ('1', '3'), ('2', '2')],
        ('1', '3'): [('1', '2'), ('1', '4'), ('2', '2'), ('2', '4')],
        ('1', '4'): [('1', '3'), ('1', '5'), ('2', '4')],
        ('1', '5'): [('1', '4'), ('2', '4'), ('2', '5')],
        ('2', '1'): [('1', '1'), ('2', '2'), ('3', '1')],
        ('2', '2'): [('1', '1'), ('1', '2'), ('1', '3'), ('2', '1'), ('2', '3'), ('3', '1'), ('3', '2'), ('3', '3')],
        ('2', '3'): [('1', '3'), ('2', '2'), ('2', '4'), ('3', '3')],
        ('2', '4'): [('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '5'), ('3', '3'), ('3', '4'), ('3', '5')],
        ('2', '5'): [('1', '5'), ('2', '4'), ('3', '5')],
        ('3', '1'): [('2', '1'), ('2', '2'), ('3', '2'), ('4', '1'), ('4', '2')],
        ('3', '2'): [('2', '2'), ('3', '1'), ('3', '3'), ('4', '2')],
        ('3', '3'): [('2', '2'), ('2', '3'), ('2', '4'), ('3', '2'), ('3', '4'), ('4', '2'), ('4', '3'), ('4', '4')],
        ('3', '4'): [('2', '4'), ('3', '3'), ('3', '5'), ('4', '4')],
        ('3', '5'): [('2', '4'), ('2', '5'), ('3', '4'), ('4', '4'), ('4', '5')],
        ('4', '1'): [('3', '1'), ('4', '2'), ('5', '1')],
        ('4', '2'): [('3', '1'), ('3', '2'), ('3', '3'), ('4', '1'), ('4', '3'), ('5', '1'), ('5', '2'), ('5', '3')],
        ('4', '3'): [('3', '3'), ('4', '2'), ('4', '4'), ('5', '2')],
        ('4', '4'): [('3', '3'), ('3', '4'), ('3', '5'), ('4', '3'), ('4', '5'), ('5', '3'), ('5', '4'), ('5', '5')],
        ('4', '5'): [('3', '5'), ('4', '4'), ('5', '5')],
        ('5', '1'): [('4', '1'), ('4', '2'), ('5', '2')],
        ('5', '2'): [('4', '1'), ('5', '1'), ('5', '3')],
        ('5', '3'): [('4', '2'), ('4', '3'), ('4', '4'), ('5', '2'), ('5', '4'), ('6', '2'), ('6', '3'), ('6', '4')],
        ('5', '4'): [('4', '4'), ('5', '3'), ('5', '5')],
        ('5', '5'): [('4', '4'), ('4', '5'), ('5', '4')],
        ('6', '2'): [('5', '3'), ('6', '3'), ('7', '1')],
        ('6', '3'): [('5', '3'), ('6', '2'), ('6', '4'), ('7', '3')],
        ('6', '4'): [('5', '3'), ('6', '3'), ('7', '5')],
        ('7', '1'): [('6', '2'), ('7', '3')],
        ('7', '3'): [('6', '3'), ('7', '1'), ('7', '5')],
        ('7', '5'): [('6', '4'), ('7', '3')]
    }

    def check_move_valid(self, player_move: Move) -> bool:
        current_board = copy.deepcopy(self.board)
        valid = False
        if player_move.move_type == 's':
            if player_move.player_type != 'o':
                return False
            if len(player_move.destination) % 2 != 0:
                return False
            origin = player_move.origin
            origin_coord = get_coord_board(origin)
            for i in range(player_move.number_of_jumps):
                valid = False
                counter = i * 2
                if counter < len(player_move.destination):
                    coord = player_move.destination[counter: counter + 2]
                else:
                    coord = player_move.destination[counter:]
                coord = (coord[0], coord[1])

                possible_links = self.moveset.get(origin)
                for link in possible_links:
                    destination_coord = get_coord_board(link)
                    dest = current_board[destination_coord[0]][destination_coord[1]]
                    if dest == 'c':
                        dog_possible_links = self.moveset.get(link)
                        if coord in dog_possible_links:
                            current_board[destination_coord[0]][destination_coord[1]] = 'v'
                            current_board[origin_coord[0]][origin_coord[1]] = 'v'
                            new_origin_coord = get_coord_board(coord)
                            current_board[new_origin_coord[0]][new_origin_coord[1]] = 'o'
                            valid = True
                            break
                if not valid:
                    break
                origin = coord
                origin_coord = get_coord_board(origin)
        else:
            origin_coord = get_coord_board(player_move.origin)
            destination_coord = get_coord_board(player_move.destination)
            dest = self.board[destination_coord[0]][destination_coord[1]]
            if dest != 'v':
                valid = False
            possible_moves = self.moveset.get(player_move.origin)
            if player_move.destination in possible_moves:
                current_board[origin_coord[0]][origin_coord[1]] = 'v'
                current_board[destination_coord[0]][destination_coord[1]] = player_move.player_type
                valid = True
        if valid:
            self.board = current_board
        return valid

    def move_player(self, move_str: str):
       player_move = Move.from_string(move_str)

       # if player_type == 'c':
       result = self.check_move_valid(player_move)
       if result:
           self.display_board()
       #print(player_destination)

    def _get_piece_char(self, row, col):
        """Função auxiliar para obter o caractere correto para a peça."""
        piece = self.board[row][col]
        if piece == 'c':
            return 'c'  # Cachorro
        if piece == 'o':
            return 'o'  # Onça
        if piece == 'v':
            return '*'  # Espaço vazio válido
        return ' '  # Espaço inválido (fora do tabuleiro triangular)

    def display_board(self):
        """Imprime o estado atual do tabuleiro no console."""

        p = {}
        for r in range(7):
            for c in range(5):
                p[f'p{r + 1}{c + 1}'] = self._get_piece_char(r, c)

        # MOLDE CORRIGIDO E ALINHADO
        board_str = rf"""
    Tabuleiro Atual:

    1   {p['p11']}---{p['p12']}---{p['p13']}---{p['p14']}---{p['p15']}
        | \ | / | \ | / | \ | / |
    2   {p['p21']}---{p['p22']}---{p['p23']}---{p['p24']}---{p['p25']}
        | / | \ | / | \ | / | \ |
    3   {p['p31']}---{p['p32']}---{p['p33']}---{p['p34']}---{p['p35']}
        | \ | / | \ | / | \ | / |
    4   {p['p41']}---{p['p42']}---{p['p43']}---{p['p44']}---{p['p45']}
        | / | \ | / | \ | / | \ |
    5   {p['p51']}---{p['p52']}---{p['p53']}---{p['p54']}---{p['p55']}
              \  |  /   \  |  /
    6          {p['p62']}---{p['p63']}---{p['p64']}
                 \ | /   \ | /
    7          {p['p71']}---{p['p73']}---{p['p75']}
          """
        print(board_str)


def get_coord_board(coord) -> tuple[int, int]:
    coord_x =  int(coord[0]) - 1
    coord_y = int(coord[1]) - 1
    return coord_x, coord_y
