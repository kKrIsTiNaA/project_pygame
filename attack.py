import os
import sys

import pygame

pygame.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)


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
             "Подбирать предметы можно при помощи клавиши", "Enter. Удачи!",
             "Чтобы вернуться назад, нажмите Esc"]
    font3 = pygame.font.Font('data/18642.ttf', 32)
    text_coord = 30
    for line in text2:
        if ('Для передвижения' in line or 'атаки -' in line or
                'при помощи клавиши' in line or 'Удачи' in line or
                'Подсказка' in line):
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
                    return


def start_screen():
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
                        cursor.move_up()
                    elif event.key == pygame.K_DOWN:
                        cursor.move_down()
                    elif event.key == pygame.K_RETURN:
                        if cursor.rect.y == 245:
                            cursor.kill()
                            return
                        elif cursor.rect.y == 345:
                            show_rules()
                        else:
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
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def level_generate(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level)):
            if level[y][x] == '@':
                Tile(tile_images['s'], x, y)
                x1, y1 = x, y
            elif level[y][x] != 'm':
                Tile(tile_images[level[y][x]], x, y)
            else:
                Tile(tile_images['s'], x, y)
                # отрисовка монстра
    new_player = Character(x1, y1)
    return new_player, x, y


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def attack(self, direction):
        shell = Shell(self.x, self.y, 'fireball', direction)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_image, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Shell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type, direction):
        super().__init__(all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = shells[type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.direction = direction

    def update(self):
        self.rect = self.rect.move(self.direction[0], self.direction[1])


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - h // 2)


all_sprites = pygame.sprite.Group()
shells = {'fireball': pygame.transform.scale(load_image('fireball.png', (0, 0, 0)), (80, 50))}
tiles_group = pygame.sprite.Group()
tile_images = {'n': load_image('lb.png'), 'l': load_image('ln.png'),
               'r': load_image('stone2.png'), 's': load_image('sand2.png'),
               'f': load_image('flower12.png'), 't': load_image('pl2.png'),
               'w': load_image('water2.png'), 'v': load_image('pine_t2.png'),
               'j': load_image('pine_b2.png'), 'g': load_image('mushroom2.png'),
               'k': load_image('key2.png'), 'x': load_image('fish_water.png'),
               '+': load_image('bochka2.png'), 'b': load_image('timber2.png'),
               "'": load_image('left_bird2.png'),
               '"': load_image('right_bird2.png'), 'u': load_image('kust2.png'),
               'y': load_image('sv.png'), 'i': load_image('sn.png'),
               'o': load_image('kolodets2.png'), 'a': load_image('what2.png'),
               'z': load_image('fl22.png'), '1': load_image('h1_2.png'),
               '2': load_image('h2_2.png'), '3': load_image('h3_2.png'),
               '4': load_image('h4_2.png'), '5': load_image('h5.png'),
               '6': load_image('h6_2.png'), '7': load_image('h7_2.png'),
               '8': load_image('h8.png'), '9': load_image('h9_2.png'),
               '0': load_image('h10_2.png'), '#': load_image('h11_2.png'),
               '%': load_image('h12_2.png'), '*': load_image('h13_2.png'),
               '?': load_image('h14_2.png'), 'p': load_image('fish_water2.png')}
player_image = load_image('wizard.png', -1)
player_image = pygame.transform.scale(player_image, (80, 50))
tile_width = tile_height = 50
player = None
start_screen()
clock = pygame.time.Clock()
player_group = pygame.sprite.Group()
player, level_x, level_y = level_generate(load_level('level1.txt'))
camera = Camera()
camera.update(player)
for sprite in all_sprites:
    camera.apply(sprite)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(event.mod)
            if event.key == pygame.K_LEFT:
                if event.mod == 64:
                    player.attack((-1, 0))
                else:
                    player.rect.move_ip(player.get_x() - 10, player.get_y() - 4)
            if event.key == pygame.K_RIGHT:
                if event.mod == 64:
                    player.attack((1, 0))
                else:
                    player.rect.move_ip(player.get_x() + 10, player.get_y() - 4)
            if event.key == pygame.K_UP:
                if event.mod == 64:
                    player.attack((0, -1))
                else:
                    player.rect.move_ip(player.get_x() - 4, player.get_y() - 10)
            if event.key == pygame.K_DOWN:
                if event.mod == 64:
                    player.attack((0, 1))
                else:
                    player.rect.move_ip(player.get_x() - 4, player.get_y() + 10)
    screen.fill((255, 255, 255))
    all_sprites.update()
    all_sprites.draw(screen)
    clock.tick(200)
    pygame.display.flip()
