import os
import random
import sys

import pygame
from pygame import mixer

CAN_ATTACK = 10
MOVE = 10

pygame.init()
mixer.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('The Lord of Hell')
pygame.time.set_timer(CAN_ATTACK, 2000)
pygame.time.set_timer(MOVE, 5000)
pygame.mouse.set_visible(False)
win = mixer.Sound('data/win.ogg')
over = mixer.Sound('data/die.ogg')
get = mixer.Sound('data/get.ogg')
intro = mixer.Sound('data/fantasy_intro.ogg')
click = mixer.Sound('data/click.ogg')
attack = mixer.Sound('data/attack.ogg')


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


TILE_IMAGES = {'n': load_image('lb.png'), 'l': load_image('ln.png'),
               'r': load_image('stone2.png'), 's': load_image('sand2.png'),
               'f': load_image('flower12.png'), 't': load_image('pl2.png'),
               'w': load_image('water2.png'), 'v': load_image('pine_t2.png'),
               'j': load_image('pine_b2.png'), 'g': load_image('mushroom2.png'),
               'k': load_image('key2.png'), 'x': load_image('fish_water.png'),
               '+': load_image('bochka2.png'), 'b': load_image('timber2.png'),
               "$": load_image('left_bird2.png'),
               '!': load_image('right_bird2.png'), 'u': load_image('kust2.png'),
               'y': load_image('sv.png'), 'i': load_image('sn.png'),
               'o': load_image('kolodets2.png'), 'a': load_image('what2.png'),
               'z': load_image('fl12.png'), '1': load_image('h1_2.png'),
               '2': load_image('h2_2.png'), '3': load_image('h3_2.png'),
               '4': load_image('h4_2.png'), '5': load_image('h5.png'),
               '6': load_image('h6_2.png'), '7': load_image('h7_2.png'),
               '8': load_image('h8.png'), '9': load_image('h9_2.png'),
               '0': load_image('h10_2.png'), '#': load_image('h11_2.png'),
               '%': load_image('h12_2.png'), '*': load_image('h13_2.png'),
               '?': load_image('h14_2.png'), 'p': load_image('fish_water2.png'),
               '&': load_image('bread2.png'), '~': load_image('block.png')}
TILE_IMAGES2 = {'w': load_image('stone_wall2.jpg'), 'k': load_image('flag2.png'),
                '(': load_image('por22.png'), ')': load_image('por12.png'),
                '5': load_image('b32.png'), '6': load_image('b42.png'),
                '7': load_image('b12.png'), '8': load_image('b2.png'),
                'g': load_image('d52.png'), 'h': load_image('d62.png'),
                'y': load_image('d3.png'), 'u': load_image('d4.png'),
                'i': load_image('d1.png'), 'o': load_image('d2.png'),
                'c': load_image('cl2.jpg'), 's': load_image('cl12.jpg'),
                '=': load_image('tum2.png'), 'e': load_image('bed22.png'),
                'd': load_image('bed12.png'), '1': load_image('w32.png'),
                '2': load_image('w42.png'), '3': load_image('w12.png'),
                '4': load_image('w22.png'), '!': load_image('u32.jpg'),
                '?': load_image('u42.jpg'), '$': load_image('u12.png'),
                '%': load_image('u22.png'), 'a': load_image('fir2.png'),
                'b': load_image('t12.png'), 'm': load_image('t22.png'),
                'p': load_image('t32.png'), 't': load_image('t42.png'),
                '+': load_image('for_legs2.png'), ',': load_image('chair_l2.png'),
                '.': load_image('chair_r2.png'), '#': load_image('ta42.png'),
                '>': load_image('ta52.png'), '&': load_image('ta62.png'),
                '*': load_image('ta12.png'), '-': load_image('ta22.png'),
                '~': load_image('ta32.png'), 'q': load_image('yaschik.png'),
                '_': load_image('stock_fl2.png'), '^': load_image('stock_wine2.png'),
                '<': load_image('bochki2.png'), 'v': load_image('pink_carpet_2.png'),
                'r': load_image('pink_carpet2.png'), 'f': load_image('floor.jpg')}
TILE_IMAGES3 = {'w': load_image('cave2.png'), 'b': load_image('block.png'),
                'l': load_image('bat_l.png'), 'r': load_image('bat_r.png'),
                'p': load_image('spider.png'),
                'f': load_image('torch2.png'), 's': load_image('ground.png')}


def terminate():
    pygame.quit()
    sys.exit()


