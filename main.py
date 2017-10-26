# -"- coding: utf-8 -"-
from Persons import *
import sys


class Main:
    def __init__(self, screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))):
        self.screen = screen
        self.player = Player()
        self.enemies = []
        self.background = pygame.image.load(BACK_GROUND_PATH)
        self.running = True
        self.state = FIRST_ENTER

        # self.add_enemies()
        # self.main_loop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.state == FIRST_ENTER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    self.state = GAME
            elif self.state == GAME:
                self.player.motions(event)
            elif self.state == END:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.state = GAME
                    elif event.key == pygame.K_n:
                        self.running = False

    def render(self):
        # rendering
        self.screen.blit(self.background, (0, 0))

        if self.state == FIRST_ENTER:
            self.screen.blit(pygame.image.load(START_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))
        elif self.state == GAME:
            self.screen.blit(self.background, (0, 0))
            for enemy in self.enemies:
                enemy.render(self.screen)
            self.player.render(self.screen)
        elif self.state == END:
            self.screen.blit(pygame.image.load(END_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))

        pygame.display.flip()

    def add_enemies(self):
        # Добавил летучих мышей)
        for i in range(10):
            self.enemies.append(Bat(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(0, 200)]))
        # Добавил зомбарей)
        for i in range(100):
            self.enemies.append(Zombie(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(400, 700)]))

    def check_player_hp(self):
        if self.player.HP <= 0:
            self.state = END

    def main_loop(self):
        # Основной цикл программы
        while self.running is True:
            # self.player.motions()
            # self.check_player_hp()
            self.render()
            self.handle_events()

            if self.state == GAME:
                if old_state in [FIRST_ENTER, END]:
                    self.player.HP = MAX_HP
                    self.add_enemies()
                for enemy in self.enemies:
                    if enemy.name == "Zombie":
                        enemy.motions(self.player)
                    else:
                        enemy.motions()
                self.check_player_hp()
            elif self.state == END:
                self.enemies = []

            old_state = self.state


pygame.init()
game = Main()
game.main_loop()
