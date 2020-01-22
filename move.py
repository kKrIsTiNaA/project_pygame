import pygame
import os
import sys

CAN_ATTACK = 10

pygame.init()
size = w, h = 550, 550
screen = pygame.display.set_mode(size)
pygame.time.set_timer(CAN_ATTACK, 2000)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def get_way(x, y, n, m, lab, list, cur):
    if y + 1 < m and lab[x][y + 1] + 1 == cur:
        list.append((0, -1))
        get_way(x, y + 1, n, m, lab, list, cur - 1)
    if x + 1 < n and lab[x + 1][y] + 1 == cur:
        list.append((-1, 0))
        get_way(x, y + 1, n, m, lab, list, cur - 1)
    if x - 1 >= 0 and lab[x - 1][y] + 1 == cur:
        list.append((1, 0))
        get_way(x, y + 1, n, m, lab, list, cur - 1)
    if y - 1 >= 0 and lab[x][y - 1] + 1 == cur:
        list.append((0, 1))
        get_way(x, y + 1, n, m, lab, list, cur - 1)


def wave(x, y, cur, n, m, lab):
    lab[x][y] = cur
    if y + 1 < m:
        if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
            wave(x, y + 1, cur + 1, n, m, lab)
    if x + 1 < n:
        if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
            wave(x + 1, y, cur + 1, n, m, lab)
    if x - 1 >= 0:
        if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
            wave(x - 1, y, cur + 1, n, m, lab)
    if y - 1 >= 0:
        if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
            wave(x, y - 1, cur + 1, n, m, lab)
    return lab


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def level_generate(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level)):
            if level[y][x] == '@':
                new_player = Character(x, y)
    return new_player, x, y


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, character_group, all_sprites)
        self.hp = 10

        self.x = pos_x
        self.y = pos_y
        self.fl = True
        self.move = (0, 0)
        self.animation = animations['stay']
        self.image = self.animation.image
        self.rect = self.image.get_rect()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png"), 8, 11, -5, None)
            self.image = self.animation.image
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False


    def update(self, flag=None):
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True
        self.rect.x += self.move[0]
        self.rect.y += self.move[1]
        if self.move != (0, 0):
            self.animation.update()
            self.image = self.animation.image
        elif self.move == (0, 0):
            player.animation = animations['stay']
            self.image = self.animation.image


class Nps(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__((nps_group, character_group, all_sprites))
        self.hp = 3
        self.x = pos_x
        self.y = pos_y
        self.fl = True
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, flag=None):
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True

        if (self.rect.x - player.rect.x) // tile_width <= 8 and (
                self.rect.y - player.rect.y) // tile_height <= 8:
            self.attack((-1, 0))

    def attack(self, direction):
        if self.fl:
            Shell(self.rect.x, self.rect.y, 'fireball', direction, nps_group)
            self.fl = False


class Boss(Nps):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.hp = 20
        self.spawn = True

    def attack(self, direction):
        if self.spawn:
            Nps((self.rect.x // tile_width) + 1, self.rect.y // tile_height)
            Nps((self.rect.x // tile_width) - 1, self.rect.y // tile_height)
            self.spawn = False
        elif self.fl:
            AnimatedSprite(load_image("vamp (1).bmp", (0, 0, 0)), 8, 11,
                           self.rect.x - 70,
                           self.rect.y - 70, -24, -16)
            Shell(self.rect.x, self.rect.y, 'fireball', direction, nps_group)
            self.fl = False


class Shell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type, direction, no_targ):
        super().__init__(all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.no_targ = no_targ
        self.image = shells[type]
        self.rect = self.image.get_rect().move(pos_x + direction[0] * tile_width,
                                               pos_y + direction[1] * tile_height)
        self.direction = direction

    def update(self):
        self.rect = self.rect.move(self.direction[0] * 10, self.direction[1] * 10)
        for i in character_group:
            if self.rect.colliderect(i.rect) and i not in self.no_targ:
                i.hp -= 1
                print(i.hp)
                self.kill()


class AnimatedSprite():
    def __init__(self, sheet, columns, rows, cut_x=None, cut_y=None, clock=False):
        if clock:
            self.clock = pygame.time.Clock()
            self.clock.tick()
        else:
            self.clock = None
        self.cut_x = cut_x
        self.cut_y = cut_y
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        self.frames = self.frames[self.cut_x:self.cut_y]

    def update(self):
        if self.clock is not None:
            if self.clock.tick() >= 1000:
                print(1)
                self.kill()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


shells = {'fireball': pygame.transform.scale(load_image('fireball.png', (0, 0, 0)), (50, 30))}
animations = {'up': AnimatedSprite(load_image('Download57453.png', (0, 0, 0)), 24, 33, 192, 201),
              'left': AnimatedSprite(load_image('Download57453.png', (0, 0, 0)), 24, 33, 216, 225),
              'down': AnimatedSprite(load_image('Download57453.png', (0, 0, 0)), 24, 33, 240, 249),
              'right': AnimatedSprite(load_image('Download57453.png', (0, 0, 0)), 24, 33, 264, 273),
              'stay': AnimatedSprite(load_image('Download57453.png', (0, 0, 0)), 24, 33, 48, 49)}
player_image = load_image('wizard.png')
player_image = pygame.transform.scale(player_image, (50, 50))
tile_width = tile_height = 50
player = None
flag = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
character_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
nps_group = pygame.sprite.Group()
player, level_x, level_y = level_generate(load_level('level1.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == CAN_ATTACK:
            character_group.update('flag')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if event.mod == 64:
                    player.attack((-1, 0))
                else:
                    player.animation = animations['left']
                    player.move = (-5, 0)
            if event.key == pygame.K_RIGHT:
                if event.mod == 64:
                    player.attack((1, 0))
                else:
                    player.animation = animations['right']
                    player.move = (5, 0)
            if event.key == pygame.K_UP:
                if event.mod == 64:
                    player.attack((0, -1))
                else:
                    player.animation = animations['up']
                    player.move = (0, -5)
            if event.key == pygame.K_DOWN:
                if event.mod == 64:
                    player.attack((0, 1))
                else:
                    player.animation = animations['down']
                    player.move = (0, 5)
        if event.type == pygame.KEYUP:
            player.move = (0, 0)
    screen.fill((255, 255, 255))
    all_sprites.update()
    all_sprites.draw(screen)
    clock.tick(8)
    pygame.display.flip()