def game_over():
    over.play()
    image3 = load_image('fon2.jpg')
    screen.blit(image3, (0, 0))
    text3 = ['GAME OVER',
             "Чтобы продолжить, нажмите 'Пробел'"]
    text_coord = 50
    for line in text3:
        if 'GAME' in line:
            font4 = pygame.font.Font('data/18642.ttf', 50)
            string_rendered = font4.render(line, 1, pygame.Color('black'))
        else:
            font5 = pygame.font.Font('data/18642.ttf', 32)
            string_rendered = font5.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    running3 = True
    pygame.display.flip()
    while running3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    click.play()
                    return


def show_rules():
    screen2 = pygame.display.set_mode(size)
    image2 = load_image('mountains.png')
    screen2.blit(image2, (0, 0))
    text2 = ["ПРАВИЛА", " ", "Ваш персонаж - волшебник, задача которого -",
             "уничтожить помощника Сатаны, который причиняет",
             "вред мирным жителям. Вам нужно пройти пройти",
             "2 уровня, а потом сразиться с главным злодеем.",
             "Подсказка: вам необходимо убить всех монстров на",
             "каждом уровне. Для передвижения используйте",
             "клавиши-стрелки, а для атаки - левую кнопку мыши.",
             "Подобрать предмет или зайти в дом можно",
             "при помощи клавиши Enter. Удачи!",
             "Чтобы вернуться назад, нажмите Esc"]
    font3 = pygame.font.Font('data/18642.ttf', 32)
    text_coord = 30
    for line in text2:
        if ('Для передвижения' in line or 'атаки -' in line or
                'при помощи клавиши' in line or 'Удачи' in line or
                'Подсказка' in line or 'Подобрать' in line):
            string_rendered = font3.render(line, 1, pygame.Color('white'))
        elif "Esc" in line:
            string_rendered = font3.render(line, 1, pygame.Color('yellow'))
        else:
            string_rendered = font3.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        if 'Esc' in line:
            intro_rect.top = 10
            intro_rect.x = 240
        screen.blit(string_rendered, intro_rect)
    running2 = True
    pygame.display.flip()
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    click.play()
                    return


def start_screen():
    intro.play(-1)
    image = load_image('fon.png')
    image = pygame.transform.scale(image, (800, 600))
    screen.blit(image, (0, 0))
    intro_text = 'THE LORD OF HELL'
    font = pygame.font.Font('data/17440.otf', 60)
    string_rend = font.render(intro_text, 1, (0, 0, 0))
    intro_rect = string_rend.get_rect()
    intro_rect.top = 100
    intro_rect.x = 130
    screen.blit(string_rend, intro_rect)
    font2 = pygame.font.Font('data/18642.ttf', 42)
    text = ['НАЧАТЬ', 'ПРАВИЛА ИГРЫ', 'ВЫХОД']
    text_coords = 190
    for line in text:
        string_rend = font2.render(line, 1, (0, 0, 0))
        intro_rect = string_rend.get_rect()
        text_coords += 50
        intro_rect.top = text_coords
        intro_rect.x = 130
        text_coords += intro_rect.height
        screen.blit(string_rend, intro_rect)
    cursor = Cursor()
    all_sprites.add(cursor)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        click.play()
                        cursor.move_up()
                    elif event.key == pygame.K_DOWN:
                        click.play()
                        cursor.move_down()
                    elif event.key == pygame.K_RETURN:
                        if cursor.rect.y == 245:
                            click.play()
                            intro.stop()
                            cursor.kill()
                            return
                        elif cursor.rect.y == 345:
                            click.play()
                            show_rules()
                        else:
                            click.play()
                            terminate()
        screen.blit(image, (0, 0))
        string_rend = font.render(intro_text, 1, (0, 0, 0))
        intro_rect = string_rend.get_rect()
        intro_rect.top = 100
        intro_rect.x = 130
        screen.blit(string_rend, intro_rect)
        font2 = pygame.font.Font('data/18642.ttf', 42)
        text = ['НАЧАТЬ', 'ПРАВИЛА ИГРЫ', 'ВЫХОД']
        text_coords = 190
        for line in text:
            if (cursor.rect.y == 245 and line == 'НАЧАТЬ' or
                    cursor.rect.y == 345 and line == 'ПРАВИЛА ИГРЫ' or
                    cursor.rect.y == 445 and line == 'ВЫХОД'):
                string_rend = font2.render(line, 1, (255, 255, 40))
            else:
                string_rend = font2.render(line, 1, (0, 0, 0))
            intro_rect = string_rend.get_rect()
            text_coords += 50
            intro_rect.top = text_coords
            intro_rect.x = 130
            text_coords += intro_rect.height
            screen.blit(string_rend, intro_rect)
        all_sprites.draw(screen)
        pygame.display.flip()


