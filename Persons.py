# -"- coding: utf-8 -"-
from lib import *
import numpy as np
from numpy.linalg import norm
from collections import deque


class Persons:
    """
    class Persons общий класс для всех персонажей, последующие классы наследуются от него, имеет общие атрибуты
    характерные для каждого класса
    """

    def __init__(self, image_path,
                 image_size,
                 speed=0,
                 start_position=[START_X, START_Y],
                 game_zone=GAME_ZONE_DEFAULT,
                 name="Person"):

        self.name = name
        self.HP = MAX_HP
        self.MP = MAX_MP
        self.state = ALIVE
        self.speed = speed
        self.game_zone = game_zone
        self.images = []
        self.animation = {'view': 0, 'count': 0}
        self.image_size = image_size
        """test NumPy"""
        self.direction_np = random.choice([LEFT_np, RIGHT_np, UP_np, DOWN_np])
        self.position_np = np.array([start_position[X] + image_size[X] / 2,
                                     start_position[Y] + image_size[Y] / 2])
        """test view zone"""
        self.visible_objects = None
        self.visible_distance = 0
        """adding persons images: images[НАПРАВЛЕНИЕ][ВИД АНИМАЦИИ]"""
        temp = pygame.image.load(image_path).convert_alpha()
        for i in range(len([RIGHT, DOWN, LEFT, UP])):
            self.images.append([temp.subsurface(self.image_size[X]*j, self.image_size[Y]*i, self.image_size[X],
                                                self.image_size[Y])
                                for j in range(len([RIGHT, DOWN, LEFT, UP]))])

    def render(self, screen):
        screen.blit(self.images[dir_vec_to_base(self.direction_np)][self.animation['view']], (self.position_np[X],
                                                                                              self.position_np[Y]))

    def render_ui(self, screen):
        pass

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


class Player(Persons):
    """
    class Player наследуется от Persons, переопределяю __init__ для записи по дефолту адресса изображений главного персонажа/игрока
    а также для записи зоны движения и названия экзмепляра. Характерным отличием евляется метод motions для определения движения игрока
    """

    def __init__(self, image_path=PLAYER_PNG_PATH,
                 image_size=PLAYER_SIZE,
                 speed=PLAYER_SPEED,
                 start_position=[START_X, START_Y],
                 game_zone=GAME_ZONE_DEFAULT,
                 name="Player"):
        Persons.__init__(self, image_path, image_size, speed, start_position, game_zone, name)
        self.event = pygame.event

    def motions(self):
        if self.event.type == pygame.KEYDOWN and self.event.key in [pygame.K_UP,
                                                          pygame.K_DOWN,
                                                          pygame.K_RIGHT,
                                                          pygame.K_LEFT]:
            self.state = MOVE
            """
            pygame.K_UP = 273
            pygame.K_DOWN = 274
            pygame.K_RIGHT = 275
            pygame.K_LEFT = 276
            
            pygame.K_UP - 273 = UP
            pygame.K_DOWN - 273 = DOWN
            pygame.K_RIGHT - 273 = RIGHT
            pygame.K_LEFT - 273 - LEFT
            """
            self.direction_np = dir_base_to_vec(self.event.key - 273)
            Persons.motions(self)

        if self.event.type == pygame.KEYUP \
                and self.event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]:
                self.state = STOP


class Enemy(Persons):
    """
    class Enemy is basic class for all enemies, пока просто переопределил инициализацию,
    и установил дефолтные значения для изображения
    """

    def __init__(self,
                 damage=0.05,
                 image_path=BAT_PNG_PATH,
                 image_size=VAMPIRE_SIZE,
                 speed=VAMPIRE_SPEED,
                 start_position=[START_X, START_Y],
                 game_zone=GAME_ZONE_DEFAULT,
                 name="Enemy"):
        Persons.__init__(self, image_path, image_size, speed, start_position, game_zone, name)
        self.damage = damage

    def motions(self):
        """ by default enemies goes from edge to edge, and spin randomly"""

        if random.randint(0, 100) == 5:
            self.direction_np = random.choice([LEFT_np, RIGHT_np, UP_np, DOWN_np])
        if Persons.motions(self) is False:
            self.direction_np = -1*self.direction_np

    def punch(self, player):
        """загатовка для атаки, каждую секунду уменьшае хп на велечинну урона для объекта"""

        player.HP -= self.damage
        print(player.HP)


