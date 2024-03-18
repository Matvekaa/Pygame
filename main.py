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
                            sound_button.play()
                            f(*a)
                        elif self.func:
                            sound_button.play()
                            f()
            self.draw()
        elif self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONUP and self.activ and\
                self.but_group is None:
            self.activ = False
            self.draw()
            if self.func:
                for f, a in zip(self.func, self.func_args if self.func_args else [False * len(self.func)]):
                    if f and a:
                        sound_button.play()
                        f(*a)
                    elif self.func:
                        sound_button.play()
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
        sound_button.play()

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
                        "В каждую из четырёх стопок, сначала кладутся Туз, затем Кароль, Дама и так далее.",
                        "В свободную ячейку (не дом) можно положить только 2.",
                        "Перекладывать можно только по одной карте."]
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
        sound_start.play()
        self.kill()


class Card(pygame.sprite.Sprite):
    def __init__(self, group, type_card, pos, is_hiden=False):
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

        self.shirt_skin = pygame.image.load("data/textures/shirt.png")

        super().__init__(group)

        self.level = int(type_card[1:])
        self.type_card = type_card

        self.is_hiden = is_hiden

        if type_card[0] == "c" and (self.level < 11 or self.level == 14):
            self.anim_card = anim_cross
        elif type_card[0] == "p" and (self.level < 11 or self.level == 14):
            self.anim_card = anim_peaks
        elif type_card[0] == "h" and (self.level < 11 or self.level == 14):
            self.anim_card = anim_heart
        elif type_card[0] == "d" and (self.level < 11 or self.level == 14):
            self.anim_card = anim_diamonds
        elif self.level == 11:
            self.anim_card = anim_jack
        elif self.level == 12:
            self.anim_card = anim_queen
        elif self.level == 13:
            self.anim_card = anim_king

        if type_card[0] == "c":
            self.sim = pygame.image.load("data/textures/cross_sim.png")
        elif type_card[0] == "h":
            self.sim = pygame.image.load("data/textures/heart_sim.png")
        elif type_card[0] == "p":
            self.sim = pygame.image.load("data/textures/peaks_sim.png")
        elif type_card[0] == "d":
            self.sim = pygame.image.load("data/textures/diamonds_sim.png")

        self.n_anim = 0
        self.image = self.anim_card[self.n_anim]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if self.is_hiden:
            self.hide()
        else:
            self.draw_level()

    def draw_level(self):
        font = pygame.font.Font(None, 45)
        if self.level <= 10:
            level_text = str(self.level)
        elif self.level == 11:
            level_text = "J"
        elif self.level == 12:
            level_text = "Q"
        elif self.level == 13:
            level_text = "K"
        elif self.level == 14:
            level_text = "A"
        level_r = font.render(level_text, True, (156, 0, 0) if self.type_card[0] in ("h", "d") else (0, 0, 0))
        self.image.blit(level_r, (7, 7))
        self.image.blit(pygame.transform.rotate(level_r, 180), (self.rect.width - level_r.get_width() - 7,
                                                                self.rect.height - level_r.get_height() - 7))
        self.image.blit(self.sim, (self.rect.width - 25 - 7, 7))
        self.image.blit(pygame.transform.rotate(self.sim, 180), (7, self.rect.height - 25 - 7))

    def update_anim(self):
        self.n_anim += 1
        self.n_anim = self.n_anim % 6
        self.image = self.anim_card[self.n_anim]
        self.draw_level()

    def hide(self):
        self.image = self.shirt_skin

    def show(self):
        self.n_anim -= 1
        self.update_anim()
        self.draw_level()


class Stack(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)

        # основные настройки спрайта -------------------------------------------
        self.image = pygame.image.load("data/textures/shirt_place.png")
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.list_card = []
        self.list_obj_card = []


class Deck_obj(pygame.sprite.Sprite):
    def __init__(self, group, pos, list_card):
        super().__init__(group)

        # основные настройки спрайта -------------------------------------------
        self.image = pygame.image.load("data/textures/shirt_place.png")
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.list_card = list_card
        self.list_obj_card = []


class Deck_stack(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)

        # основные настройки спрайта -------------------------------------------
        self.image = pygame.image.load("data/textures/shirt_place.png")
        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.list_card = []
        self.list_obj_card = []


