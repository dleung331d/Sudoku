import random
import logging
from collections import defaultdict

# ver 0.1 - initial version
# game mode                 = AI only
# board generation          = none.  User has to input a board manually in init method
# player board generation   = none.  User has to input a board manually in init method
# board resolution          = brute force
#
# To-dos
# game mode                 = player or AI
# board generation          = automatic
# player board generation   = automatic
# board resolution          = start with cell with smallest number of choices

class Sudoku:
    def __init__(self):
        #self.board = self.initialize_board()
        self.board = {0: {0: 5, 1: 8, 2: 2, 3: 4, 4: 7, 5: 1, 6: 6, 7: 9, 8: 3},
                      1: {0: 6, 1: 9, 2: 3, 3: 5, 4: 8, 5: 2, 6: 4, 7: 7, 8: 1},
                      2: {0: 4, 1: 7, 2: 1, 3: 6, 4: 9, 5: 3, 6: 5, 7: 8, 8: 2},
                      3: {0: 2, 1: 5, 2: 8, 3: 1, 4: 4, 5: 7, 6: 3, 7: 6, 8: 9},
                      4: {0: 3, 1: 6, 2: 9, 3: 2, 4: 5, 5: 8, 6: 1, 7: 4, 8: 7},
                      5: {0: 1, 1: 4, 2: 7, 3: 3, 4: 6, 5: 9, 6: 2, 7: 5, 8: 8},
                      6: {0: 8, 1: 2, 2: 5, 3: 7, 4: 1, 5: 4, 6: 9, 7: 3, 8: 6},
                      7: {0: 9, 1: 3, 2: 6, 3: 8, 4: 2, 5: 5, 6: 7, 7: 1, 8: 4},
                      8: {0: 7, 1: 1, 2: 4, 3: 9, 4: 3, 5: 6, 6: 8, 7: 2, 8: 5}
                      }
        #self.board_player = dict()
        self.board_player = { 0: {0: 2, 1: 0, 2: 0, 3: 0, 4: 8, 5: 0, 6: 4, 7: 0, 8: 0},	1: {0: 0, 1: 1, 2: 7, 3: 2, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},	2: {0: 4, 1: 0, 2: 0, 3: 0, 4: 3, 5: 0, 6: 9, 7: 1, 8: 0},	3: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 5, 6: 0, 7: 0, 8: 0},	4: {0: 6, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 7},	5: {0: 0, 1: 4, 2: 0, 3: 0, 4: 7, 5: 0, 6: 3, 7: 0, 8: 0},	6: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 3},	7: {0: 0, 1: 0, 2: 2, 3: 0, 4: 9, 5: 0, 6: 8, 7: 0, 8: 0},	8: {0: 9, 1: 0, 2: 0, 3: 0, 4: 0, 5: 6, 6: 0, 7: 0, 8: 0}
                              }
        self.empty_cells = self.get_empty_cells_list()

        formatter = logging.Formatter("[%(funcName)s-%(message)s]")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        file_handler = logging.FileHandler("sudoku.log")
        #file_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.addHandler(file_handler)
        #self.logger.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.INFO)

    # Returns
    # 1 if a valid value exists for the given empty cell.  The value will be assigned to that cell
    # 0 if no valid value exists for the given empty cell
    def assign_valid_value_to_empty_cell(self, x, y, valid_values):
        self.logger.debug(f'x:{str(x)} y:{str(y)} valid_values:' + ' '.join(str(valid_values)) + '\n')
        if len(valid_values) >= 1:
            # assign a valid value to this cell
            v = valid_values.pop()
            self.board_player[x][y] = v
            self.logger.debug(f'x:{str(x)} y:{str(y)} assigned with {str(v)}')
            return 1
        else:
            return 0

    # Returns a list of empty cells on player board
    def get_empty_cells_list(self):
        empty_cells = list()
        for x in range(0, 9):
            for y in range(0, 9):
                if self.board_player[x][y] == 0:
                    empty_cells.append([x, y])
        return empty_cells

    @staticmethod
    def get_subgrid_number(x, y):
        # subgrids
        # 0: 0 <= x <= 2; 0 <= y <= 2
        # 1: 3 <= x <= 5; 0 <= y <= 2
        # 2: 6 <= x <= 8; 0 <= y <= 2
        #
        # 3: 0 <= x <= 2; 3 <= y <= 5
        # 4: 3 <= x <= 5; 3 <= y <= 5
        # 5: 6 <= x <= 8; 3 <= y <= 5
        if 0 <= y <= 2:
            if 0 <= x <= 2:
                return 0
            elif 3 <= x <= 5:
                return 1
            elif 6 <= x <= 8:
                return 2
        elif 3 <= y <= 5:
            if 0 <= x <= 2:
                return 3
            elif 3 <= x <= 5:
                return 4
            elif 6 <= x <= 8:
                return 5
        elif 6 <= y <= 8:
            if 0 <= x <= 2:
                return 6
            elif 3 <= x <= 5:
                return 7
            elif 6 <= x <= 8:
                return 8

    # Returns a list of valid values for a given cell
    def get_valid_values_for_cell(self, x, y):
        valid_values = list()
        for num in range(1, 10):
            if self.is_valid_value(x, y, num):
                valid_values.append(num)
        return valid_values

    # Returns a valid board of Sudoku with all cells populated
    def initialize_board(self):
        board = defaultdict(dict)
        # board = dict of list
        # board[0] = row 0 = [1, 2, 3, 5, ...]

        # Temp variables for populating the board
        # num_used_in_column[0] = column 0 = list [1, 2, 3...]
        # 9 columns in total
        # using a dictionary of list instead of nested dictionaries because
        # we just need a list of used numbers rather than the exact location+value of each cell
        num_used_in_column = defaultdict(list)

        # num_used_in_subgrid[0] = subgrid 0 = list [1, 2, 3...]
        # 9 subgrids in total
        num_used_in_subgrid = defaultdict(list)

        # Generate board row by row
        for y in range(0, 9):
            # for each cell in row x
            num_used_in_row = list()
            for x in range(0, 9):
                subgrid_num = self.get_subgrid_number(x, y)
                board[x][y] = 0
                rand_int = random.randint(1, 9)
                # if rand_int is not yet used in
                # - the row
                # - AND column
                # - AND its respective 3x3 sub-grid
                # assign value to board[x][y]

                rand_int_list = ''
                while rand_int in num_used_in_row \
                        or rand_int  in num_used_in_column[x] \
                        or rand_int  in num_used_in_subgrid[subgrid_num]:
                    rand_int = random.randint(1, 9)
                    rand_int_list += str(rand_int)
                    if len(rand_int_list) >= 19:
                        exit()
                num_used_in_row.append(rand_int)
                num_used_in_column[x].append(rand_int)
                num_used_in_subgrid[subgrid_num].append(rand_int)
                board[x][y] = rand_int
                # DLTEST
                print(f'{str(x),str(y)} int:{str(rand_int)} subgrid:{str(subgrid_num)}')
                print(board)
                print('num_used_in_row:' + ' '.join(str(num_used_in_row)))
                print(num_used_in_column[x])
                print(num_used_in_subgrid[subgrid_num])
                print()
        return board

    # Returns
    # 0 if the value is not valid in subgrid
    # 1 otherwise (ie value is valid in subgrid)
    def is_valid_value_in_subgrid(self, subgrid_num, value):
        if subgrid_num == 0:
            if value in [self.board_player[x][y] for y in range(0,3) for x in range(0,3)]:
                return 0
        elif subgrid_num == 1:
            if value in [self.board_player[x][y] for y in range(0,3) for x in range(3,6)]:
                return 0
        elif subgrid_num == 2:
            if value in [self.board_player[x][y] for y in range(0,3) for x in range(6,9)]:
                return 0
        elif subgrid_num == 3:
            if value in [self.board_player[x][y] for y in range(3,6) for x in range(0,3)]:
                return 0
        elif subgrid_num == 4:
            if value in [self.board_player[x][y] for y in range(3,6) for x in range(3,6)]:
                return 0
        elif subgrid_num == 5:
            if value in [self.board_player[x][y] for y in range(3,6) for x in range(6,9)]:
                return 0
        elif subgrid_num == 6:
            if value in [self.board_player[x][y] for y in range(6,9) for x in range(0,3)]:
                return 0
        elif subgrid_num == 7:
            if value in [self.board_player[x][y] for y in range(6,9) for x in range(3,6)]:
                return 0
        elif subgrid_num == 8:
            if value in [self.board_player[x][y] for y in range(6,9) for x in range(6,9)]:
                return 0
        return 1

    def is_valid_value(self, x, y, value):
        # if value is not yet used in board_player
        #                 # - the row
        #                 # - AND column
        #                 # - AND its respective 3x3 sub-grid
        #                 # assign value to board[x][y]

        # If board_player is nested dict
        # Check column x
        if value in self.board_player[x].values():
            # DLTEST
            # print(f'Value {str(value)} is not valid in column {str(x)}')
            return 0
        # Check row y
        elif value in [self.board_player[c][y] for c in range(0,9)]:
            # DLTEST
            # print(f'Value {str(value)} is not valid in row {str(y)}')
            return 0
        # Check 3x3 sub-grid
        else:
            subgrid_num = self.get_subgrid_number(x, y)
            if self.is_valid_value_in_subgrid(subgrid_num, value):
                # DLTEST
                # print(f'Value {str(value)} is valid at {str(x), str(y)}')
                return 1
            else:
                # DLTEST
                # print(f'Value {str(value)} is not valid in subgrid {str(subgrid_num)}')
                return 0

    # Prints the full board
    @staticmethod
    def print_board(board):
        # DLTEST
        print('Board is ')
        print(board)

        # Print cells
        for y in range(0, 9):
            row_string = ''
            for x in range(0, 9):
                cell_value = board[x][y]
                row_string += ' ' + str(cell_value) + ' |'
            if y in [2, 5]:
                row_string += '\n' + '_'*36
            print(row_string)
        print()

    # Program will try to solve the board by brute force
    def solve_sudoku(self):
        num_empty_cells = len(self.empty_cells)

        # If this is the last empty cell
        if num_empty_cells == 0:
            return 1
        else:
            # Pop the first empty cell
            x, y = self.empty_cells.pop(0)

            # find valid values for this empty cell
            valid_values = self.get_valid_values_for_cell(x, y)
            self.logger.debug(f'x:{str(x)} y:{str(y)} valid_values:' + ' '.join(str(valid_values)) + '\n')
            self.logger.debug(
                'num_empty_cells:' + str(len(self.empty_cells)) + ' empty_cells:' + ''.join(str(self.empty_cells)) + '\n')

            if self.assign_valid_value_to_empty_cell(x, y, valid_values):
                # Move onto next empty cell
                # Loop:
                # if no more valid values, go back to last empty cell and try another value
                #
                self.logger.debug(f' about to enter while loop: x:{str(x)} y:{str(y)} \n')
                while self.solve_sudoku() != 1:
                    self.logger.debug(f' while loop: x:{str(x)} y:{str(y)} \n')
                    if self.assign_valid_value_to_empty_cell(x, y, valid_values) != 1:
                        # No valid value for this cell.
                        return self.step_back(x, y)
                self.logger.debug(f'x:{str(x)} y:{str(y)} final value:{self.board_player[x][y]}' + '\n')
            else:
                # No valid value for this cell.
                return self.step_back(x, y)
            self.logger.debug(f'x:{str(x)} y:{str(y)} final value:{self.board_player[x][y]}' + '\n')
            return 1

    # When program fails to find a valid value for a cell, it needs to revert the last move(s) and try different values
    def step_back(self, x, y):
        self.logger.debug(f' start - [{str(x), str(y)}]')
        self.board_player[x][y] = 0
        if [x, y] not in self.empty_cells:
            self.empty_cells.insert(0, [x, y])
            self.logger.debug(f'Added [{str(x), str(y)}] back to empty_cells list:' + ''.join(str(self.empty_cells)))
        return 0

# Leave blank


# Main
if __name__ == '__main__':
    s = Sudoku()
    s.print_board(s.board_player)

    s.logger.debug('num_empty_cells:' + str(len(s.empty_cells)) + ' empty_cells:' + ''.join(str(s.empty_cells)))

    s.solve_sudoku()
    s.print_board(s.board_player)