def win_screen():
    win.play(-1)
    screen4 = pygame.display.set_mode(size)
    image4 = load_image('fon.jpg')
    screen4.blit(image4, (0, 0))
    font6 = pygame.font.Font('data/18642.ttf', 40)
    text_coord = 150
    for i in range(2):
        if i == 0:
            string_rendered = font6.render('ВЫ ПОБЕДИЛИ!', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 210
        else:
            string_rendered = font6.render('Нажмите "Пробел"', 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 240
        intro_rect.top = text_coord
        text_coord += 200
        screen.blit(string_rendered, intro_rect)
    running4 = True
    pygame.display.flip()
    while running4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    win.stop()
                    click.play()
                    main()
                    return


class Heart(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        global hearts
        super().__init__(hearts)
        self.image = load_image('heart.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, 10


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image('sword.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 65, 245

    def move_up(self):
        if self.rect.y != 245:
            self.rect.y -= 100

    def move_down(self):
        if self.rect.y != 445:
            self.rect.y += 100


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        return level_map


def level_generate(level):
    global count
    new_player, x, y, return_level = None, None, None, []
    if '~' in level[1]:
        for y in range(len(level)):
            return_level.append([])
            for x in range(len(level[y])):
                if level[y][x] == '@':
                    Tile(TILE_IMAGES['s'], x, y, True)
                    return_level[-1].append(0)
                    new_player = Character(x, y)
                elif level[y][x] != 'm':
                    if level[y][x] != 's':
                        return_level[-1].append(-1)
                        if level[y][x] == 'k':
                            global key
                            key = Tile(TILE_IMAGES[level[y][x]], x, y, False)
                        else:
                            Tile(TILE_IMAGES[level[y][x]], x, y, False)
                    else:
                        return_level[-1].append(0)
                        Tile(TILE_IMAGES[level[y][x]], x, y, True)
                else:
                    count += 1
                    Tile(TILE_IMAGES['s'], x, y, True)
                    return_level[-1].append(0)
                    Nps(x, y)
    elif 'w' in level[0]:
        for y in range(len(level)):
            return_level.append([])
            for x in range(len(level[y])):
                if level[y][x] == '@':
                    Tile(TILE_IMAGES2['f'], x, y, True)
                    new_player = Character(x, y)
                elif level[y][x] != 'x':
                    if (level[y][x] != 'v' or level[y][x] != 'r' or
                            level[y][x] != 'f'):
                        Tile(TILE_IMAGES2[level[y][x]], x, y, False)
                    else:
                        Tile(TILE_IMAGES2[level[y][x]], x, y, True)
                else:
                    count += 1
                    Tile(TILE_IMAGES2['f'], x, y, True)
                    Nps(x, y)
    else:
        for y in range(len(level)):
            return_level.append([])
            for x in range(len(level[y])):
                if level[y][x] == '@':
                    Tile(TILE_IMAGES3['s'], x, y, True)
                    return_level[-1].append(0)
                    new_player = Character(x, y)
                elif level[y][x] != 'm':
                    if level[y][x] != 's':
                        return_level[-1].append(-1)
                        Tile(TILE_IMAGES3[level[y][x]], x, y, False)
                    else:
                        return_level[-1].append(0)
                        Tile(TILE_IMAGES3[level[y][x]], x, y, True)
                else:
                    Tile(TILE_IMAGES3['s'], x, y, True)
                    return_level[-1].append(0)
                    count += 1
                    Nps(x, y, boss=True)
    return new_player, x, y, return_level


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_image, pos_x, pos_y, can_move):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.move = can_move


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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)

    def right_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 8, 33, -16, -8, True)
            self.image = self.animation.image
            self.rect.x -= 60
            self.ind_x = 60
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def left_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 8, 33, -64, -56, True)
            self.image = self.animation.image
            self.rect.x -= 60
            self.ind_x = 60
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def up_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download57453.png", (0, 0, 0)), 24, 20, -164, -140, True, True)
            self.image = self.animation.image
            self.rect.y -= 40
            self.ind_y = 40
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, player_group)
            self.fl = False

    def down_attack(self, direction):
        attack.play()
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
            if self.move == (5, 0):
                self.animation = animations['right']
            elif self.move == (-5, 0):
                self.animation = animations['left']
            elif self.move == (0, 5):
                self.animation = animations['down']
            elif self.move == (0, -5):
                self.animation = animations['up']
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
        self.mask = pygame.mask.from_surface(self.image)


