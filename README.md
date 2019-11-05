# othello-AI
Optimized Othello player (python).

Searches solution tree efficiently and makes informed moves. Prioritizes corners and edge spots in the board over central spots, and has greater weight on moves that do not lend an advantage to the opponent in the short-term (i.e. bridging the step to the corners, giving the opponent the corner in the next move). Overall unconcerned with immediate improvement of number of pieces on the board, focuses on long term success above temporary indicators of future chances of winning.

I used alpha beta pruning with minimax and a scoring matrix. At first, I won against non-random opponent code the same way every time, so I decided to put in a randomized tiebreaker (when the weight eval of possible boards was the same with two different moves). I ran the alpha beta at max depth 3 for time efficiency, and the total time was 55 seconds for 10 games.

The alpha-beta search algorithm:
```
function AB-search(state) returns an action
  inputs: state, current state in game
  
  v = MAX-value(state, -inf, inf)
  return the action in SUCCESSORS(state) with value v
```
```
function MAX-value(state, A, B) returns a utility value
  inputs: state, current state in game
    A, the value of the best alternative for MAX along the path to state
    B, the value of the best alternative for MIN along the path to state
    
  if TERMINAL-CHECK(state) then return UTILITY(state)
  v = -inf
  for A, S in SUCCESSORS(state) do
    v = MAX(v, MIN-value(S, A, B))
    if v >= B then return v
    A = MAX(A, v)
  return v
```
```
function MIN-value(state, A, B) returns a utility value
  inputs: state, current state in game
    A, the value of the best alternative for MAX along the path to state
    B, the value of the best alternative for MIN along the path to state
    
  if TERMINAL-CHECK(state) then return UTILITY(state)
  v = inf
  for A, S in SUCCESSORS(state) do
    v = MIN(v, MAX-value(S, A, B))
    if v <= B then return v
    B = MIN(B, v)
  return v
```
Example game:</br>
```
BLACK (@): RANDOM. WHITE (O): ALPHA-BETA

  1 2 3 4 5 6 7 8
1 . . . . . . . .
2 . . . . . . . .
3 . . . . . . . .
4 . . . o @ . . .
5 . . . @ o . . .
6 . . . . . . . .
7 . . . . . . . .
8 . . . . . . . .

(Gameplay between random heuristic and a-b pruning heuristic. . .)

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o . o @
3 o o o o @ o @ o
4 @ @ @ @ o @ o o
5 o @ o o o o o o
6 . @ o @ o o . o
7 @ @ @ o . @ . .
8 o @ o . . o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o . o @
3 o o o o @ o @ o
4 @ @ @ @ o @ o o
5 o @ o o o o o o
6 . @ o o o o . o
7 @ @ @ o o @ . .
8 o @ o . . o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ o
4 @ @ @ @ o @ o o
5 o @ o o o o o o
6 . @ o o o o . o
7 @ @ @ o o @ . .
8 o @ o . . o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ o
4 @ @ @ @ o @ o o
5 o @ o o o o o o
6 . o o o o o . o
7 @ @ o o o @ . .
8 o @ o o . o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ o
4 @ @ @ @ @ @ o o
5 o @ o o @ o o o
6 . o @ o @ o . o
7 @ @ o @ @ @ . .
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ o
4 @ @ o @ @ @ o o
5 o o o o @ o o o
6 o o @ o @ o . o
7 o @ o @ @ @ . .
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ @
4 @ @ o @ @ @ o @
5 o o o o @ o o @
6 o o @ o @ o . @
7 o @ o @ @ @ . @
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o . o o o o . o
2 . o o o o @ @ @
3 o o o o @ @ @ @
4 @ @ o @ @ @ o @
5 o o o o @ o o @
6 o o @ o @ o . @
7 o @ o o o o o @
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o @ o o o o . o
2 . @ @ o o @ @ @
3 o @ o @ @ @ @ @
4 @ @ o @ @ @ o @
5 o o o o @ o o @
6 o o @ o @ o . @
7 o @ o o o o o @
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o @ o o o o o o
2 . @ @ o o o o @
3 o @ o @ o @ o @
4 @ @ o o @ @ o @
5 o o o o @ o o @
6 o o @ o @ o . @
7 o @ o o o o o @
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o @ o o o o o o
2 . @ @ o o o o @
3 o @ o @ o @ o @
4 @ @ o o @ @ o @
5 o o o o @ @ o @
6 o o @ o @ @ @ @
7 o @ o o o @ o @
8 o @ @ @ @ o o o

  1 2 3 4 5 6 7 8
1 o @ o o o o o o
2 o o o o o o o @
3 o o o @ o @ o @
4 @ @ o o @ @ o @
5 o o o o @ @ o @
6 o o @ o @ @ @ @
7 o @ o o o @ o @
8 o @ @ @ @ o o o

WHITE wins!
```
