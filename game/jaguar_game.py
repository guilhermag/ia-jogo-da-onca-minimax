import copy
from game.move import Move
from tabulate import tabulate

class JaguarGame:
    board = [
        # (1,1), (1,2), (1,3), (1,4), (1,5)
        ['c', 'c', 'c', 'c', 'c'],
        # (2,1), (2,2), (2,3), (2,4), (2,5)
        ['c', 'c', 'c', 'c', 'c'],
        # (3,1), (3,2), (3,3), (3,4), (3,5)
        ['c', 'c', 'o', 'c', 'c'],
        # (4,1), (4,2), (4,3), (4,4), (4,5)
        ['v', 'v', 'v', 'v', 'v'],
        # (5,1), (5,2), (5,3), (5,4), (5,5)
        ['v', 'v', 'v', 'v', 'v'],
        # (6,1), (6,2), (6,3), (6,4), (6,5)
        ['', 'v', 'v', 'v', ''],
        # (7,1), (7,2), (7,3), (7,4), (7,5)
        ['v', '', 'v', '', 'v'],
    ]
    score_board = {
        'o': 0,
        'o_position': ('3', '3')
    }

    # board = [
    #     # (1,1), (1,2), (1,3), (1,4), (1,5)
    #     ['c', 'c', 'c', 'c', 'c'],
    #     # (2,1), (2,2), (2,3), (2,4), (2,5)
    #     ['c', 'c', 'c', 'v', 'c'],
    #     # (3,1), (3,2), (3,3), (3,4), (3,5)
    #     ['v', 'c', 'v', 'v', 'v'],
    #     # (4,1), (4,2), (4,3), (4,4), (4,5)
    #     ['v', 'v', 'v', 'v', 'v'],
    #     # (5,1), (5,2), (5,3), (5,4), (5,5)
    #     ['v', 'v', 'c', 'v', 'v'],
    #     # (6,1), (6,2), (6,3), (6,4), (6,5)
    #     ['', 'v', 'v', 'c', ''],
    #     # (7,1), (7,2), (7,3), (7,4), (7,5)
    #     ['c', '', 'c', '', 'o'],
    # ]
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
        ('4', '3'): [('3', '3'), ('4', '2'), ('4', '4'), ('5', '3')],
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

    def print_current_board(self):
        # for row in self.board:
        #     print(row)
        print(tabulate(self.board, headers='firstrow', tablefmt='fancy_grid'))
        print()




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
                new_origin_coord = get_coord_board(coord)
                dest_check = current_board[new_origin_coord[0]][new_origin_coord[1]]
                if dest_check != 'v':
                    break
                possible_links = self.moveset.get(origin)
                for link in possible_links:
                    destination_coord = get_coord_board(link)
                    dest = current_board[destination_coord[0]][destination_coord[1]]
                    if dest == 'c':
                        dog_possible_links = self.moveset.get(link)
                        if coord in dog_possible_links and self.check_link_jump(origin, link, coord) and check_jump_direction(origin, link, coord, current_board):
                            current_board[destination_coord[0]][destination_coord[1]] = 'v'
                            current_board[origin_coord[0]][origin_coord[1]] = 'v'
                            new_origin_coord = get_coord_board(coord)
                            current_board[new_origin_coord[0]][new_origin_coord[1]] = 'o'
                            valid = True
                            self.score_board['o'] += 1
                            self.score_board['o_position'] = player_move.destination
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
                if player_move.player_type == 'o':
                    self.score_board['o_position'] = player_move.destination
        if valid:
            self.board = current_board
        return valid

    def move_player(self, move_str: str):
       winner = self.check_winner()
       if winner:
           print("Game over! Winner: ", winner)
           return
       player_move = Move.from_string(move_str)
       self.check_move_valid(player_move)


    def check_link_jump(self, origin: tuple[str, str], middle: tuple[str, str], destination: tuple[str, str]):
        possible_links_origin = self.moveset.get(origin)
        possible_links_end = self.moveset.get(destination)
        valid_start = False
        valid_end = False
        if middle in possible_links_origin:
            valid_start = True
        if middle in possible_links_end:
            valid_end = True
        return valid_start and valid_end
    
    def check_winner(self) -> str | None:
        if self.score_board['o'] >= 5:
            return 'o'
        if not self.check_jaguar_moves():
            return 'c'
        return None
    
    def check_jaguar_moves(self) -> bool:
        o_position = self.score_board['o_position']
        possible_moves = self.moveset.get(o_position)
        for move in possible_moves:
            coord = get_coord_board(move)
            dest = self.board[coord[0]][coord[1]]
            if dest == 'v':
                return True
        possible_links = self.moveset.get(o_position)
        for link in possible_links:
            link_coord = get_coord_board(link)
            link_dest = self.board[link_coord[0]][link_coord[1]]
            if link_dest == 'c':
                dog_possible_links = self.moveset.get(link)
                for dog_link in dog_possible_links:
                    dog_link_coord = get_coord_board(dog_link)
                    dog_link_dest = self.board[dog_link_coord[0]][dog_link_coord[1]]
                    if dog_link_dest == 'v' and check_jump_direction(o_position, link, dog_link, self.board):
                        return True
        return False


def get_coord_board(coord: tuple[str, str]) -> tuple[int, int]:
    coord_x =  int(coord[0]) - 1
    coord_y = int(coord[1]) - 1
    return coord_x, coord_y

def check_jump_direction(origin: tuple[str, str],
                         middle: tuple[str, str],
                         destination: tuple[str, str],
                         board) -> bool:
    verification_list = []

    if origin[0] == middle[0] == destination[0]:
        verification_list.append(True)

    if origin[1] == middle[1] == destination[1]:
        verification_list.append(True)

    origin_int = [int(origin[0]), int(origin[1])]
    middle_int = [int(middle[0]), int(middle[1])]
    destination_int = [int(destination[0]), int(destination[1])]

    x_check = origin_int[0] < middle_int[0] < destination_int[0]
    y_check = origin_int[1] < middle_int[1] < destination_int[1]
    if x_check and y_check:
        verification_list.append(True)

    x_check = origin_int[0] > middle_int[0] > destination_int[0]
    y_check = origin_int[1] < middle_int[1] < destination_int[1]

    if x_check and y_check:
        verification_list.append(True)

    x_check = origin_int[0] > middle_int[0] > destination_int[0]
    y_check = origin_int[1] > middle_int[1] > destination_int[1]

    if x_check and y_check:
        verification_list.append(True)

    x_check = origin_int[0] < middle_int[0] < destination_int[0]
    y_check = origin_int[1] > middle_int[1] > destination_int[1]

    if x_check and y_check:
        verification_list.append(True)


    return len(verification_list) == 1