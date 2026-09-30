# Code Plays Itself

Source code for the games and AIs from the **Code Plays Itself** YouTube channel.
Every project is a single Python file you can run and change yourself.

| Project | What it does | Folder |
|---|---|---|
| 🐍 Snake that never loses | Follows a loop through every cell and takes safe shortcuts. It always wins. | [`snake-perfect-game`](snake-perfect-game) |
| 🐦 Flappy Bird AI | 50 birds with tiny neural networks evolve until they can play. | [`flappy-bird-ai`](flappy-bird-ai) |
| 👻 Ghost pathfinding | A ghost that always finds you, using BFS, Dijkstra and A*. | [`ghost-pathfinding`](ghost-pathfinding) |

## Run any project

You need [Python 3](https://www.python.org/downloads/). Then:

```bash
pip install -r requirements.txt
cd flappy-bird-ai
python flappy.py
```

Swap in another folder name and file to run a different project.

## Try changing things

Every folder's README ends with a few challenges. Break things, see what happens,
and tell me in the comments what you found.

## License

MIT: use it, learn from it, build on it.
