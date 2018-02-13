# Rachel Weber
# 96124542


import math


EMPTY = 0
BLACK = 1
WHITE = -1


class InvalidMoveError(Exception):
    pass


class InvalidSetting(Exception):
    pass


class InvalidCellContents(Exception):
    pass


class InvalidDiscColor(Exception):
    pass


class GameState:
    '''
    Memorizes and manipulates the state of the Othello game.
    '''
    def __init__(self, first_to_move: int, winner_mode: int, rows: int,
                 col: int, top_left_center_disc: int) -> None:
        self._player_making_move = first_to_move
        self._winner_mode = winner_mode
        self._winner = None
        self._gameboard = GameBoard(rows, col, top_left_center_disc)

    def to_string(self) -> str:
        '''
        Converts the game state into a printable string.
        '''
        game_as_str = "B: " + str(self._gameboard.no_of_black_discs()) + "  W: " + str(self._gameboard.no_of_white_discs()) + "\n" + self._gameboard.to_string()

        if self._player_making_move != None:
            game_as_str += "\n" + "TURN: " + GameState.player_to_string(self._player_making_move)
                 
        return game_as_str

    def player_take_turn(self, row_index: int, col_index: int):
        '''
        Places a disc at the given cell address. The disc matches the
        player whose turn it is. 
        '''
        if self._gameboard.valid_move(row_index, col_index, self._player_making_move):
            self._gameboard.place_disc(row_index, col_index, self._player_making_move)
        else:
            raise InvalidMoveError

    def next_player_turn(self):
        '''
        Determines who moves next. Invokes the _determine_winner method
        if there are no moves left for anyone.
        '''
        if not self._gameboard.no_moves(-1*self._player_making_move):
            self._player_making_move = -1*self._player_making_move
        elif not self._gameboard.no_moves(self._player_making_move):
            pass
        else:
            self._player_making_move = None
            self._determine_winner()

    def get_rows_of_cells(self) -> [["Cells"]]:
        return self._gameboard.get_rows_of_cells()

    def get_winner(self):
        return self._winner

    def no_of_rows(self):
        return self._gameboard.no_of_rows()

    def no_of_col(self):
        return self._gameboard.no_of_col()

    def black_score(self):
        return self._gameboard.no_of_black_discs()

    def white_score(self):
        return self._gameboard.no_of_white_discs()

    def player_making_move(self):
        return self._player_making_move

    def player_to_string(player_index: int):
        '''
        Converts a player's index to a string.
        '''
        if player_index == BLACK:
            return 'Black'
        elif player_index == WHITE:
            return 'White'
        elif player_index == EMPTY:
            return "None"
        else:
            raise InvalidDiscColor

    def _determine_winner(self):
        '''
        Determines the winner based on the settings.
        '''
        if self._winner_mode == '<':
            if self._gameboard.no_of_white_discs() < self._gameboard.no_of_black_discs():
                self._winner = WHITE
            elif self._gameboard.no_of_black_discs() < self._gameboard.no_of_white_discs():
                self._winner = BLACK
            else:
                self._winner = EMPTY
                
        elif self._winner_mode == '>':
            if self._gameboard.no_of_white_discs() > self._gameboard.no_of_black_discs():
                self._winner = WHITE
            elif self._gameboard.no_of_black_discs() > self._gameboard.no_of_white_discs():
                self._winner = BLACK
            else:
                self._winner = EMPTY
                
        else:
            raise InvalidSetting


