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
        # Добавил летучих мышей)
        for i in range(1):
            self.enemies.append(Bat(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(0, 200)]))
        # Добавил зомбарей)
        for i in range(1):
            self.enemies.append(Zombie(start_position=[random.randint(0, SCREEN_WIDTH), random.randint(400, 700)]))

        self.main_loop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            self.player.motions(event)

    def render(self):
        #Прорисовка
        self.screen.blit(self.background, (0, 0))
        for enemy in self.enemies:
            enemy.render(self.screen)
        self.player.render(self.screen)
        pygame.display.flip()

    def main_loop(self):
        # Основной цикл программы
        while self.running is True:
            # self.player.motions()
            self.handle_events()
            for enemy in self.enemies:
                if enemy.name == "Zombie":
                    enemy.motions(self.player)
                else:
                    enemy.motions()
            self.render()


pygame.init()
game = Main()
