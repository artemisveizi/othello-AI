import pickle
import strategy7_aveizi
from strategy7_aveizi import my_strategy
#from strategy7_jcai import my_strat
import time

B_STRATEGY = Strategy.alpha_beta
W_STRATEGY = strategy7_aveizi.human
ROUNDS = 1
SILENT = True

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

# see core.py for constants: MAX, MIN, TIE

def play(strategy_b, strategy_w, first = BLACK, silent=True):
    strategy = my_strategy()
    #jstrat = my_strat()
    board = strategy.initial_board()
    player = first
    current_strategy = {BLACK: strategy_b, WHITE: strategy_w}
    print("BLACK (@): RANDOM. WHITE (O): ALPHA-BETA")
    #print(strategy.print_board(board))
    while player is not None:
        if player == WHITE:
            move = strategy.alpha_beta(player, board, 1000000000, -1000000000, 2)
        if player == BLACK:
            move = strategy.alpha_beta(player, board, -1000000000, 1000000000, 2)
            #move = strategy7_aveizi.random(player, board)
        board = strategy.make_move(move, player, board)
        #print(strategy.print_board(board))
        player = strategy.next_player(board, player)
    print(strategy.print_board(board))
    sc = strategy.score(BLACK, board)
    win = "TIE"
    if sc > 0: 
        win = "BLACK"
    elif sc < 0: 
        win = "WHITE" 
    print(win + " wins!")
    return board, sc # returns "X" "O" or "TIE"

def main():
    #j = []
    #for i in range(ROUNDS):
    #    try:
    #        game_result = play(X_STRATEGY, O_STRATEGY,
    #                      first=random.choice([MAX, MIN]),
    #                      silent=SILENT)
    #        j.append(game_result)
    #        print("Winner: ", game_result)
    #    except IllegalMoveError as e:
    #        print(e)
    #        j.append("FORFEIT")
    #print("\nResults\n" + "%4s %4s %4s" % ("X", "O", "-"))
    #print("-" * 15)
    #print("%4i %4i %4i" % (j.count(MAX), j.count(MIN), j.count(TIE)))
    for i in range(10):
        play(B_STRATEGY, W_STRATEGY)

start_time = time.time()
main()
end_time = time.time()
print("" + str(end_time - start_time))
