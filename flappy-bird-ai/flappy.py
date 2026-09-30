# Flappy Bird AI that teaches itself (neuroevolution)
import math
import random
import pygame

W, H, BIRD_X, R = 800, 800, 200, 16
GAP, PIPE_W, SPACING, SPEED = 220, 90, 340, 5
POP, KEEP, HIDDEN, INPUTS = 50, 5, 6, 5
YELLOW, DEAD = (255, 214, 10), (120, 50, 70)
GREEN = (40, 170, 130)


class Brain:
    def __init__(self, rng, w=None):
        n = HIDDEN * INPUTS + HIDDEN
        self.w = w or [rng.gauss(0, 1) for _ in range(n)]

    def flap(self, seen):
        outs = self.w[HIDDEN * INPUTS:]
        total = 0
        for h in range(HIDDEN):
            row = self.w[h * INPUTS:(h + 1) * INPUTS]
            s = sum(x * w for x, w in zip(seen, row))
            total += math.tanh(s) * outs[h]
        return total > 0

    def child(self, rng):
        # copy the parent, randomly nudge some weights
        w = list(self.w)
        for i in range(len(w)):
            if rng.random() < 0.2:
                w[i] += rng.gauss(0, 0.4)
        return Brain(rng, w)


class Bird:
    def __init__(self, brain):
        self.brain = brain
        self.x, self.y, self.vy = BIRD_X, H / 2, 0
        self.alive, self.fitness = True, 0


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.gen = 0
        brains = [Brain(self.rng) for _ in range(POP)]
        self.new_generation(brains)

    def new_generation(self, brains):
        self.gen += 1
        self.score = 0
        self.birds = [Bird(b) for b in brains]
        self.pipes = [[W + i * SPACING, self.gap()]
                      for i in range(3)]

    def gap(self):
        return self.rng.randint(170, H - 170)

    def step(self):
        # the next pipe we haven't flown past yet
        pipe = next(p for p in self.pipes
                    if p[0] + PIPE_W > BIRD_X - R)
        top, bottom = pipe[1] - GAP / 2, pipe[1] + GAP / 2
        for b in self.birds:
            if not b.alive:
                b.x -= SPEED
                continue
            seen = [b.y / H,                # height
                    b.vy / 10,              # speed
                    (pipe[0] - BIRD_X) / W, # distance
                    (pipe[1] - b.y) / H,    # gap
                    1]
            if b.brain.flap(seen):
                b.vy = -9
            b.vy = min(b.vy + 0.8, 12)
            b.y += b.vy
            b.fitness += 1
            in_pipe = -R < BIRD_X - pipe[0] < PIPE_W + R
            safe = top + R < b.y < bottom - R
            if (in_pipe and not safe) or not 0 < b.y < H:
                b.alive = False
        for p in self.pipes:
            p[0] -= SPEED
            edge = p[0] + PIPE_W
            if edge < BIRD_X <= edge + SPEED:
                self.score += 1
        if self.pipes[0][0] + PIPE_W < 0:
            self.pipes.pop(0)
            x = self.pipes[-1][0] + SPACING
            self.pipes.append([x, self.gap()])
        if not any(b.alive for b in self.birds):
            self.evolve()

    def evolve(self):
        # the birds that flew furthest become the parents
        ranked = sorted(self.birds, reverse=True,
                        key=lambda b: b.fitness)
        parents = [b.brain for b in ranked[:KEEP]]
        kids = [self.rng.choice(parents).child(self.rng)
                for _ in range(POP - KEEP)]
        self.new_generation(parents + kids)

    def draw(self, screen):
        screen.fill((13, 17, 23))
        for x, gy in self.pipes:
            top, bottom = gy - GAP // 2, gy + GAP // 2
            for y0, y1 in ((-20, top), (bottom, H + 20)):
                pygame.draw.rect(screen, GREEN,
                                 (x, y0, PIPE_W, y1 - y0),
                                 border_radius=12)
        for b in reversed(self.birds):  # parents on top
            if b.x > -R:
                color = YELLOW if b.alive else DEAD
                x, y = b.x, b.y
                pygame.draw.circle(screen, color, (x, y), R)
                eye = (x + 6, y - 6)
                pygame.draw.circle(screen, "white", eye, 6)
                pygame.draw.circle(screen, "black", eye, 3)
                beak = [(x + 12, y), (x + 26, y + 4),
                        (x + 12, y + 8)]
                pygame.draw.polygon(screen, "orange", beak)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        game.step()
        game.draw(screen)
        caption = f"Gen {game.gen}  Score {game.score}"
        pygame.display.set_caption(caption)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