class Home(pygame.sprite.Sprite):
    def __init__(self, group, pos, type_home):
        super().__init__(group)

        # основные настройки спрайта -------------------------------------------
        if type_home == "c":
            self.image = pygame.image.load("data/textures/cross_home.png")
        elif type_home == "p":
            self.image = pygame.image.load("data/textures/peaks_home.png")
        elif type_home == "d":
            self.image = pygame.image.load("data/textures/diamonds_home.png")
        elif type_home == "h":
            self.image = pygame.image.load("data/textures/heart_home.png")

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.list_card = []
        self.list_obj_card = []

        self.type_home = type_home


class Game(pygame.sprite.Sprite):
    def __init__(self, group, size_menu=(1080, 720)):
        super().__init__(group)
        # основные настройки спрайта -------------------------------------------
        self.screen = screen
        self.size_menu = self.width, self.height = size_menu
        self.image = pygame.Surface(size_menu)
        self.rect = self.image.get_rect()

        self.win_image = pygame.image.load("data/textures/win.png")
        self.win_x = -self.win_image.get_rect().width
        self.new_record = False

        self.active = False

        self.is_drag = False
        self.is_drag_deck = False

        self.n_step = 0
        self.font_inf = pygame.font.Font(None, 35)
        self.font_win_inf = pygame.font.Font(None, 60)

        self.group_card = pygame.sprite.Group()
        self.group_deck = pygame.sprite.Group()
        self.group_stack = pygame.sprite.Group()

        self.deck = []

        if menu_resul == 52:
            for i in range(2, 15):
                for j in ("c", "p", "h", "d"):
                    self.deck.append(f"{j}{i}")
        elif menu_resul == 40:
            for i in range(5, 15):
                for j in ("c", "p", "h", "d"):
                    self.deck.append(f"{j}{i}")
        elif menu_resul == 36:
            for i in range(2, 11):
                for j in ("c", "p", "h", "d"):
                    self.deck.append(f"{j}{i}")

        # дом
        self.home_list = []
        types_homes = ("c", "p", "h", "d")
        for i in range(3, 7):
            self.home_list.append(Home(self.group_stack, (130 * i + 20 * i + 25, 10), types_homes[i - 3]))

        # self.home_list[-1].list_card += [str(i) for i in range(52)] # test win

        # стопки
        self.stacks_list = []
        for i in range(7):
            self.stacks_list.append(Stack(self.group_stack, (130 * i + 20 * i + 25, 210)))

        for i, el in enumerate(self.stacks_list[::-1]):
            el.list_card = [self.deck.pop(random.randrange(len(self.deck))) for j in range(i + 1)]

        for i in range(7):
            for j in range(len(self.stacks_list[i].list_card)):
                self.stacks_list[i].list_obj_card. append(Card(self.group_card, self.stacks_list[i].list_card[j],
                                                              (self.stacks_list[i].rect.x,
                                                               self.stacks_list[i].rect.y + 35 * j),
                                                               not j == len(self.stacks_list[i].list_card) - 1))

        # калода
        for i in range(len(self.deck)):
            r1 = random.randrange(len(self.deck))
            r2 = random.randrange(len(self.deck))
            self.deck[r1], self.deck[r2] = self.deck[r2], self.deck[r1]

        self.deck_obj = Deck_obj(self.group_deck, (25, 10), self.deck)
        self.deck_stack = Deck_stack(self.group_deck, (175, 10))
        for i in self.deck_obj.list_card:
            self.deck_obj.list_obj_card.append(Card(self.group_card, i, (25, 10), True))



        # Card(self.group_card, f"c2", (0 * 130, 0 * 180))
        # Card(self.group_card, f"c3", (1 * 130, 0 * 180))

        # for i, t in enumerate(("c", "h", "p", "d")):
        #     for j in range(8, 15):
        #         Card(self.group_card, f"{t}{j}", ((j - 8) * 130, i * 180))

    def draw_game(self):
        self.image.fill((2, 61, 1))
        self.group_stack.draw(self.image)
        self.group_deck.draw(self.image)
        self.group_card.draw(self.image)
        rend = self.font_inf.render(str(self.n_step), True, (255, 255, 255))
        self.image.blit(rend, (self.rect.width - rend.get_rect().width - 3,
                               self.rect.height - rend.get_rect().height - 3))


    def draw_win(self):
        if self.win_x < self.rect.width / 2 - self.win_image.get_rect().width / 2:
            self.win_x += 5
        else:
            if not self.new_record:
                with open("data/win.txt", "r") as f:
                    record = int(f.read())
                if record > self.n_step:
                    with open("data/win.txt", "w") as f:
                        f.write(str(self.n_step))
                    self.record = self.n_step
                else:
                    self.record = record
                sound_win.play()
                self.new_record = True

            rend = self.font_win_inf.render(f'Ваш результат: {self.n_step}', True, (255, 255, 255))
            rend1 = self.font_win_inf.render(f'Рекорд: {self.record}', True, (255, 255, 255))
            self.image.blit(rend, (self.rect.width / 2 - rend.get_rect().width / 2, 620))
            self.image.blit(rend1, (self.rect.width / 2 - rend1.get_rect().width / 2, 680))

        self.image.blit(self.win_image, (self.win_x, 0))

    def update(self, event=False):
        self.draw_game()
        if sum([len(self.home_list[i].list_card) for i in range(4)]) == menu_resul:
            self.draw_win()
        if event:
            if event.type == ANIM_TICK:
                for i in self.home_list:
                    if i.list_obj_card:
                        i.list_obj_card[-1].update_anim()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(7):
                    if ((self.stacks_list[i].list_obj_card and
                         self.stacks_list[i].list_obj_card[-1].rect.collidepoint(pygame.mouse.get_pos())) or
                            (not self.stacks_list[i].list_obj_card and
                             self.stacks_list[i].rect.collidepoint(pygame.mouse.get_pos()))):
                        self.is_drag = True
                        sound_card_up.play()
                        self.drag_obj = self.stacks_list[i].list_obj_card[-1]
                        self.drag_start_coord = (self.drag_obj.rect.x,
                                                 self.drag_obj.rect.y)
                        self.drag_stack = i

                        self.drag_obj.remove(self.group_card)
                        self.drag_obj.add(self.group_card)

                        print("drag!")
                        break

                if not self.is_drag and not self.is_drag_deck:
                    if self.deck_obj.rect.collidepoint(pygame.mouse.get_pos()):
                        sound_card_up.play()
                        if self.deck_obj.list_card:
                            self.deck_stack.list_card.append(self.deck_obj.list_card[-1])
                            self.deck_stack.list_obj_card.append(self.deck_obj.list_obj_card[-1])

                            del self.deck_obj.list_card[-1]
                            del self.deck_obj.list_obj_card[-1]

                            self.deck_stack.list_obj_card[-1].rect.x = self.deck_stack.rect.x
                            self.deck_stack.list_obj_card[-1].rect.y = self.deck_stack.rect.y

                            self.deck_stack.list_obj_card[-1].show()

                            self.deck_stack.list_obj_card[-1].remove(self.group_card)
                            self.deck_stack.list_obj_card[-1].add(self.group_card)

                            self.n_step += 1
                        else:
                            self.deck_obj.list_card = self.deck_stack.list_card[::-1]
                            self.deck_obj.list_obj_card = self.deck_stack.list_obj_card[::-1]

                            self.deck_stack.list_card = []
                            self.deck_stack.list_obj_card = []

                            for i in self.deck_obj.list_obj_card:
                                i.hide()
                                i.rect.x = self.deck_obj.rect.x
                                i.rect.y = self.deck_obj.rect.y
                                i.remove(self.group_card)
                                i.add(self.group_card)

                    # elif self.deck_stack.list_obj_card[-1].rect.collidepoint(pygame.mouse.get_pos()):
                    #     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ^ ^ ^ ^
                    # debug complite
                    elif (self.deck_stack.list_obj_card and
                          self.deck_stack.list_obj_card[-1].rect.collidepoint(pygame.mouse.get_pos())):
                        print('start drag deck')
                        self.is_drag_deck = True
                        sound_card_up.play()
                        self.drag_deck_obj = self.deck_stack.list_obj_card[-1]
                        self.drag_deck_start_coord = (self.drag_deck_obj.rect.x, self.drag_deck_obj.rect.y)

                        self.drag_deck_obj.remove(self.group_card)
                        self.drag_deck_obj.add(self.group_card)

            if event.type == pygame.MOUSEMOTION:
                if self.is_drag:
                    self.drag_obj.rect.x += event.rel[0]
                    self.drag_obj.rect.y += event.rel[1]
                if self.is_drag_deck:
                    self.drag_deck_obj.rect.x += event.rel[0]
                    self.drag_deck_obj.rect.y += event.rel[1]

            if event.type == pygame.MOUSEBUTTONUP:
                is_collider_stack = False
                is_collider_home = False
                if self.is_drag:
                    for i in range(7):
                        if ((self.stacks_list[i].list_obj_card and
                                (pygame.Rect.colliderect(self.drag_obj.rect,
                                                         self.stacks_list[i].list_obj_card[-1].rect)
                                 and self.drag_obj is not self.stacks_list[i].list_obj_card[-1])) or
                                (not self.stacks_list[i].list_obj_card and
                                (pygame.Rect.colliderect(self.drag_obj.rect,
                                                         self.stacks_list[i].rect)))):

                            is_collider_stack = True

                            print("colliderect:", i)

                            if self.check_drag(self.stacks_list[i].list_card, self.drag_obj.type_card):

                                self.n_step += 1
                                del self.stacks_list[self.drag_stack].list_obj_card[-1]
                                del self.stacks_list[self.drag_stack].list_card[-1]

                                self.stacks_list[i].list_obj_card.append(self.drag_obj)
                                self.stacks_list[i].list_card.append(self.drag_obj.type_card)

                                self.drag_obj.rect.x = self.stacks_list[i].rect.x
                                self.drag_obj.rect.y = self.stacks_list[i].rect.y + (len(self.stacks_list[i].list_card) - 1) * 35

                                if (self.stacks_list[self.drag_stack].list_card and
                                        self.stacks_list[self.drag_stack].list_obj_card[-1].is_hiden):
                                    self.stacks_list[self.drag_stack].list_obj_card[-1].show()
                            else:
                                self.drag_obj.rect.x = self.drag_start_coord[0]
                                self.drag_obj.rect.y = self.drag_start_coord[1]

                    if not is_collider_stack:
                        for i in range(4):
                            if pygame.Rect.colliderect(self.drag_obj.rect, self.home_list[i].rect):
                                is_collider_home = True
                                if self.check_drag_to_home(self.home_list[i], self.drag_obj.type_card):

                                    self.n_step += 1
                                    del self.stacks_list[self.drag_stack].list_obj_card[-1]
                                    del self.stacks_list[self.drag_stack].list_card[-1]

                                    self.home_list[i].list_obj_card.append(self.drag_obj)
                                    self.home_list[i].list_card.append(self.drag_obj.type_card)

                                    self.drag_obj.rect.x = self.home_list[i].rect.x
                                    self.drag_obj.rect.y = self.home_list[i].rect.y

                                    if (self.stacks_list[self.drag_stack].list_card and
                                            self.stacks_list[self.drag_stack].list_obj_card[-1].is_hiden):
                                        self.stacks_list[self.drag_stack].list_obj_card[-1].show()

                                    sound_down_to_home.play()

                                else:
                                    self.drag_obj.rect.x = self.drag_start_coord[0]
                                    self.drag_obj.rect.y = self.drag_start_coord[1]

                    if (not is_collider_stack) and (not is_collider_home):
                        print("error drag")
                        print((not is_collider_stack), (not is_collider_home))
                        self.drag_obj.rect.x = self.drag_start_coord[0]
                        self.drag_obj.rect.y = self.drag_start_coord[1]


                    self.is_drag = False
                    sound_card_down.play()

                elif self.is_drag_deck:
                    is_collider_stack_deck = False
                    is_collider_home_deck = False

                    # тут оштбка! не будет работать с пустым слотом debug complite
                    for i in range(7):
                        if ((self.stacks_list[i].list_obj_card and
                             (pygame.Rect.colliderect(self.drag_deck_obj.rect,
                                                      self.stacks_list[i].list_obj_card[-1].rect))) or
                                (not self.stacks_list[i].list_obj_card and
                                 (pygame.Rect.colliderect(self.drag_deck_obj.rect, self.stacks_list[i].rect)))):
                            is_collider_stack_deck = True

                            print("colliderect:", i, 'deck -> stack')

                            if self.check_drag(self.stacks_list[i].list_card, self.drag_deck_obj.type_card):
                                print("good")

                                self.n_step += 1
                                del self.deck_stack.list_obj_card[-1]
                                del self.deck_stack.list_card[-1]

                                self.stacks_list[i].list_obj_card.append(self.drag_deck_obj)
                                self.stacks_list[i].list_card.append(self.drag_deck_obj.type_card)

                                self.drag_deck_obj.rect.x = self.stacks_list[i].rect.x
                                self.drag_deck_obj.rect.y = (self.stacks_list[i].rect.y +
                                                             (len(self.stacks_list[i].list_card) - 1) * 35)

                            else:
                                self.drag_deck_obj.rect.x = self.drag_deck_start_coord[0]
                                self.drag_deck_obj.rect.y = self.drag_deck_start_coord[1]

                    if not is_collider_stack_deck:
                        for i in range(4):
                            if pygame.Rect.colliderect(self.drag_deck_obj.rect, self.home_list[i].rect):
                                print('deck -> home')
                                is_collider_home_deck = True
                                if self.check_drag_to_home(self.home_list[i], self.drag_deck_obj.type_card):

                                    self.n_step += 1
                                    del self.deck_stack.list_obj_card[-1]
                                    del self.deck_stack.list_card[-1]

                                    self.home_list[i].list_obj_card.append(self.drag_deck_obj)
                                    self.home_list[i].list_card.append(self.drag_deck_obj.type_card)

                                    self.drag_deck_obj.rect.x = self.home_list[i].rect.x
                                    self.drag_deck_obj.rect.y = self.home_list[i].rect.y

                                    sound_down_to_home.play()

                                else:
                                    self.drag_deck_obj.rect.x = self.drag_deck_start_coord[0]
                                    self.drag_deck_obj.rect.y = self.drag_deck_start_coord[1]

                    if (not is_collider_stack_deck) and (not is_collider_home_deck):
                        print("error drag (deck)")
                        print((not is_collider_stack_deck), (not is_collider_home_deck))
                        self.drag_deck_obj.rect.x = self.drag_deck_start_coord[0]
                        self.drag_deck_obj.rect.y = self.drag_deck_start_coord[1]

                    self.is_drag_deck = False
                    sound_card_down.play()

                for i in self.stacks_list:
                    print(i.list_card)


    def check_drag_to_home(self, home, card):
        if home.list_card:
            if card[0] == home.type_home and int(home.list_card[-1][1:]) - int(card[1:]) == 1:
                return True
        else:
            if menu_resul in (52, 40):
                if card[0] == home.type_home and int(card[1:]) == 14:
                    return True
            elif menu_resul == 36:
                if card[0] == home.type_home and int(card[1:]) == 10:
                    return True
        return False

    def check_drag(self, stack, card):
        if stack:
            if int(card[1:]) - int(stack[-1][1:]) == 1 and ((stack[-1][0] in ("c", "p") and card[0] in ("h", "d")) or (stack[-1][0] in ("h", "d") and card[0] in ("c", "p"))):
                return True
        else:
            if int(card[1:]) == 2:
                return True
        return False


pygame.init()

# Settings
size = width, height = (1080, 850)
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

ANIM_TICK = pygame.USEREVENT + 1
pygame.time.set_timer(ANIM_TICK, 700)

pygame.mixer.music.load('data/music/djazz.mp3')
for i in range(20):
    pygame.mixer.music.queue('data/music/djazz.mp3')
pygame.mixer.music.play()

sound_start = pygame.mixer.Sound('data/music/start.mp3')
sound_button = pygame.mixer.Sound('data/music/button.mp3')

sound_card_up = pygame.mixer.Sound('data/music/card_up.mp3')
sound_card_down = pygame.mixer.Sound('data/music/card_dawn.mp3')

sound_down_to_home = pygame.mixer.Sound('data/music/down_to_home.mp3')

sound_win = pygame.mixer.Sound('data/music/win.mp3')

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            if menu in all_menu:
                menu.update(event)
            elif game in all_game:
                game.update(event)
        if event.type == pygame.MOUSEMOTION:
            if game in all_game:
                game.update(event)
        if event.type == ANIM_TICK:
            if game in all_game:
                game.update(event)

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