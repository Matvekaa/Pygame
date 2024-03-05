import pygame
import random


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text_but, font_size, func=None, func_args=None, but_group=None, but_group_value=None,
                 color=(0, 0, 0), activ_color=(255, 255, 255), select_color=(10, 10, 10), font_color=(255, 255, 255),
                 border_color=(255, 255, 255), border_width=3, group=None):
        if group is not None:
            super().__init__(group)
        else:
            super().__init__()
        self.add(all_button_sprite)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.activ = False
        self.select = False

        self.but_group, self.but_group_value = but_group, but_group_value

        self.color, self.activ_color, self.select_color = color, activ_color, select_color
        self.border_color, self.border_width = border_color, border_width
        self.func = func
        self.func_args = func_args

        font = pygame.font.Font(None, font_size)
        self.text = font.render(text_but, True, font_color)
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()

        self.draw()

    def draw(self):
        if self.activ:
            self.image.fill(self.activ_color)
        elif self.select and not self.activ:
            self.image.fill(self.select_color)
        else:
            self.image.fill(self.color)
        self.image.blit(self.text, (self.image.get_width() // 2 - self.text_w // 2,
                        self.image.get_height() // 2 - self.text_h // 2))
        pygame.draw.rect(self.image, self.border_color,
                         pygame.Rect((0, 0), (self.rect.width, self.rect.height)), self.border_width)

    def check_select(self, pos):
        if self.rect.collidepoint(pos) and not self.select:
            self.select = True
            self.draw()
        elif not self.rect.collidepoint(pos) and self.select:
            self.select = False
            self.draw()

    def check_click(self, event, pos):
        if self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and not self.activ:
            self.activ = True
            if self.but_group is not None:
                self.but_group.new_select(self.but_group_value)
                if self.func:
                    for f, a in zip(self.func, self.func_args if self.func_args else [False * len(self.func)]):
                        if f and a:
                            f(*a)
                        elif self.func:
                            f()
            self.draw()
        elif self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONUP and self.activ and\
                self.but_group is None:
            self.activ = False
            self.draw()
            if self.func:
                for f, a in zip(self.func, self.func_args if self.func_args else [False * len(self.func)]):
                    if f and a:
                        f(*a)
                    elif self.func:
                        f()

    def get_value_group(self):
        return self.but_group_value

    def off(self):
        self.activ = False
        self.draw()

    def on(self):
        self.activ = True
        self.draw()

    def update(self, event=False):
        pos = pygame.mouse.get_pos()
        self.check_select(pos)
        if event:
            self.check_click(event, pos)


class Button_group:
    def __init__(self, value=0):
        self.value = value
        self.list_but = []

    def new_select(self, value):
        self.value = value
        for i in self.list_but:
            if i.get_value_group() != self.value:
                i.off()

    def get_value(self):
        return self.value

    def add_but(self, list_but):
        self.list_but += list_but


class Menu(pygame.sprite.Sprite):
    global menu_resul

    class rules_menu(pygame.sprite.Sprite):
        def __init__(self, group, func_back, size_menu=(1080, 720)):
            super().__init__(group)
            # основные настройки спрайта -------------------------------------------
            self.screen = screen
            self.size_menu = self.width, self.height = size_menu
            self.image = pygame.Surface(size_menu)
            self.rect = self.image.get_rect()

            self.func_back = func_back

            # переменные для отрисовки ----------------------------------------------
            self.menu_button = pygame.sprite.Group()

            font_main_title = pygame.font.Font(None, 120)
            self.main_title = font_main_title.render("ПРАВИЛА", True, (255, 255, 255))

            self.main_title_x = self.width // 2 - self.main_title.get_width() // 2
            self.main_title_y = self.height // 8 - self.main_title.get_height() // 2

            font_inf = pygame.font.Font(None, 35)
            self.inf = []
            inf_text = ["Цель игры — разложить карты по мастям в порядке от туза до 2 в четыре стопки.",
                        "Карту можно перекладывать на другую рангом ниже, но другого цвета.",
                        " В каждую из четырёх стопок, сначала кладутся Туз, затем Кароль, Дама и так далее.",
                        " В свободную ячейку (не дом) можно положить только 2."]
            for i in inf_text:
                self.inf.append(font_inf.render(i, True, (255, 255, 255)))

            but_back = Button((self.width - 160, 10),
                              (150, 50), "НАЗАД", 50,
                              border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1),
                              activ_color=(0, 150, 0),
                              func=(self.func_back,), group=self.menu_button)

        def draw(self):
            self.image.fill((2, 61, 1))
            self.image.blit(self.main_title, (self.main_title_x, self.main_title_y))
            for i, el in enumerate(self.inf):
                self.image.blit(el, (self.width // 2 - el.get_width() // 2,
                                     self.height // 8 * (i + 3) - self.main_title.get_height() // 2))
            self.menu_button.draw(self.image)

    def __init__(self, group, size_menu=(1080, 720)):
        super().__init__(group)
        # основные настройки спрайта -------------------------------------------
        self.screen = screen
        self.size_menu = self.width, self.height = size_menu
        self.image = pygame.Surface(size_menu)
        self.rect = self.image.get_rect()

        def update_open_screen_rules():
            self.open_frame = "main"
        self.rules_screen_sprite_group = pygame.sprite.Group()
        self.rules_screen = self.rules_menu(self.rules_screen_sprite_group, update_open_screen_rules, self.size_menu)

        # переменные для отрисовки ----------------------------------------------
        self.menu_button = pygame.sprite.Group()
        self.open_frame = "main"

        font_main_title = pygame.font.Font(None, 120)
        self.main_title = font_main_title.render("Шапка", True, (255, 255, 255))

        self.main_title_x = self.width // 2 - self.main_title.get_width() // 2
        self.main_title_y = self.height // 8 - self.main_title.get_height() // 2
        self.main_title_w = self.main_title.get_width()
        self.main_title_h = self.main_title.get_height()

        self.cap = pygame.image.load("data/textures/шапка_меню.png")
        colorkey_cap = self.cap.get_at((0, 0))
        self.cap.set_colorkey(colorkey_cap)

        # кнопки --------------------------------------------------------------------
        but_start = Button((self.width // 2 - 250, self.height // 7 * 3 - 40),
                           (500, 80), "ИГРАТЬ", 70,
                           border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                           group=self.menu_button, func=(self.exit_menu,))

        self.n_card_group = Button_group(value=52)

        but_36 = Button((self.width // 3 - 75, self.height // 7 * 4 - 40),
                        (150, 80), "36", 70,
                        border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                        group=self.menu_button, but_group=self.n_card_group, but_group_value=36)

        but_40 = Button((self.width // 2 - 75, self.height // 7 * 4 - 40),
                        (150, 80), "40", 70,
                        border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                        group=self.menu_button, but_group=self.n_card_group, but_group_value=40)

        but_52 = Button((self.width // 3 * 2 - 75, self.height // 7 * 4 - 40),
                        (150, 80), "52", 70,
                        border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                        group=self.menu_button, but_group=self.n_card_group, but_group_value=52)

        but_52.on()

        self.n_card_group.add_but((but_36, but_40, but_52))

        def update_open_screen_rules():
            self.open_frame = "rules"

        but_rules = Button((self.width // 2 - 250, self.height // 7 * 5 - 40),
                           (500, 80), "ПРАВИЛА", 70,
                           border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                           func=(update_open_screen_rules,),
                           func_args=(False,),
                           group=self.menu_button)

        but_quit = Button((self.width // 2 - 250, self.height // 7 * 6 - 40),
                          (500, 80), "ВЫХОД", 70,
                          border_color=(0, 150, 0), color=(2, 75, 1), select_color=(2, 51, 1), activ_color=(0, 150, 0),
                          func=(exit,), group=self.menu_button)

    def update(self, event=False):
        if self.open_frame == "main":
            self.draw_menu()
            self.menu_button.update(event)
            self.menu_button.draw(self.image)
        elif self.open_frame == "rules":
            self.rules_screen_sprite_group.draw(self.image)
            self.rules_screen.menu_button.update(event)
            self.rules_screen.menu_button.draw(self.rules_screen.image)

    def draw_menu(self):
        # сама отрисовка основного меню
        self.image.fill((2, 61, 1))
        self.image.blit(self.main_title, (self.main_title_x, self.main_title_y))
        pygame.draw.rect(self.image, (0, 150, 0), (self.main_title_x - 10, self.main_title_y - 10,
                                                   self.main_title_w + 20, self.main_title_h + 20), 3)

        self.image.blit(self.cap, (self.main_title_x - self.width / 15 - self.cap.get_width(), self.main_title_y / 2))
        self.image.blit(self.cap, (self.main_title_x + self.main_title_w + self.width / 15, self.main_title_y / 2))

        self.rules_screen.draw()

    def exit_menu(self):
        global menu_resul
        menu_resul = self.n_card_group.get_value()
        self.kill()


class Card(pygame.sprite.Sprite):
    anim_cross = [pygame.image.load(f"data/textures/cross.png"),
                  pygame.image.load(f"data/textures/cross_a1.png"),
                  pygame.image.load(f"data/textures/cross_a2.png"),
                  pygame.image.load(f"data/textures/cross_a1.png"),
                  pygame.image.load(f"data/textures/cross_a3.png"),
                  pygame.image.load(f"data/textures/cross_a1.png")]

    anim_peaks = [pygame.image.load(f"data/textures/peaks.png"),
                  pygame.image.load(f"data/textures/peaks_a1.png"),
                  pygame.image.load(f"data/textures/peaks_a2.png"),
                  pygame.image.load(f"data/textures/peaks_a1.png"),
                  pygame.image.load(f"data/textures/peaks_a3.png"),
                  pygame.image.load(f"data/textures/peaks_a1.png")]

    anim_heart = [pygame.image.load(f"data/textures/heart.png"),
                  pygame.image.load(f"data/textures/heart_a1.png"),
                  pygame.image.load(f"data/textures/heart_a2.png"),
                  pygame.image.load(f"data/textures/heart_a1.png"),
                  pygame.image.load(f"data/textures/heart_a3.png"),
                  pygame.image.load(f"data/textures/heart_a1.png")]

    anim_diamonds = [pygame.image.load(f"data/textures/diamonds.png"),
                     pygame.image.load(f"data/textures/diamonds_a1.png"),
                     pygame.image.load(f"data/textures/diamonds_a2.png"),
                     pygame.image.load(f"data/textures/diamonds_a1.png"),
                     pygame.image.load(f"data/textures/diamonds_a3.png"),
                     pygame.image.load(f"data/textures/diamonds_a1.png")]

    anim_jack = [pygame.image.load(f"data/textures/jack.png"),
                 pygame.image.load(f"data/textures/jack_a1.png"),
                 pygame.image.load(f"data/textures/jack_a2.png"),
                 pygame.image.load(f"data/textures/jack_a1.png"),
                 pygame.image.load(f"data/textures/jack_a3.png"),
                 pygame.image.load(f"data/textures/jack_a4.png")]

    anim_queen = [pygame.image.load(f"data/textures/queen.png"),
                  pygame.image.load(f"data/textures/queen_a1.png"),
                  pygame.image.load(f"data/textures/queen_a2.png"),
                  pygame.image.load(f"data/textures/queen_a1.png"),
                  pygame.image.load(f"data/textures/queen_a3.png"),
                  pygame.image.load(f"data/textures/queen_a4.png")]

    anim_king = [pygame.image.load(f"data/textures/king.png"),
                 pygame.image.load(f"data/textures/king_a1.png"),
                 pygame.image.load(f"data/textures/king_a2.png"),
                 pygame.image.load(f"data/textures/king_a1.png"),
                 pygame.image.load(f"data/textures/king_a3.png"),
                 pygame.image.load(f"data/textures/king_a4.png")]

    def __init__(self, group, type_card, pos):
        super().__init__(group)
        if type_card[0] == "c" and (int(type_card[1:]) < 11 or int(type_card[1:]) == 14):
            self.anim_card = self.anim_cross
        elif type_card[0] == "p" and (int(type_card[1:]) < 11 or int(type_card[1:]) == 14):
            self.anim_card = self.anim_peaks
        elif type_card[0] == "h" and (int(type_card[1:]) < 11 or int(type_card[1:]) == 14):
            self.anim_card = self.anim_heart
        elif type_card[0] == "d" and (int(type_card[1:]) < 11 or int(type_card[1:]) == 14):
            self.anim_card = self.anim_diamonds
        elif int(type_card[1:]) == 11:
            self.anim_card = self.anim_jack
        elif int(type_card[1:]) == 12:
            self.anim_card = self.anim_queen
        elif int(type_card[1:]) == 13:
            self.anim_card = self.anim_king

        self.image = self.anim_card[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Game(pygame.sprite.Sprite):
    def __init__(self, group, size_menu=(1080, 720)):
        super().__init__(group)
        # основные настройки спрайта -------------------------------------------
        self.screen = screen
        self.size_menu = self.width, self.height = size_menu
        self.image = pygame.Surface(size_menu)
        self.rect = self.image.get_rect()

        self.active = False


pygame.init()

# Settings
size = width, height = (1080, 720)
screen = pygame.display.set_mode(size)
fps = 60

# --------------------------
main_fps_clock = pygame.time.Clock()

all_button_sprite = pygame.sprite.Group()
all_menu = pygame.sprite.Group()
all_game = pygame.sprite.Group()

menu_resul = 0
menu = Menu(all_menu, size_menu=size)

game = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            if menu in all_menu:
                menu.update(event)
            # elif game in all:
            #     game.update(event)

    screen.fill((2, 61, 1))

    if menu in all_menu:
        all_menu.draw(screen)
        menu.update()
    if menu not in all_menu and not game:
        print(menu_resul)
        game = Game(all_game, size_menu=size)

    if game in all_game:
        all_game.draw(screen)
        game.update()

    pygame.display.flip()

    main_fps_clock.tick(60)
pygame.quit()