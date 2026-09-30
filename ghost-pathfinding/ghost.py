# A ghost that always finds you: BFS, Dijkstra and A*
import heapq
import random
from collections import deque
import pygame

COLS, ROWS, CELL = 21, 21, 38
WALL, FLOOR, MUD = 0, 1, 5  # number = cost to step there
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BLUE, BROWN = (33, 66, 200), (70, 50, 30)
YELLOW, PINK = (255, 214, 10), (255, 70, 110)


def make_maze(rng):
    # carve a random maze by walking and backtracking
    g = [[WALL] * COLS for _ in range(ROWS)]
    g[1][1] = FLOOR
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        options = [(dx, dy) for dx, dy in DIRS
                   if 0 < x + 2 * dx < COLS - 1
                   and 0 < y + 2 * dy < ROWS - 1
                   and g[y + 2 * dy][x + 2 * dx] == WALL]
        if not options:
            stack.pop()
            continue
        dx, dy = rng.choice(options)
        g[y + dy][x + dx] = FLOOR
        g[y + 2 * dy][x + 2 * dx] = FLOOR
        stack.append((x + 2 * dx, y + 2 * dy))
    for _ in range(45):  # knock out walls to make loops
        x = rng.randrange(1, COLS - 1)
        y = rng.randrange(1, ROWS - 1)
        g[y][x] = FLOOR
    for _ in range(5):  # sprinkle some mud
        cx = rng.randrange(2, COLS - 2)
        cy = rng.randrange(2, ROWS - 2)
        for x in range(cx - 1, cx + 2):
            for y in range(cy - 1, cy + 2):
                if g[y][x] == FLOOR:
                    g[y][x] = MUD
    return g


def neighbors(grid, cell):
    x, y = cell
    for dx, dy in DIRS:
        if grid[y + dy][x + dx] != WALL:
            yield (x + dx, y + dy)


def path_to(came_from, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = came_from[goal]
    return path[::-1]


def bfs(grid, start, goal):
    came_from = {start: None}
    queue = deque([start])
    order = []  # every cell we looked at
    while queue:
        cell = queue.popleft()
        order.append(cell)
        if cell == goal:
            break
        for nxt in neighbors(grid, cell):
            if nxt not in came_from:
                came_from[nxt] = cell
                queue.append(nxt)
    return path_to(came_from, goal), order


def guess(a, b):
    # steps left if there were no walls
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal, use_guess=True):
    # with use_guess=False this is Dijkstra
    cost = {start: 0}
    came_from = {start: None}
    frontier = [(0, start)]
    done, order = set(), []
    while frontier:
        _, cell = heapq.heappop(frontier)
        if cell in done:
            continue
        done.add(cell)
        order.append(cell)
        if cell == goal:
            break
        for nxt in neighbors(grid, cell):
            new = cost[cell] + grid[nxt[1]][nxt[0]]
            if nxt not in cost or new < cost[nxt]:
                cost[nxt] = new
                came_from[nxt] = cell
                h = guess(nxt, goal) if use_guess else 0
                heapq.heappush(frontier, (new + h, nxt))
    return path_to(came_from, goal), order


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.grid = make_maze(self.rng)
        self.ghost = (1, 1)
        self.player = (COLS - 2, ROWS - 2)
        self.target = self.player
        self.path = []
        self.caught = 0
        self.ghost_wait = self.player_wait = 0

    def floor_cells(self):
        g = self.grid
        return [(x, y) for y in range(ROWS)
                for x in range(COLS) if g[y][x] != WALL]

    def flee_target(self):
        # the player runs to a spot far from the ghost
        spots = self.rng.sample(self.floor_cells(), 8)
        far = lambda c: guess(c, self.ghost)
        return max(spots, key=far)

    def step(self):
        g = self.grid
        self.player_wait -= 1
        if self.player_wait <= 0:
            if self.player == self.target:
                self.target = self.flee_target()
            route, _ = bfs(g, self.player, self.target)
            self.player = route[min(1, len(route) - 1)]
            x, y = self.player
            self.player_wait = 3 * g[y][x]
        self.ghost_wait -= 1
        # the ghost re-plans its route every single frame
        self.path, _ = astar(g, self.ghost, self.player)
        if self.ghost_wait <= 0 and len(self.path) > 1:
            self.ghost = self.path[1]
            x, y = self.ghost
            self.ghost_wait = 4 * g[y][x]
        if self.ghost == self.player:
            self.caught += 1
            self.respawn()

    def respawn(self):
        self.player = self.flee_target()
        self.target = self.player

    def draw(self, screen):
        screen.fill((10, 12, 30))
        for y in range(ROWS):
            for x in range(COLS):
                r = (x * CELL, y * CELL, CELL, CELL)
                if self.grid[y][x] == WALL:
                    pygame.draw.rect(screen, BLUE, r)
                elif self.grid[y][x] == MUD:
                    pygame.draw.rect(screen, BROWN, r)
        half = CELL // 2
        for x, y in self.path[1:-1]:
            c = (x * CELL + half, y * CELL + half)
            pygame.draw.circle(screen, PINK, c, 4)
        px, py = self.player
        c = (px * CELL + half, py * CELL + half)
        pygame.draw.circle(screen, YELLOW, c, half - 4)
        mouth = [c, (c[0] + half, c[1] - 9), (c[0] + half, c[1] + 9)]
        pygame.draw.polygon(screen, (10, 12, 30), mouth)
        gx, gy = self.ghost
        body = pygame.Rect(gx * CELL, gy * CELL, CELL, CELL)
        body.inflate_ip(-8, -8)
        pygame.draw.rect(screen, PINK, body,
                         border_top_left_radius=half,
                         border_top_right_radius=half)
        eye = (gx * CELL + half, gy * CELL + half - 3)
        pygame.draw.circle(screen, "white", eye, 6)


def main():
    pygame.init()
    size = (COLS * CELL, ROWS * CELL)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        game.step()
        game.draw(screen)
        caption = f"Caught {game.caught} times"
        pygame.display.set_caption(caption)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
