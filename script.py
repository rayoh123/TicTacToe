import copy

class GameState:
    def __init__(self, board = None, turn = 'x'):
        if board == None:
            self._board = {
                'a': [None, None, None],
                'b': [None, None, None],
                'c': [None, None, None]
                }
        else:
            self._board = board
        self._col_order = ('a', 'b', 'c')
        self._num_rows = len(self._board['a'])
        self._num_cols = len(self._board)
        self.computer = 'x'
        self.human = 'o'
        self.player_turn = turn

    def __str__(self):
        string = ' -------\n'
        row = 2
        for _ in range(self._num_cols):
            string += str(row+1) + '|'
            for col in self._col_order:
                if self._board[col][row] != None: string += self._board[col][row] + '|'
                else                            : string += ' |'
            string += '\n -------\n'
            row -=1
        return string + '  a b c'

    def copy(self):
        return GameState(copy.deepcopy(self._board), self.player_turn)

    def make_move(self, player, move):
        if self._board[move[0]][int(move[1])-1] != None:
            raise AssertionError
        
        self._board[move[0]][int(move[1])-1] = player
        if player == self.computer:
            self.player_turn = self.human
        else:
            self.player_turn = self.computer
        return self

    def winner(self):
        if self._board['a'][0] == self._board['a'][1] == self._board['a'][2] != None or \
        self._board['a'][0] == self._board['b'][0] == self._board['c'][0] != None or    \
        self._board['a'][0] == self._board['b'][1] == self._board['c'][2] != None:
            return self._board['a'][0]

        elif self._board['b'][0] == self._board['b'][1] == self._board['b'][2] != None or \
        self._board['a'][1] == self._board['b'][1] == self._board['c'][1] != None:
            return self._board['b'][1]

        elif self._board['c'][0] == self._board['c'][1] == self._board['c'][2] != None or \
        self._board['a'][2] == self._board['b'][1] == self._board['c'][0] != None:
            return self._board['c'][0]

        elif self._board['a'][2] == self._board['b'][2] == self._board['c'][2] != None:
            return self._board['a'][2]

        elif len(self.all_possible_moves()) == 0:
            return 0

        return None

    def all_possible_moves(self):
        moves = set()
        for col, row in self._board.items():
            for i in range(len(row)):
                if row[i] == None:
                    moves.add('%s%d' % (col, i+1))
        return moves




def minimax(game_state: GameState, alpha: int, beta: int) -> str:
    def find_end(x: (str, tuple)) -> int:
        if type(x) == int:
            return x
        elif type(x[1]) == int:
            return x[1]
        else:
            return find_end(x[1])

    if game_state.winner() == 'x':
        return 1
    elif game_state.winner() == 'o':
        return -1
    elif game_state.winner() == 0:
        return 0
    elif game_state.winner() == None:

        turn = game_state.player_turn
        
        if turn == game_state.computer:
            max_val = -2
            for move in game_state.all_possible_moves():
                temp = (move, minimax(game_state.copy().make_move(turn, move), alpha, beta))
                max_val = max(max_val, temp, key=find_end)
                alpha = max(alpha, max_val, key=find_end)
                if find_end(beta) <= find_end(alpha):
                    break
            return max_val
        else:
            min_val = 2
            for move in game_state.all_possible_moves():
                temp = ((move, minimax(game_state.copy().make_move(turn, move), alpha, beta)))
                min_val = min(min_val, temp, key=find_end)
                beta = min(alpha, min_val, key=find_end)
                if find_end(beta) <= find_end(alpha):
                    break
            return min_val


if __name__ == "__main__":
    a = GameState()
    print("The computer is 'x'. You are 'o'. Please wait several seconds as the computer calculates its first move.....")
    while a.winner() == None:
        move = minimax(a, -2, 2)[0]
        a.make_move('x', move)
        print(a)
        if a.winner() != None:
            break

        user_move = input("It's your turn. Make a move, for example 'a1', or 'c3': ")
        while True:
            try:
                a.make_move('o', user_move)
                break
            except AssertionError:
                user_move = input("That's illegal. It's your turn. Make a move, for example 'a1', or 'c3': ")
                

    if a.winner() not in (0, None):
        print(str(a.winner()) + ' has won')
    elif a.winner() == 0:
        print("Tie")