class GameBoard:
    '''
    Represents the board of Tiles on which discs can be placed.
    '''    
    def __init__(self, rows: int, col: int, top_left_center_disc: int) -> None:
        '''
        Set up the game board.
        '''
        self._white_discs = Counter(2)
        self._black_discs = Counter(2)
        self._no_of_rows = rows
        self._no_of_col = col        
        self._rows = []

        # A list of functions giving the addresses of neighboring cells.
        self.neighbor_functions = [GameBoard._north_cell, GameBoard._south_cell, GameBoard._east_cell,
                      GameBoard._west_cell, GameBoard._northwest_cell,
                      GameBoard._southwest_cell, GameBoard._northeast_cell,
                      GameBoard._southeast_cell]        

        # Create the rows and columns.
        for r in range(rows):
            row = []
            
            for c in range(col):
                row.append(Cell())

            self._rows.append(row)

        # Place the first four discs. Do not use the place disc method.
        self._rows[math.floor(rows/2) - 1][math.floor(col/2) - 1].place_disc(top_left_center_disc)
        self._rows[math.floor(rows/2)][math.floor(col/2)].place_disc(top_left_center_disc)
        self._rows[math.floor(rows/2)][math.floor(col/2) - 1].place_disc(top_left_center_disc * -1)
        self._rows[math.floor(rows/2) - 1][math.floor(col/2)].place_disc(top_left_center_disc * -1)        

    def get_rows_of_cells(self) -> [["Cell"]]:
        '''
        Returns the rows of the gameboard's cells.
        '''
        return self._rows
            
    def to_string(self) -> str:
        '''
        Gives a string resembling the game board.
        '''
        gameboard_as_str = ""

        for row in self._rows:
            for cell in row:
                gameboard_as_str += cell.to_string() + " "

            gameboard_as_str += "\n"

        return gameboard_as_str[:-1]

    def is_full(self) -> bool:
        '''
        Returns whether or not every cell in the GameBoard is full.
        '''
        for row in self._rows:
            for cell in row:
                if cell.cell_content() == EMPTY:
                    return False

        return True

    def no_of_white_discs(self):
        '''
        Returns the number of white discs.
        '''
        return self._white_discs.get_count()

    def no_of_black_discs(self):
        '''
        Returns the number of black discs.
        '''
        return self._black_discs.get_count()

    def no_of_rows(self):
        '''
        Returns the gameboard's number of rows.
        '''
        return self._no_of_rows

    def no_of_col(self):
        '''
        Returns the gameboard's number of columns.
        '''
        return self._no_of_col     

    def no_moves(self, color: int) -> bool:
        '''
        See if there are no valid moves on the board
        for a particular color.
        '''
        for row_index in range(self._no_of_rows):
            for cell_index in range(self._no_of_col):
                if self.valid_move(row_index, cell_index, color):                    
                    return False

        return True
                
    def valid_move(self, row_index: int, col_index: int, color: int) -> bool:
        '''
        Placing a disc is valid only if it will flip a series of
        bounded discs in at least one direction AND only if the cell is
        empty.
        '''
        if self._rows[row_index][col_index].cell_content() == EMPTY:
            bounded_discs_exist = []

            # Make a list of whether or not the prospective
            # move would flip a series of discs in each given
            # direction.
            for neighbor_funct in self.neighbor_functions:
                try:
                    cells_of_flippable_discs = self._cells_of_bounded_discs(color, neighbor_funct,
                                                                            row_index, col_index)
                except InvalidMoveError:
                    bounded_discs_exist.append(False)
                except IndexError:
                    bounded_discs_exist.append(False)
                else:
                    if cells_of_flippable_discs == []:
                        bounded_discs_exist.append(False)
                    else:
                        bounded_discs_exist.append(True)

            # See if the prospective move would flip any
            # bounded discs.
            if True in bounded_discs_exist:
                return True
            else:
                return False
        else:
            return False

    def place_disc(self, row_index: int, col_index: int, color: int) -> None:
        '''
        Places a disc at the specified cell. The disc color is
        indicated by a number. If the number does not specify a
        defined disc color (black or white), then this function
        will catch that. Once a disc is placed, bounded discs
        will be flipped.
        '''
        if(color == BLACK):
            self._rows[row_index][col_index].place_disc(color)
            self._black_discs.increment()
        elif(color == WHITE):
            self._rows[row_index][col_index].place_disc(color)
            self._white_discs.increment()
        else:
            raise InvalidDiscColor

        self._flip_bounded_discs(color, row_index, col_index)

    def _flip_bounded_discs(self, color: int,
                           row_index: int, col_index: int) -> None:
        '''
        Flips the discs bounded between the one assumed to be placed at a given
        position and a corresponding one in any direction. If there are no
        bounded discs, then nothing will be flipped.
        '''
        series_of_cells_with_discs = []
        
        for neighbor_funct in self.neighbor_functions:
            try:
                series_of_cells_with_discs.append(self._cells_of_bounded_discs(color,
                                        neighbor_funct, row_index, col_index))

            # The following errors are expected to possibly arise.
            # Nothing needs to be done about those.
            except IndexError:
                pass
            except InvalidMoveError:
                pass

        for cells_of_discs_to_flip in series_of_cells_with_discs:            
            for cell in cells_of_discs_to_flip:
                cell.switch_cell_disc_color()

                if color == WHITE:
                    self._white_discs.increment()
                    self._black_discs.decrement()
                elif color == BLACK:
                    self._black_discs.increment()
                    self._white_discs.decrement()
                else:
                    raise InvalidDiscColor
        
    def _cells_of_bounded_discs(self, color: int, neighbor_formula: "Function",
                                row_index: int, col_index: int) -> ["Cell"]:
        '''
        This takes a disc color the user wants to place at the given position.
        It then returns a list of the discs of the opposite color which
        would be bounded between the disc at this position and a corresponding
        disc in the given direction. There may be zero bounded discs. If there
        is not corresponding disc in the given direction, there will be either and
        IndexError or and InvalidMoveError.
        '''
        cells_with_discs = []       # Bounded discs we have found thus far
        neighbor_row_index, neighbor_col_index = neighbor_formula(row_index, col_index)     # Neighboring cell's address

        # For our purposes, there should be no negative indices.
        # Python will not catch that, so we need to raise an IndexError
        # if an index is negative.
        if neighbor_row_index < 0 or neighbor_col_index < 0:
            raise IndexError
        
        neighboring_cell = self._rows[neighbor_row_index][neighbor_col_index]   # Neighboring cell

        # If the next cell's disc's color is the opposite of our
        # original disc color, the cell has one of the bounded discs.
        if neighboring_cell.cell_content() == color*-1:            
            cells_with_discs.append(neighboring_cell)

            # Go on to see if the next cell in the same direction
            # also has a bounded disc.
            cells_with_discs += self._cells_of_bounded_discs(color, neighbor_formula, neighbor_row_index, neighbor_col_index)

            return cells_with_discs
        
        elif neighboring_cell.cell_content() == color:
            # When we reach a disc of the color matching our
            # original, we have reached the end of the series
            # of bounded discs.
            return []
        
        else:
            # If we reach something other than a bounded disc
            # or the end of our bounded disc series, then
            # there are not really any bounded discs. In that
            # case, we have made an invalid move.
            raise InvalidMoveError        

    # The following functions give the addresses of cells
    # neighboring a particular cell.
    def _north_cell(row: int, col: int) -> (int):
        return (row-1, col)

    def _south_cell(row: int, col: int) -> (int):
        return (row+1, col)

    def _east_cell(row: int, col: int) -> (int):
        return (row, col+1)

    def _west_cell(row: int, col: int) -> (int):
        return (row, col-1)

    def _northeast_cell(row: int, col: int) -> (int):
        return (row-1, col+1)

    def _northwest_cell(row: int, col: int) -> (int):
        return (row-1, col-1)   

    def _southeast_cell(row: int, col: int) -> (int):
        return (row+1, col+1)

    def _southwest_cell(row: int, col: int) -> (int):
        return (row+1, col-1)    
        