class Nps(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, boss=False):
        super().__init__((nps_group, all_sprites, character_group))
        if not boss:
            self.hp = 3
        else:
            self.hp = 20
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
            global count
            count -= 1
            self.fl = False
        if flag:
            self.fl = True
        self.animation.update()
        self.image = self.animation.image
        if self.rect.x == player.rect.x and self.rect.y > player.rect.y:
            self.up_attack((0, -1))
        elif self.rect.x == player.rect.x and self.rect.y < player.rect.y:
            self.down_attack((0, 1))
        elif self.rect.y == player.rect.y and self.rect.x > player.rect.x:
            self.left_attack((-1, 0))
        elif self.rect.y == player.rect.y and self.rect.x < player.rect.x:
            self.right_attack((1, 0))
        elif self.move != (0, 0):
            if self.move == (4, 0):
                self.animation = animations_nps['right']
            elif self.move == (-4, 0):
                self.animation = animations_nps['left']
            elif self.move == (0, 4):
                self.animation = animations_nps['down']
            elif self.move == (0, -4):
                self.animation = animations_nps['up']
            self.rect.x += self.move[0]
            self.rect.y += self.move[1]
            self.animation.update()
            self.image = self.animation.image
        elif self.move == (0, 0) and self.animation.die():
            self.rect.x += self.ind_x
            self.rect.y += self.ind_y
            self.ind_x, self.ind_y = 0, 0
            player.animation = animations_nps['stay']
            self.image = self.animation.image

    def right_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 8, 33, -16,
                                            -8, True)
            self.image = self.animation.image
            self.rect.x -= 0
            self.ind_x = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def left_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 8, 33, -64,
                                            -56, True)
            self.image = self.animation.image
            self.rect.x -= 0
            self.ind_x = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def up_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 24, 20,
                                            -164, -140, True, True)
            self.image = self.animation.image
            self.rect.y -= 0
            self.ind_y = 0
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False

    def down_attack(self, direction):
        attack.play()
        if self.fl:
            self.animation = AnimatedSprite(load_image("Download60481.png", (0, 0, 0)), 24, 20, -68,
                                            -48, True, True)
            self.image = self.animation.image
            Shell(self.rect.x + 10, self.rect.y + 15, 'fireball', direction, nps_group)
            self.fl = False


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


class Camera:
    def __init__(self, camera_func, total_w, total_h):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, total_w, total_h)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + w // 2
    t = -target_rect.y + h // 2
    width, height = camera.width, camera.height
    l = min(0, l)
    l = max(-(camera.width - w), l)
    t = max(-(camera.height - h), t)
    t = min(0, t)
    return pygame.Rect(l, t, width, height)


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

all_sprites = pygame.sprite.Group()
player_image = load_image('wizard.png')
player_image = pygame.transform.scale(player_image, (50, 50))
tiles_group = pygame.sprite.Group()
nps_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
character_group = pygame.sprite.Group()
hearts = pygame.sprite.Group()
nps_move = [(4, 0), (-4, 0), (0, 4), (0, -4)]
player = None
tile_width = tile_height = 50
clock = pygame.time.Clock()
key = None
count = None
flag = True
exit = 0


