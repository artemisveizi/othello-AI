from othello_core import OthelloCore
from random import randint
import time
from multiprocessing import Process, Value
time_limit = 5

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

class Strategy(OthelloCore):
    def is_valid(self, move):
        """Is move a square on the board?"""
        return move != OUTER

    def opponent(self, player):
        """Get player's opponent piece."""
        return WHITE if player is BLACK else BLACK

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists. TO PLAYER OR SPACE
        Returns the index of the bracketing square if found
        """
        notAdjacent = False
        current_square = square + direction
        while self.is_valid(current_square):
            if board[current_square] == EMPTY or board[current_square] == OUTER:
                return None
            if board[current_square] == self.opponent(player):
                current_square = current_square + direction
                notAdjacent = True
            if board[current_square] == player and notAdjacent:
                return square
            if board[current_square] == player and not notAdjacent:
                return None
        return None
            

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        for i in DIRECTIONS:
            if self.find_bracket(move, player, board, i) != None:
                return True

    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        b = list(board)
        for i in DIRECTIONS:
            if self.find_bracket(move, player, b, i) != None:
                self.make_flips(move, player, b, i)
        return b

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        board[move] = player
        current_square = move + direction
        while board[current_square] != player:
            board[current_square] = player
            current_square = current_square + direction

    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        legal = []
        for i in range(11, 89):
            move = i
            if board[move] == EMPTY:
                 if self.is_legal(move, player, board):
                     legal.append(move)
        return legal

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
        return len(self.legal_moves(player, board)) != 0

    def next_player(self,board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        o = self.opponent(prev_player)
        if self.any_legal_move(o, board):
                return o
        elif self.any_legal_move(prev_player, board):
                return prev_player
        return None

    def t_t(self, player, board):
        e = self.score(player,board)
        if e > 0:
            return sum(map(abs, SQUARE_WEIGHTS))
        elif e < 0:
            return -sum(map(abs, SQUARE_WEIGHTS))
        return e
    def weight_eval(self, player, board):
        """
        Compute the difference between the sum of the weights of player's
        squares and the sum of the weights of opponent's squares.
        """
        o = self.opponent(player)
        eval = 0
        for s in self.squares():
            if board[s] == player:
                eval += SQUARE_WEIGHTS[s]
            elif board[s] == o:
                eval -= SQUARE_WEIGHTS[s]
        return eval

    def minimax_strategy(max_depth):
        """ Takes a max_depth parameter and returns a new function/closure for strategy """
        def strategy(board, player):
            return minimax(board, player)
        return strategy

    def minimax(board, player):
        if player == BLACK: return max_dfs(board, player, 0)[1]
        if player == WHITE: return min_dfs(board, player, 0)[1]

    def game_over(self, player, board):
        score = self.score(player, board)
        if score < 0:
            return -inf
        elif score > 0:
            return inf
        return score

    """    
    def max_dfs(self, board, player, current_d):
        if current_d == 0:
            return self.weight_eval(player, board), None
        moves = self.legal_moves(player, board)
        if len(moves) == 0:
            if not self.any_legal_move(self.opponent(player), board):
                return self.game_over(player, board), None
            return self.min_dfs(board, player, current_d + 1), None
        return max(self.min_dfs((self.make_move(m, player, board) for m in moves), self.opponent(player), current_d + 1)), None

    def min_dfs(self, board, player, current_d, eval):
        if current_d == 0:
            return self.weight_eval(player, board), None
        moves = self.legal_moves(player, board)
        if len(moves) == 0:
            if not self.any_legal_move(self.opponent(player), board):
                return self.game_over(player, board), None
            return self.max_dfs(board, player, current_d + 1), None
        return min(self.max_dfs((self.make_move(m, player, board) for m in moves), self.opponent(player), current_d + 1)), None
    """
    def best_strategy(self, board, player, best_move, still_running):
        """
        :param board: a length 100 list representing the board state
        :param player: WHITE or BLACK
        :param best_move: shared multiptocessing.Value containing an int of
                the current best move
        :param still_running: shared multiprocessing.Value containing an int
                that is 0 iff the parent process intends to kill this process
        :return: best move as an int in [11,88] or possibly 0 for 'unknown'
        """
        depth = 1
        best_move = 0
        while still_running > 0:
            best_move.value = self.alpha_beta(player, board, -1000000, 1000000, depth)
            depth += 1
        return best_move

    def alpha_beta(self, player, board, alpha, beta, depth):
        if depth == 0:
            return self.weight_eval(player, board)
        moves = self.legal_moves(player, board)
        if not moves:
            if not self.any_legal_move(self.opponent(player), board):
                return self.t_t(player, board)
            return -(self.alpha_beta(self.opponent(player), board, -beta, -alpha, depth-1))
        best_move = moves[0]
        for move in moves:
            if alpha >= beta:
                break
            new_board = self.make_move(move, player,board)
            val = -(self.alpha_beta(self.opponent(player), new_board, -beta, -alpha, depth-1))
            if val > alpha:
                alpha = val
                best_move = move
            if val == alpha:
                if randint(0, 1) == 0:
                    alpha = val
                    best_move = move
        return best_move

    def ab_complete(depth, evaluate, player, board):
        def strategy(player, board):
            return alpha_beta(player, board, -1000000, 10000000, depth, evaluate)[1]
        return strategy
        import os, signal
	
def random(player, board):
    strat = my_strategy()
    moves = strat.legal_moves(player, board)
    a = randint(0, len(moves)-1)
    return moves[a]

def human(player, board):
    move = -1
    while move not in range(11, 89):
        print('What is your next move? (rowcol)')
        s = input()
        row = int(s[0])
        col = int(s[1])
        move = (10 * row) + col
    return move

"""
A-B PSEUDOCODE
(* the minimax value of n, searched to depth d.
 * If the value is less than min, returns min.
 * If greater than max, returns max. *)
 fun minimax(n: node, d: int, min: int, max: int): int =
   if leaf(n) or depth=0 return evaluate(n)
   if n is a max node
      v := minSCORE
      for each child of n
         v' := minimax (child,d-1,v,max)
         if v' > v, v:= v'
         if v > max return max
      return v
   if n is a min node
      v := max
      for each child of n
         v' := minimax (child,d-1,min,v)
         if v' < v, v:= v'
         if v < min return min
      return v
"""
