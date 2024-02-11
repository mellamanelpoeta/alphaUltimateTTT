# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/Python implementation/UltimateTicTacToe.ipynb.

# %% auto 0
__all__ = ['UltimateTicTacToe', 'utttError']

# %% ../nbs/Python implementation/UltimateTicTacToe.ipynb 3
#Copyright 2024 Gerardo Guerrero

from .constants import *
from .Move import *

class UltimateTicTacToe:
    def __init__(self,
                state:list() = None): #If no state is given, it generates a new one. 
        '''The state is a list of 93 elements. \n
        The first 81 elements are the state of each square, 0 for empty, 1 for X and 2 for O. \n
        The next 9 elements are the result of each subgame: 0 while being played, 1 is win for X, 2 is a win for O and 3 for draw.\n 
        The next element is the next symbol to play: 1 for X and 2 for O.\n 
        The next element is the index of the subgame that is constrained, 9 for no subgame constraint. \n
        The last element is the result of the UTTT: 0 while being played, 1 is win for X, 2 is a win for O and 3 for draw.'''
        if state:
            self.state = state
        else:
            self.state = [0] * SIZE
            self.state[NEXT_SYMBOL_INDEX] = X_STATE_VALUE #X always starts the game
            self.state[CONSTRAINT_INDEX] = UNCONSTRAINED_STATE_VALUE #no subgame is constrained at the beginning


    @property
    def result(self) -> int:
        return self.state[RESULT_INDEX]
    
    @property
    def next_symbol(self) -> int:
        return self.state[NEXT_SYMBOL_INDEX]
    
    @property
    def constraint(self) -> int:
        return self.state[CONSTRAINT_INDEX]

    def is_game_over(self) -> bool:
        '''Returns True if the game is over, False otherwise.'''
        return bool(self.state[RESULT_INDEX])
    
    def is_constrained(self) -> bool:
        '''Returns True if a subgame is constrained, False otherwise.'''
        return self.state[CONSTRAINT_INDEX] != UNCONSTRAINED_STATE_VALUE
      
    def _verify_move(self, 
                     move: Move): #Verifies if the move is valid.
        '''Verifies if the move is valid: if the index is in the valid range, 
        if the subgame is not over, if the index is not already taken and if the subgame is not constrained.
          If it is not, it raises an exception.'''
        illegal_move = f"Illegal move {move} - "
        if not (0 <= move.index < 81):
            raise utttError(illegal_move + "index outside the valid range")
        if self.is_constrained() and self.constraint != move.index // 9:
            raise utttError(illegal_move + f"violated constraint = {self.constraint}")
        if self.state[81 + move.index // 9]:
            raise utttError(illegal_move + "index from terminated subgame")
        if self.state[move.index]:
            raise utttError(illegal_move + "index already taken")
        
    def _get_subgame_result(self,
                            subgame_index: int) -> int:   #Index of the subgame from 0 to 8
        '''Returns the result of the subgame.''' 
        return self.state[81 + subgame_index]
        
    def _update_state(self,
                      move: Move): #Updates the state of the game after a move.
        '''Updates the state of the game after a move. It also verifies if the subgame and the game are over.'''
        self.state[move.index] = move.symbol
        self.state[NEXT_SYMBOL_INDEX] = X_STATE_VALUE + O_STATE_VALUE - move.symbol

        self._verify_subgame_result(move)
        self._verify_game_result(move)

        if not self.is_game_over():
            #Check if the subgame on index move.index % 9 is still being played. If it is, constraint to it. Else, unconstrain the game.
            subgame_index = move.index % 9
            if not self._get_subgame_result(subgame_index):
                self.state[CONSTRAINT_INDEX] = subgame_index
            else:
                self.state[CONSTRAINT_INDEX] = UNCONSTRAINED_STATE_VALUE

    def _make_move(self,
                move: Move, #Receives a move and updates the state of the game.
                verify: bool = True): #A boolean to verify if the move is valid.
        '''Makes a move in the game. It verifies if the move is valid'''
        if verify:
            if self.is_game_over():
                raise utttError("Illegal move " + str(move) + ' - The game is over')
            self._verify_move(move)

        self._update_state(move)
        self._verify_game_result(move)
        if self.is_game_over():
            print('The game is over')
            if self.state[RESULT_INDEX] == DRAW_STATE_VALUE:
                print('The game is a draw')
            elif self.state[RESULT_INDEX] == X_STATE_VALUE:
                print('X is the winner')
            else:
                print('O is the winner')

    def is_winning_position(self,
                            game:list) -> bool: #Receives a list of 9 elements and returns True if it is a winning position, False otherwise.
        '''Returns True if the game is a winning position, False otherwise.'''
        return game[0] == game[1] == game[2] != 0 or game[3] == game[4] == game[5] != 0 or game[6] == game[7] == game[8] != 0 or game[0] == game[3] == game[6] != 0 or game[1] == game[4] == game[7] != 0 or game[2] == game[5] == game[8] != 0 or game[0] == game[4] == game[8] != 0 or game[2] == game[4] == game[6] != 0

    def is_drawn_position(self,
                          game:list) -> bool: #Receives a list of 9 elements and returns True if it is a drawn position, False otherwise.
        '''Returns True if the game is a drawn position, False otherwise.'''
        return 0 not in game
    
    def _verify_subgame_result(self, move):
        '''Verifies if the subgame is over and updates the state of the subgame.'''
        subgame_index = move.index // 9
        subgame = self.state[subgame_index * 9 : subgame_index * 9 + 9]
        if self.is_winning_position(subgame):
            self.state[81 + subgame_index] = move.symbol
        elif self.is_drawn_position(subgame):
            self.state[81 + subgame_index] = DRAW_STATE_VALUE
    
    def _verify_game_result(self,move):
        '''Verifies if the game is over and updates the state of the game.'''
        symbol = move.symbol
        game = self.state[81:90]
        if self.is_winning_position(game):
            self.state[RESULT_INDEX] = symbol
        elif self.is_drawn_position(game):
            self.state[RESULT_INDEX] = DRAW_STATE_VALUE
    
    def _get_legal_indexes(self) -> list:
        '''Returns a list with the indexes of the legal moves.'''
        if not self.is_constrained():
            ## If the game is not constrained, all the empty squares are legal moves, except the ones from subgames that are already over.
            legal = []
            for subgame_index in range(9):
                if not self._get_subgame_result(subgame_index):
                    for i in range(subgame_index * 9, subgame_index * 9 + 9):
                        if not self.state[i]:
                            legal.append(i)
            return legal
        else:
            subgame_index = self.state[CONSTRAINT_INDEX]
            return [i for i in range(subgame_index * 9, subgame_index * 9 + 9) if not self.state[i]]

    def __str__(self):
        state_values_map = {
            X_STATE_VALUE: 'X',
            O_STATE_VALUE: 'O',
            DRAW_STATE_VALUE: '=',
            0: '·',
        }

        subgames = [state_values_map[s] for s in self.state[:81]]
        supergame = [state_values_map[s] for s in self.state[81:90]]

        if not self.is_game_over():
            legal_indexes = self._get_legal_indexes()
            for legal_index in legal_indexes:
                subgames[legal_index] = '•'

            if self.is_constrained():
                supergame[self.constraint] = '•'
            elif self.constraint == UNCONSTRAINED_STATE_VALUE:
                supergame = ['•' if s == '·' else s for s in supergame]

        sb = lambda l, r: ' '.join(subgames[l : r + 1])
        sp = lambda l, r: ' '.join(supergame[l : r + 1])

        subgames_str = [
            '    1 2 3   4 5 6   7 8 9',
            '  1 ' + sb(0, 2)   + ' │ ' + sb(9, 11) +  ' │ ' + sb(18, 20),
            '  2 ' + sb(3, 5)   + ' │ ' + sb(12, 14) + ' │ ' + sb(21, 23),
            '  3 ' + sb(6, 8)   + ' │ ' + sb(15, 17) + ' │ ' + sb(24, 26),
            '    ' + '—' * 21,
            '  4 ' + sb(27, 29) + ' │ ' + sb(36, 38) + ' │ ' + sb(45, 47),
            '  5 ' + sb(30, 32) + ' │ ' + sb(39, 41) + ' │ ' + sb(48, 50),
            '  6 ' + sb(33, 35) + ' │ ' + sb(42, 44) + ' │ ' + sb(51, 53),
            '    ' + '—' * 21,
            '  7 ' + sb(54, 56) + ' │ ' + sb(63, 65) + ' │ ' + sb(72, 74),
            '  8 ' + sb(57, 59) + ' │ ' + sb(66, 68) + ' │ ' + sb(75, 77),
            '  9 ' + sb(60, 62) + ' │ ' + sb(69, 71) + ' │ ' + sb(78, 80),
        ]

        supergame_str = [
            '  ' + sp(0, 2),
            '  ' + sp(3, 5),
            '  ' + sp(6, 8),
        ]

        subgames_str = '\n'.join(subgames_str)
        supergame_str = '\n'.join(supergame_str)

        next_symbol = state_values_map[self.next_symbol]
        constraint = 'None' if self.constraint == UNCONSTRAINED_STATE_VALUE else str(self.constraint+1)
        result = 'In Game'
        if self.result == X_STATE_VALUE:
            result = 'X won'
        elif self.result == O_STATE_VALUE:
            result = 'O won'
        elif self.result == DRAW_STATE_VALUE:
            result = 'Draw'

        output = f'{self.__class__.__name__}(\n'
        output += f'  subgames:\n{subgames_str}\n'
        if not self.is_game_over():
            output += f'  next player: {next_symbol}\n'
            output += f'  constraint: {constraint}\n'
        output += f'  supergame:\n{supergame_str}\n'
        output += f'  result: {result}\n)'
        return output
    
    def map_matrix_to_subgame(self, matrix_index: int) -> int:
        digit_1 = matrix_index // 10 
        digit_2 = matrix_index % 10
        subgame_index = MAPPING[(digit_1, digit_2)]
        return subgame_index

    def play(self, matrix_index: int):
        '''Plays the game. Receives a matrix index and makes a move in the corresponding state index.'''
        index = self.map_matrix_to_subgame(matrix_index)
        self._make_move(Move(self.next_symbol, index))
        print(self)


# %% ../nbs/Python implementation/UltimateTicTacToe.ipynb 11
class utttError(Exception):
    pass
