import pygame
import os
import sys
from collections import deque
import copy

pygame.init()

# -------------------- НАСТРОЙКИ --------------------
SIZE = WIDTH, HEIGHT = 550, 550
TILE = 50
FPS = 30
PATH_UPDATE_EVENT = pygame.USEREVENT + 1

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.time.set_timer(PATH_UPDATE_EVENT, 500)

# -------------------- ЗАГРУЗКА --------------------
def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    print("BEFORE IMAGES")
    image = pygame.image.load(fullname)
    print("AFTER IMAGES")
    if colorkey is not None:
        image = image.convert()
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# -------------------- УРОВЕНЬ --------------------
def load_level(filename):
    with open(os.path.join("data", filename)) as f:
        level = [line.strip() for line in f]
    width = max(map(len, level))
    return [line.ljust(width, ".") for line in level]

def generate_level(level):
    player = None
    lab = []
    for y in range(len(level)):
        lab.append([])
        for x in range(len(level[y])):
            if level[y][x] == "#":
                lab[y].append(-1)
            else:
                lab[y].append(0)
            if level[y][x] == "@":
                player = Player(x, y)
            if level[y][x] == "№":
                Enemy(x, y)
    return player, lab

# -------------------- BFS ВОЛНА --------------------
def bfs(start, goal, grid):
    h, w = len(grid), len(grid[0])
    q = deque([start])
    prev = {start: None}

    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] != -1 and (nx, ny) not in prev:
                    prev[(nx, ny)] = (x, y)
                    q.append((nx, ny))

    path = []
    cur = goal
    while cur and cur in prev:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

# -------------------- СПРАЙТЫ --------------------
all_sprites = pygame.sprite.Group()
characters = pygame.sprite.Group()
enemies = pygame.sprite.Group()
players = pygame.sprite.Group()

player_img = pygame.transform.scale(load_image("wizard.png"), (TILE, TILE))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, characters, players)
        self.image = player_img
        self.rect = self.image.get_rect(topleft=(x * TILE, y * TILE))
        self.move = [0, 0]

    def update(self):
        self.rect.x += self.move[0]
        self.rect.y += self.move[1]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, characters, enemies)
        self.image = pygame.transform.scale(load_image("wizard.png"), (TILE, TILE))
        self.rect = self.image.get_rect(topleft=(x * TILE, y * TILE))
        self.path = []

    def update(self):
        if self.path:
            nx, ny = self.path.pop(0)
            self.rect.topleft = (nx * TILE, ny * TILE)

    def recalc_path(self):
        sx = self.rect.x // TILE
        sy = self.rect.y // TILE
        px = player.rect.x // TILE
        py = player.rect.y // TILE
        lab_copy = copy.deepcopy(level_lab)
        self.path = bfs((sx, sy), (px, py), lab_copy)[1:]

# -------------------- ЗАПУСК --------------------
player, level_lab = generate_level(load_level("level1.txt"))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == PATH_UPDATE_EVENT:
            for e in enemies:
                e.recalc_path()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move = [-5, 0]
            if event.key == pygame.K_RIGHT:
                player.move = [5, 0]
            if event.key == pygame.K_UP:
                player.move = [0, -5]
            if event.key == pygame.K_DOWN:
                player.move = [0, 5]

        if event.type == pygame.KEYUP:
            player.move = [0, 0]

    screen.fill((240, 240, 240))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
