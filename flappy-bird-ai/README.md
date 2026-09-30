# 🐦 Flappy Bird AI (neural network + evolution)

50 birds start with random brains and learn to play Flappy Bird by themselves.
No machine learning libraries, just Python and pygame.

```bash
pip install pygame
python flappy.py
```

The window title shows the current generation and score. It usually takes a few to
a few dozen generations before a bird gets really good.

## How it works

**The brain (`Brain.flap`)** is a tiny neural network:

- 4 inputs: the bird's height, its speed, the distance to the next pipe, and where the gap is (plus a constant 1, the *bias*).
- 6 hidden neurons: each multiplies the inputs by its weights, adds them up and squashes the result with `tanh`.
- 1 output: the hidden values are weighted and added. If the total is above 0, **flap**.

That's 36 numbers (weights) in total. The weights *are* the brain.

**Evolution (`Game.evolve`)** finds good weights:

1. When every bird is dead, rank them by fitness (how many frames they survived).
2. The best 5 become parents and are kept unchanged (*elitism*).
3. The other 45 are children: a copy of a random parent, where each weight has a
   20% chance of a small random nudge (a *mutation*).
4. Repeat.

## Challenges

- Keep only 1 parent (`KEEP = 1`). Does it learn faster or slower?
- Make mutations bigger: change `rng.gauss(0, 0.4)` to `rng.gauss(0, 1.0)`.
- Change the number of hidden neurons (`HIDDEN`).
- Give the bird a new input, like the height of the pipe after next (remember to update `INPUTS`).
