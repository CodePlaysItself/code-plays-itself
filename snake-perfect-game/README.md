# 🐍 Snake that never loses

A Snake AI in about 100 lines of Python that fills the whole board (400/400) without ever crashing.

```bash
pip install pygame
python snake.py
```

## How it works

1. **The loop.** `build_cycle()` makes one zigzag path that visits every cell on the board
   and ends next to where it started (a *Hamiltonian cycle*).
2. **Always safe.** A snake that follows this loop can never crash. Its body is always
   *behind* the head along the loop.
3. **Shortcuts.** Following the loop is slow, so `choose()` jumps ahead toward the food, but only when the
   jump lands before the tail on the loop (`d < room`). That means it can never trap itself.
4. **Late game.** As the snake grows there's less room, the shortcuts stop, and it just
   follows the loop until every cell is filled.

## Challenges

- Make the board bigger (`H` must be an even number).
- Remove the `- 2` safety margin in `room`. Does it still always win?
- Count how many moves a full game takes, then try to make it faster.
