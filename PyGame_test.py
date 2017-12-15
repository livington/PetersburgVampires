from Persons import *


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()


types = {
    'Zombie': type(Zombie)
}


def get_type(str_type):
    return types[str_type]
