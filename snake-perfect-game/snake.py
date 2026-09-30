# Snake that plays itself (and never loses)
import random
import pygame

W, H, CELL = 20, 20, 40
N = W * H


def build_cycle():
    # zigzag through every cell, then back up column 0
    path = [(0, 0)]
    for y in range(H):
        xs = range(1, W) if y % 2 == 0 else range(W - 1, 0, -1)
        path += [(x, y) for x in xs]
    path += [(0, y) for y in range(H - 1, 0, -1)]
    return {cell: i for i, cell in enumerate(path)}


ORDER = build_cycle()
CELLS = sorted(ORDER, key=ORDER.get)


def ahead(a, b):
    # steps along the loop to get from a to b
    return (ORDER[b] - ORDER[a]) % N


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.snake = [CELLS[2], CELLS[1], CELLS[0]]
        self.won = False
        self.place_food()

    def place_food(self):
        free = [c for c in CELLS if c not in self.snake]
        if not free:
            self.won = True
            return
        self.food = self.rng.choice(free)

    def choose(self):
        head, tail = self.snake[0], self.snake[-1]
        room = ahead(head, tail) - 2
        goal = ahead(head, self.food)
        best, best_d = None, 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (head[0] + dx, head[1] + dy)
            if nxt not in ORDER or nxt in self.snake:
                continue
            d = ahead(head, nxt)
            # shortcut only if we can't trap our tail
            if best_d < d <= goal and d < room:
                best, best_d = nxt, d
        # no safe shortcut? just follow the loop
        return best or CELLS[(ORDER[head] + 1) % N]

    def step(self):
        if self.won:
            return
        nxt = self.choose()
        self.snake.insert(0, nxt)
        if nxt == self.food:
            self.place_food()
        else:
            self.snake.pop()

    def draw(self, screen):
        screen.fill((13, 17, 23))
        n = len(self.snake)
        for i, (x, y) in enumerate(self.snake):
            px, py = self.snake[max(i - 1, 0)]
            t = i / max(n - 1, 1)
            color = (40, int(230 - 130 * t), int(120 + 80 * t))
            r = pygame.Rect(
                min(x, px) * CELL + 5, min(y, py) * CELL + 5,
                (abs(x - px) + 1) * CELL - 10,
                (abs(y - py) + 1) * CELL - 10)
            pygame.draw.rect(screen, color, r, border_radius=10)
        if not self.won:
            fx, fy = self.food
            c = (fx * CELL + CELL // 2, fy * CELL + CELL // 2)
            pygame.draw.circle(screen, (255, 70, 110), c, 14)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W * CELL, H * CELL))
    pygame.display.set_caption("Snake that plays itself")
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        game.step()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
