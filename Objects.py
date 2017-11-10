from lib import *
import pygame
from Persons import *


class CommonObjects:
    """class CommonObjects include public attributes and methods for all objects in the game world"""

    def __init__(self, image_path,
                 image_size,
                 start_position=[START_X, START_Y],
                 name="CommonObjects"):

        self.name = name
        self.image_path = image_path
        self.image_size = image_size
        self.position_np = np.array([start_position[X] + image_size[X] / 2,
                                     start_position[Y] + image_size[Y] / 2])

    def render(self, screen):
        screen.blit(pygame.image.load(self.image_path), (self.position_np[X],
                                                         self.position_np[Y]))


class MovingObjects(CommonObjects):
    """base class for all objects capable to move"""

    def __init__(self, image_path,
                 image_size,
                 speed,
                 start_position=[START_X, START_Y],
                 game_zone=GAME_ZONE_DEFAULT,
                 name="MovingObjects",
                 direction=random.choice([LEFT_np, RIGHT_np, UP_np, DOWN_np])):
        CommonObjects.__init__(self, image_path, image_size, start_position, name)
        self.state = ALIVE
        self.speed = speed
        self.game_zone = game_zone
        self.images = []
        self.animation = {'view': 0, 'count': 0}
        self.image_size = image_size
        """test NumPy"""
        self.direction_np = direction
        """test view zone"""
        self.visible_objects = None
        self.visible_distance = 0
        self.view_rad = 0
        """adding persons images: images[НАПРАВЛЕНИЕ][ВИД АНИМАЦИИ]"""
        temp = pygame.image.load(image_path).convert_alpha()
        for i in range(len([RIGHT, DOWN, LEFT, UP])):
            self.images.append([temp.subsurface(self.image_size[X] * j, self.image_size[Y] * i, self.image_size[X],
                                                self.image_size[Y])
                                for j in range(len([RIGHT, DOWN, LEFT, UP]))])

    def render(self, screen):
        screen.blit(self.images[dir_vec_to_base(self.direction_np)][self.animation['view']], (self.position_np[X],
                                                                                              self.position_np[Y]))

    def check_ability_to_move(self):
        """check motion ability"""

        if np.dot(self.direction_np, LEFT_np) == 1:
            if self.position_np[X] >= self.game_zone[X][MIN]:
                return True
            else:
                return False
        elif np.dot(self.direction_np, RIGHT_np) == 1:
            if self.position_np[X] <= self.game_zone[X][MAX]:
                return True
            else:
                return False
        elif np.dot(self.direction_np, DOWN_np) == 1:
            if self.position_np[Y] <= self.game_zone[Y][MAX]:
                return True
            else:
                return False
        elif np.dot(self.direction_np, UP_np) == 1:
            if self.position_np[Y] >= self.game_zone[Y][MIN]:
                return True
            else:
                return False

    def animation_moving(self):
        if self.animation['count'] < 7 - self.speed:
            self.animation['count'] += 1
        else:
            if self.animation['view'] < 2:
                self.animation['view'] += 1
            else:
                self.animation['view'] = 0
            self.animation['count'] = 0

    def take_step(self):
        self.position_np += self.speed * self.direction_np
        self.animation_moving()

    def motions(self):
        if self.check_ability_to_move():
            self.take_step()
            return True
        else:
            return False

    def reaction(self):
        pass
