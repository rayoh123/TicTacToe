import copy

class GameState:
    def __init__(self, board = None, turn = 'x'):
        if board == None:
            self.board = {
                'a': [None, None, None],
                'b': [None, None, None],
                'c': [None, None, None]
                }
        else:
            self.board = board
        self._col_order = ('a', 'b', 'c')
        self._num_rows = len(self.board['a'])
        self._num_cols = len(self.board)
        self.computer = 'x'
        self.human = 'o'
        self.player_turn = turn

    def __str__(self):
        string = ' ------\n'
        row = 2
        for _ in range(self._num_cols):
            string += str(row+1) + '|'
            for col in self._col_order:
                if self.board[col][row] != None: string += self.board[col][row] + ' '
                else                            : string += '  '
            string += '\n'
            row -=1
        return string + ' ------\n  a b c'

    def copy(self):
        return GameState(copy.deepcopy(self.board), self.player_turn)

    def make_move(self, player, move):
        self.board[move[0]][int(move[1])-1] = player
        if player == self.computer:
            self.player_turn = self.human
        else:
            self.player_turn = self.computer
        return self

    def winner(self):
        if self.board['a'][0] == self.board['a'][1] == self.board['a'][2] != None or \
        self.board['a'][0] == self.board['b'][0] == self.board['c'][0] != None or    \
        self.board['a'][0] == self.board['b'][1] == self.board['c'][2] != None:
            return self.board['a'][0]

        elif self.board['b'][0] == self.board['b'][1] == self.board['b'][2] != None or \
        self.board['a'][1] == self.board['b'][1] == self.board['c'][1] != None:
            return self.board['b'][1]

        elif self.board['c'][0] == self.board['c'][1] == self.board['c'][2] != None or \
        self.board['a'][2] == self.board['b'][1] == self.board['c'][0] != None:
            return self.board['c'][0]

        elif self.board['a'][2] == self.board['b'][2] == self.board['c'][2] != None:
            return self.board['a'][2]

        elif len(self.all_possible_moves()) == 0:
            return 0

        return None

    def all_possible_moves(self):
        moves = set()
        for col, row in self.board.items():
            for i in range(len(row)):
                if row[i] == None:
                    moves.add('%s%d' % (col, i+1))
        return moves




def minimax(game_state: GameState) -> str:
    def find_end(x: (str, tuple)) -> int:
        if type(x[1]) == int:
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
            return max([(move, minimax(game_state.copy().make_move(turn, move))) for move in game_state.all_possible_moves()],
                      key = lambda x:find_end(x))
        else:
            return min([(move, minimax(game_state.copy().make_move(turn, move))) for move in game_state.all_possible_moves()],
                      key = lambda x:find_end(x))


if __name__ == "__main__":
    a = GameState()
    print("The computer is 'x'. You are 'o'. Please wait several seconds as the computer calculates its first move.....")
    while a.winner() == None:
        move = minimax(a)[0]
        a.make_move('x', move)
        print(a)
        if a.winner() not in (0, None):
            print(str(a.winner()) + ' has won')
            break
        elif a.winner() == 0:
            print("Tie")
            break
        user_move = input("It's your turn. Make a move, for example 'a1', or 'c3': ")
        a.make_move('o', user_move)
