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
        self.all_objects = []
        # self.all_objects.append(self.player)
        """init pygame"""
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('C:\Windows\Fonts\Arial.TTF', 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.state == FIRST_ENTER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    self.state = GAME
                    self.player.event = event
            elif self.state == GAME:
                self.player.event = event
            elif self.state == END:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.state = GAME
                    elif event.key == pygame.K_n:
                        self.running = False

    def render(self):
        """rendering"""
        self.screen.blit(self.background, (0, 0))

        """work with ever game state"""
        if self.state == FIRST_ENTER:
            """welcome screen))"""
            self.screen.blit(pygame.image.load(START_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))
        elif self.state == GAME:
            """rendering enemies and player"""
            for obj in self.all_objects:
                obj.render(self.screen)
            # self.player.render(self.screen)
            """rendering HP status"""
            text = self.font.render("HP: " + str(self.player.HP), True, (255, 0, 0))
            self.screen.blit(text, (0, 10))
        elif self.state == END:
            """The end screen"""
            self.screen.blit(pygame.image.load(END_BUTTON_PATH), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 8))

        pygame.display.flip()

    def add_enemies(self):
        """add all enemies"""

        for i in range(1):
            self.all_objects.append(Bat(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(0, 200)]))
        """adding zombies, half to left side and half to other"""
        for i in range(ZOMBIES_AMOUNT):
            self.all_objects.append(Zombie(name="zombie " + str(i), start_position=[SCREEN_WIDTH*int(i > ZOMBIES_AMOUNT / 2),
                                                       random.randint(400, 700)]))
        # self.all_objects.extend(self.enemies)

    """check all objects"""
    def check_all_objects(self):
        for main_obj in self.enemies:
            for sub_obj in self.enemies:
                # if sub_obj not in main_obj.visible_objects:
                main_obj.check_obj(sub_obj)
                # pass

    def check_player_hp(self):
        if self.player.HP <= 0:
            self.state = END

    def main_loop(self):
        """Основной цикл программы"""

        old_k_delay, old_k_interval = pygame.key.get_repeat()
        pygame.key.set_repeat(50, 50)
        try:
            while self.running is True:
                self.render()
                self.handle_events()

                if self.state == GAME:
                    if old_state in [FIRST_ENTER, END]:
                        self.player.HP = MAX_HP
                        self.all_objects.append(self.player)
                        self.add_enemies()
                    for main_obj in self.all_objects:
                        for sub_obj in self.all_objects:
                            if main_obj is not sub_obj:
                                main_obj.get_visible_obj(sub_obj)
                                main_obj.reaction()
                        main_obj.motions()
                    self.check_player_hp()
                    pygame.display.flip()
                elif self.state == END:
                    self.all_objects = []

                old_state = self.state
        finally:
            pygame.key.set_repeat(old_k_delay, old_k_interval)
            pygame.quit()

if __name__ == '__main__':
    game = Main()
    game.main_loop()