def show_level1():
    global all_sprites, nps_groupm, character_group, player_group, exit, \
        hearts, player_image, tiles_group, player, clock, key, count, flag
    exit = 0
    count = 0
    key_group = pygame.sprite.Group()
    player, level_x, level_y, level = level_generate(load_level('level1.txt'))
    total_w = level_x * tile_width
    total_h = level_y * tile_width
    camera = Camera(camera_func, total_w, total_h)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = 1
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
                        player.move = (-5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (5, 0)
                if event.key == pygame.K_RIGHT:
                    if event.mod == 64:
                        player.right_attack((1, 0))
                    elif player.animation.die():
                        player.move = (5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (-5, 0)
                if event.key == pygame.K_UP:
                    if event.mod == 64:
                        player.up_attack((0, -1))
                    elif player.animation.die():
                        player.move = (0, -5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, 5)
                if event.key == pygame.K_DOWN:
                    if event.mod == 64:
                        player.down_attack((0, 1))
                    elif player.animation.die():
                        player.move = (0, 5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, -5)
                if event.key == pygame.K_RETURN:
                    if (player.rect.x // 50 == 7 and
                            player.rect.y // 50 == 17):
                        key.kill()
                        Tile(TILE_IMAGES['s'], 8, 18, True)
                        key = pygame.sprite.Sprite()
                        key.image = load_image('key.png', -1)
                        key.rect = key.image.get_rect()
                        key.rect.x, key.rect.y = 740, 10
                        get.play()
                        key.add(key_group)
                    if (player.rect.x // 50 == 22 and
                            player.rect.y // 50 == 18 and
                            key in key_group and count == 0):
                        return
            if event.type == pygame.KEYUP:
                player.move = (0, 0)
            if player.hp == 0:
                exit = 2
                return
        all_sprites.update()
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in nps_group:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        hearts = pygame.sprite.Group()
        x = 10
        for i in range(player.hp):
            heart = Heart(x)
            heart.add(hearts)
            x += 30
        hearts.draw(screen)
        key_group.draw(screen)
        clock.tick(10)
        pygame.display.flip()


def show_level2():
    global all_sprites, nps_group, character_group, player_group, \
        hearts, player_image, tiles_group, player, clock, count, exit
    for sprite in all_sprites:
        sprite.kill()
    screen.fill(pygame.Color('white'))
    count = 0
    exit = 0
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    nps_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    character_group = pygame.sprite.Group()
    player, level_x, level_y, level = level_generate(load_level('level2.txt'))
    total_w = level_x * tile_width
    total_h = level_y * tile_width
    camera = Camera(camera_func, total_w, total_h)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = 1
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
                        player.move = (-5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (5, 0)
                if event.key == pygame.K_RIGHT:
                    if event.mod == 64:
                        player.right_attack((1, 0))
                    elif player.animation.die():
                        player.move = (5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (-5, 0)
                if event.key == pygame.K_UP:
                    if event.mod == 64:
                        player.up_attack((0, -1))
                    elif player.animation.die():
                        player.move = (0, -5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, 5)
                if event.key == pygame.K_DOWN:
                    if event.mod == 64:
                        player.down_attack((0, 1))
                    elif player.animation.die():
                        player.move = (0, 5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, -5)
                if event.key == pygame.K_RETURN:
                    if (player.rect.x // 50 == 19 and player.rect.y // 50 == 5 and
                            count == 0):
                        return
            if event.type == pygame.KEYUP:
                player.move = (0, 0)
            if player.hp == 0:
                exit = 2
                return
        all_sprites.update()
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in nps_group:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        hearts = pygame.sprite.Group()
        x = 10
        for i in range(player.hp):
            heart = Heart(x)
            heart.add(hearts)
            x += 30
        hearts.draw(screen)
        clock.tick(10)
        pygame.display.flip()


def show_level3():
    global all_sprites, nps_group, character_group, player_group, \
        hearts, player_image, tiles_group, player, clock, count, exit
    count = 0
    exit = 0
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    nps_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    character_group = pygame.sprite.Group()
    screen.fill(pygame.Color('white'))
    player, level_x, level_y, level = level_generate(load_level('level3.txt'))
    total_w = level_x * tile_width
    total_h = level_y * tile_width
    camera = Camera(camera_func, total_w, total_h)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = 1
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
                        player.move = (-5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (5, 0)
                if event.key == pygame.K_RIGHT:
                    if event.mod == 64:
                        player.right_attack((1, 0))
                    elif player.animation.die():
                        player.move = (5, 0)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (-5, 0)
                if event.key == pygame.K_UP:
                    if event.mod == 64:
                        player.up_attack((0, -1))
                    elif player.animation.die():
                        player.move = (0, -5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, 5)
                if event.key == pygame.K_DOWN:
                    if event.mod == 64:
                        player.down_attack((0, 1))
                    elif player.animation.die():
                        player.move = (0, 5)
                        for tile in tiles_group:
                            if pygame.sprite.collide_mask(player, tile) and not tile.move:
                                player.move = (0, -5)
                if count == 0:
                    return
            if event.type == pygame.KEYUP:
                player.move = (0, 0)
            if player.hp == 0:
                exit = 2
                return
        all_sprites.update()
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        for sprite in nps_group:
            screen.blit(sprite.image, camera.apply(sprite))
        screen.blit(player.image, camera.apply(player))
        hearts = pygame.sprite.Group()
        x = 10
        for i in range(player.hp):
            heart = Heart(x)
            heart.add(hearts)
            x += 30
        hearts.draw(screen)
        clock.tick(10)
        pygame.display.flip()


def main():
    start_screen()
    show_level1()
    if exit == 1:
        return
    elif exit == 2:
        game_over()
        for sprite in all_sprites:
            sprite.kill()
        player.kill()
        main()
    if exit == 0:
        show_level2()
        if exit == 1:
            return
        elif exit == 2:
            game_over()
            for sprite in all_sprites:
                sprite.kill()
            player.kill()
            main()
        if exit == 0:
            show_level3()
            if exit == 1:
                return
            elif exit == 2:
                game_over()
                for sprite in all_sprites:
                    sprite.kill()
                player.kill()
                main()
            if exit == 0:
                win_screen()
            else:
                return
        else:
            return
    else:
        return


main()
