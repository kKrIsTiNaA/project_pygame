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
    new_player, x, y, return_level = None, None, None, []
    for y in range(len(level)):
        return_level.append([])
        for x in range(len(level)):
            if level[y][x] == '.':
                return_level[-1].append(0)
            if level[y][x] == '#':
                return_level[-1].append(-1)
            if level[y][x] == '@':
                new_player = Character(x, y)
                return_level[-1].append(0)
            if level[y][x] == '№':
                Nps(x, y)
                return_level[-1].append(0)
    return new_player, x, y, return_level


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
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png"), 8, 11, -8, None, True)
            self.image = self.animation.image
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False


    def update(self, flag=None):
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True
        if not self.fl:
            self.animation.update()
            self.image = self.animation.image
        if self.move != (0, 0) and self.animation.die():
            self.rect.x += self.move[0]
            self.rect.y += self.move[1]
            self.animation.update()
            self.image = self.animation.image
        if self.move == (0, 0) and self.animation.die():
            player.animation = animations['stay']
            self.image = self.animation.image

class Nps(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__((nps_group, character_group, all_sprites))
        self.hp = 3
        self.x = pos_x
        self.y = pos_y
        self.way = []
        self.fl = True
        #self.image = (load_image('Download60481.png').subsurface(pygame.Rect((0, 135), (74, 70))))
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, flag=None):
        self.way = []
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True
        if (self.rect.x - player.rect.x) // tile_width <= 8 and (
                self.rect.y - player.rect.y) // tile_height <= 8:
            lab = wave(self.rect.y // tile_height, self.rect.x // tile_width, 1, level_x, level_y,
                       level)
            x, y = player.rect.x // tile_width, player.y // tile_height
            self.get_way(y, x, level_x, level_y, lab, lab[x][y])
            for i in self.way:
                if (self.rect.x - player.rect.x) // tile_width == len(self.way) - 1 or (
                        self.rect.y - player.rect.y) // tile_height == len(self.way) - 1:
                    self.attack((-1, 0))
                else:
                    self.rect.x += i[0] * tile_width
                    self.rect.y += i[1] * tile_height


    def attack(self, direction):
        if self.fl:
            Shell(self.rect.x, self.rect.y, 'fireball', direction, nps_group)
            self.fl = False

    def get_way(self, x, y, n, m, lab, cur):
        if y + 1 < m and lab[x][y + 1] + 1 == cur:
            self.way.append((0, 1))
            self.get_way(x, y + 1, n, m, lab, cur - 1)
        elif x + 1 < n and lab[x + 1][y] + 1 == cur:
            self.way.append((1, 0))
            self.get_way(x + 1, y, n, m, lab, cur - 1)
        elif x - 1 >= 0 and lab[x - 1][y] + 1 == cur:
            self.way.append((-1, 0))
            self.get_way(x - 1, y, n, m, lab, cur - 1)
        elif y - 1 >= 0 and lab[x][y - 1] + 1 == cur:
            self.way.append((0, -1))
            self.get_way(x, y - 1, n, m, lab, cur - 1)

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
            if self.rect.colliderect(i) and i not in self.no_targ:
                i.hp -= 1
                print(i.hp)
                self.kill()

class AnimatedSprite():
    def __init__(self, sheet, columns, rows, cut_x=None, cut_y=None, die=False):
        if die:
            self.count = 0
        else:
            self.count = None
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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.count is not None:
            self.count += 1

    def die(self):
        if self.count is not None:
            if self.count >= 8:
                return True
            else:
                return False
        else:
            return True


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
player, level_x, level_y, level = level_generate(load_level('level1.txt'))
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
