import pygame
import os
import sys
import random

CAN_ATTACK = 10
MOVE = 10

pygame.init()
size = w, h = 900, 900
screen = pygame.display.set_mode(size)
pygame.time.set_timer(CAN_ATTACK, 2000)
pygame.time.set_timer(MOVE, 5000)


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
        self.ind_x = 0
        self.ind_y = 0
        self.move = (0, 0)
        self.animation = animations['stay']
        self.image = self.animation.image
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)

    def right_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 8, 33, -16, -8, True)
            self.image = self.animation.image
            self.rect.x -= 60
            self.ind_x = 60
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def left_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 8, 33, -64, -56, True)
            self.image = self.animation.image
            self.rect.x -= 60
            self.ind_x = 60
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def up_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 24, 20, -164, -140, True, True)
            self.image = self.animation.image
            self.rect.y -= 40
            self.ind_y = 40
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def down_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 24, 20, -68, -48, True, True)
            self.image = self.animation.image
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False


    def update(self, flag=None):
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True
        self.animation.update()
        self.image = self.animation.image
        if self.move != (0, 0):
            self.rect.x += self.move[0]
            self.rect.y += self.move[1]
            self.animation.update()
            self.image = self.animation.image
        if self.move == (0, 0) and self.animation.die():
            self.rect.x += self.ind_x
            self.rect.y += self.ind_y
            self.ind_x, self.ind_y = 0, 0
            player.animation = animations['stay']
            self.image = self.animation.image

class Nps(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__((nps_group, character_group, all_sprites))
        self.hp = 3
        self.x = pos_x
        self.y = pos_y
        self.ind_x = 0
        self.ind_y = 0
        self.way = []
        self.move = (0, 0)
        self.fl = True
        self.animation = animations_nps['stay']
        self.image = self.animation.image
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)

    def update(self, flag=None):
        if self.hp <= 0:
            self.kill()
            self.fl = False
        if flag:
            self.fl = True
        self.animation.update()
        self.image = self.animation.image
        if self.move != (0, 0):
            if self.move == (8, 0):
                self.animation = animations_nps['right']
            elif self.move == (-8, 0):
                self.animation = animations_nps['left']
            elif self.move == (0, 8):
                self.animation = animations_nps['down']
            elif self.move == (0, -8):
                self.animation = animations_nps['up']
            self.rect.x += self.move[0]
            self.rect.y += self.move[1]
            self.animation.update()
            self.image = self.animation.image
        if self.move == (0, 0) and self.animation.die():
            self.rect.x += self.ind_x
            self.rect.y += self.ind_y
            self.ind_x, self.ind_y = 0, 0
            player.animation = animations_nps['stay']
            self.image = self.animation.image
        if self.rect.x == player.rect.x and self.rect.y > player.rect.y:
            print(4)
            self.up_attack((0, -1))
        if self.rect.x == player.rect.x and self.rect.y < player.rect.y:
            print(3)
            self.down_attack((0, 1))
        if self.rect.y == player.rect.y and self.rect.x > player.rect.x:
            print(2)
            self.left_attack((-1, 0))
        if self.rect.y == player.rect.y and self.rect.x < player.rect.x:
            print(1)
            self.right_attack((1, 0))

    def right_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 8, 33, -16,
                                            -8, True)
            self.image = self.animation.image
            self.rect.x -= 0
            self.ind_x = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def left_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 8, 33, -64,
                                            -56, True)
            self.image = self.animation.image
            self.rect.x -= 0
            self.ind_x = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def up_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 24, 20,
                                            -164, -140, True, True)
            self.image = self.animation.image
            self.rect.y -= 0
            self.ind_y = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def down_attack(self, direction):
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 24, 20, -68,
                                            -48, True, True)
            self.image = self.animation.image
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False


class Boss(Nps):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.hp = 20
        Nps((self.rect.x // tile_width) + 1, self.rect.y // tile_height)
        Nps((self.rect.x // tile_width) - 1, self.rect.y // tile_height)


class Shell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type, direction, no_targ):
        super().__init__(all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.no_targ = no_targ
        if direction == (-1, 0):
            image = pygame.transform.rotate(shells[type], 180)
        elif direction == (0, 1):
            image = pygame.transform.rotate(shells[type], 270)
        elif direction == (0, -1):
            image = pygame.transform.rotate(shells[type], 90)
        else:
            image = shells[type]
        self.image = image
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
    def __init__(self, sheet, columns, rows, cut_x=None, cut_y=None, die=False, speed=False):
        if die:
            self.count = 0
        else:
            self.count = None
        self.speed = speed
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
        if not self.speed:
            self.frames = self.frames[self.cut_x:self.cut_y]
        else:
            self.frames = self.frames[self.cut_x:self.cut_y:3]

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
animations_nps = {'up': AnimatedSprite(load_image('Download60481.png', (0, 0, 0)), 24, 33, 192, 201),
              'left': AnimatedSprite(load_image('Download60481.png', (0, 0, 0)), 24, 33, 216, 225),
              'down': AnimatedSprite(load_image('Download60481.png', (0, 0, 0)), 24, 33, 240, 249),
              'right': AnimatedSprite(load_image('Download60481.png', (0, 0, 0)), 24, 33, 264, 273),
              'stay': AnimatedSprite(load_image('Download60481.png', (0, 0, 0)), 24, 33, 48, 49)}
player_image = load_image('wizard.png')
player_image = pygame.transform.scale(player_image, (50, 50))
tile_width = tile_height = 50
player = None
nps_move = [(4, 0), (-4, 0), (0, 4), (0, -4)]
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
        if event.type == MOVE:
            for i in nps_group:
                i.move = random.choice(nps_move)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if event.mod == 64:
                    player.left_attack((-1, 0))
                elif player.animation.die():
                    player.animation = animations['left']
                    player.move = (-5, 0)
            if event.key == pygame.K_RIGHT:
                if event.mod == 64:
                    player.right_attack((1, 0))
                elif player.animation.die():
                    player.animation = animations['right']
                    player.move = (5, 0)
            if event.key == pygame.K_UP:
                if event.mod == 64:
                    player.up_attack((0, -1))
                elif player.animation.die():
                    player.animation = animations['up']
                    player.move = (0, -5)
            if event.key == pygame.K_DOWN:
                if event.mod == 64:
                    player.down_attack((0, 1))
                elif player.animation.die():
                    player.animation = animations['down']
                    player.move = (0, 5)
        if event.type == pygame.KEYUP:
            player.move = (0, 0)
    screen.fill((255, 255, 255))
    all_sprites.update()
    all_sprites.draw(screen)
    clock.tick(8)
    pygame.display.flip()