class Bat(Enemy):
    def __init__(self, damage=0,
                 speed=VAMPIRE_SPEED,
                 image_path=BAT_PNG_PATH,
                 image_size=VAMPIRE_SIZE,
                 start_position=[START_X, START_Y],
                 game_zone=VAMPIRE_ZONE,
                 name="Bat"):
        Enemy.__init__(self, damage, image_path, image_size, speed, start_position, game_zone, name)


class Zombie(Enemy):
    def __init__(self, catch=150,
                 damage=0.5,
                 image_path=ZOMBIE_PNG_PATH,
                 image_size=ZOMBIE_SIZE,
                 speed=ZOMBIE_SPEED,
                 start_position=[START_X, START_Y],
                 game_zone=GAME_ZONE_DEFAULT,
                 name="Zombie"):
        Enemy.__init__(self, damage, image_path, image_size, speed, start_position, game_zone, name)
        self.state = MOVE
        self.catch = catch
        self.damage_zone = self.catch/5

    def motions(self):
        """test example for Zombies motions"""

        if self.state is MOVE:
            Enemy.motions(self)
        elif self.state is CATCH:
            Persons.motions(self)

    def reaction(self):
        """The reaction depends of the type of visible object"""

        if type(self.visible_objects) is Player:
            if 0 < self.visible_distance < 3:
                vec_distance, vec_enemy_view, distance = get_vec_view_and_distance(self.position_np,
                                                                                   self.visible_objects.position_np,
                                                                                   self.direction_np)
                self.state = CATCH
                """if Zombie see Player it will be move and won't change his direction"""
                # if vec_enemy_view > 0.1 and distance <= self.catch:
                #     self.state = CATCH
                #     # If zombie doesn't see Player it will turn to player
                # if self.damage_zone < distance <= self.catch:  # a trying to turn right
                #     temp = np.dot(self.direction_np.T, MTX_TURN_RIGHT)
                #     if np.dot(temp, self.visible_objects.position_np - self.position_np) > 0:
                #         # if it's ok, enemy will get temp direction
                #         self.direction_np = temp
                #     else:
                #         self.direction_np = -1 * temp  # either turn to left
                # if player are in damage zone, Zombie will attack him
                if distance < self.damage_zone:
                    self.punch(self.visible_objects)
                    self.state = STOP
            else:
                self.state = MOVE
            # pass
        elif type(self.visible_objects) is Zombie and self.state not in [CATCH, STOP]:
            if 0 < self.visible_distance < 3:
                vec_distance, vec_enemy_view, distance = get_vec_view_and_distance(self.position_np,
                                                                                   self.visible_objects.position_np,
                                                                                   self.direction_np)
                """if Zombie see Player it will be move and won't change his direction"""
                if vec_enemy_view > 0 and distance <= 15:
                    self.direction_np = -1 * self.direction_np
                    self.visible_objects.direction_np = -1 * self.visible_objects.direction_np
                # if self.damage_zone < distance <= self.catch:  # a trying to turn right
                #     temp = np.dot(self.direction_np.T, MTX_TURN_RIGHT)
                #     if np.dot(temp, self.visible_objects.position_np - self.position_np) > 0:
                #         # if it's ok, enemy will get temp direction
                #         self.direction_np = temp
                #     else:
                #         self.direction_np = -1 * temp  # either turn to left
            self.state = MOVE
        elif self.state is not STOP:
            self.state = MOVE