class Cell:
    '''
    This represents a cell or square on a game board.
    '''
    def __init__(self) -> None:
        self._cell_state = EMPTY

    def to_string(self) -> str:
        '''
        Give a string resembling the contents of the cell.
        '''
        if self._cell_state == EMPTY:
            return '.'
        elif self._cell_state == BLACK:
            return 'B'
        elif self._cell_state == WHITE:
            return 'W'
        else:
            raise InvalidCellContents

    def cell_content(self) -> int:
        '''
        Gives back the contents of the cell.
        '''
        return self._cell_state

    def switch_cell_disc_color(self) -> None:
        '''
        Switches the color of the discs in this cell.
        Raises an error if the cell is empty or has
        invalid contents.
        '''
        if self._cell_state == BLACK:
            self._cell_state = WHITE            
        elif self._cell_state == WHITE:
            self._cell_state = BLACK            
        elif self._cell_state == EMPTY:
            raise InvalidMoveError
        else:
            raise InvalidCellContents

    def place_disc(self, color: int) -> None:
        '''
        Assigns a cell the number of a disc color,
        thus, placing a disc in the cell. It will assign
        a disc color number only if the cell empty.
        '''
        if color == BLACK and self._cell_state == EMPTY:
            self._cell_state = BLACK
        elif color == WHITE and self._cell_state == EMPTY:
            self._cell_state = WHITE            
        else:
            raise InvalidMoveError


class Counter:
    def __init__(self, start: int) -> None:
        self._count = start

    def increment(self) -> None:
        self._count += 1

    def decrement(self) -> None:
        self._count -= 1

    def get_count(self) -> int:
        return self._count


