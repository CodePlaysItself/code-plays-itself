# 👻 A ghost that always finds you: BFS, Dijkstra and A*

A Pac-Man style maze where a ghost hunts the player using A* pathfinding.
The file also contains breadth-first search and Dijkstra, so you can compare all three.

```bash
pip install pygame
python ghost.py
```

The window title counts how many times the ghost has caught the player.

## How it works

- **The maze (`make_maze`)**: a grid where each cell is a number, the cost of stepping on it:
  `0` = wall, `1` = floor, `5` = mud. It's carved by walking randomly and backtracking,
  then some walls are knocked out to make loops, and mud is sprinkled in.
- **Breadth-first search (`bfs`)**: explores outward in rings using a queue. It finds the path
  with the *fewest steps*, but ignores cost, so it walks straight through mud.
- **Dijkstra (`astar(..., use_guess=False)`)**: explores the *cheapest* cell first using a heap,
  so it walks around the mud.
- **A\* (`astar`)**: like Dijkstra, but every cell's score is *cost so far + a guess* of the
  distance left (as if there were no walls). It heads straight for the goal and explores far
  fewer cells, but still finds the cheapest path, because the guess never overestimates.
- **The chase (`Game.step`)**: every frame the ghost re-runs A* to the player's current
  position and takes one step. The player flees to random far-away spots using BFS.

## Challenges

- Give the player A* too. Can it escape?
- Add a second ghost.
- Allow diagonal moves (you'll need a different `guess`).
- Make the ghost aim for where the player is *going*, not where it is.
- Multiply the guess by 5 in `astar`. It gets faster, but does it still find the cheapest path?
