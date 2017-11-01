# -"- coding: utf-8 -"-
from lib import *
import numpy as np
from numpy.linalg import norm
from collections import deque

"""
class Persons общий класс для всех персонажей, последующие классы наследуются от него, имеет общие атрибуты
характерные для каждого класса
"""


class Persons:

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
        # self.direction = random.choice([LEFT, RIGHT, UP, DOWN])
        # self.position = start_position
        self.game_zone = game_zone
        self.images = []
        self.animation = {'view': 0, 'count': 0}
        self.image_size = image_size
        """test NumPy"""
        self.direction_np = random.choice([LEFT_np, RIGHT_np, UP_np, DOWN_np])
        self.position_np = np.array([start_position[X], start_position[Y]])
        """test view zone"""
        self.visible_objects = None
        self.input_msg = deque()
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

    """Test check visible obj or not"""
    def check_obj(self, obj):

        # vec_distance = obj.position_np - self.position_np
        # vec_enemy_view = np.dot(vec_distance, self.direction_np)
        #
        limit = [[self.position_np[X] - 200, self.position_np[X] + 200],
                 [self.position_np[Y] - 200, self.position_np[Y] + 200]]

        if obj.name not in self.visible_objects:
            if limit[X][MIN] < obj.position_np[X] < limit[X][MAX]:
                if limit[Y][MIN] < obj.position_np[Y] < limit[Y][MAX]:
                    # self.visible_objects.append(obj.name)
                    pass
        else:
            if (limit[X][MIN] < obj.position_np[X] < limit[X][MAX]) or (limit[Y][MIN] < obj.position_np[Y] < limit[Y][MAX]) is False:
                # self.visible_objects.remove(obj.name)
                pass

    def get_visible_obj(self, sub):
        limit = [[self.position_np[X] - 200, self.position_np[X] + 200],
                 [self.position_np[Y] - 200, self.position_np[Y] + 200]]

        if limit[X][MIN] < sub.position_np[X] < limit[X][MAX] and limit[Y][MIN] < sub.position_np[Y] < limit[Y][MAX]:
            self.visible_objects = sub
        else:
            self.visible_objects = None

    """check motion ability"""
    def check_ability_to_move(self):
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

"""
class Player наследуется от Persons, переопределяю __init__ для записи по дефолту адресса изображений главного персонажа/игрока
а также для записи зоны движения и названия экзмепляра. Характерным отличием евляется метод motions для определения движения игрока
"""


class Player(Persons):

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

    def __init__(self, damage=0.05,
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

        if self.state is not CATCH:
            Enemy.motions(self)

    def reaction(self):
        """Get a reaction depending of a type of visible object"""

        if type(self.visible_objects) is Player:
            vec_distance = self.visible_objects.position_np - (self.position_np - 5)
            vec_enemy_view = np.dot(vec_distance, self.direction_np)
            """if Zombie see Player it will be move and won't change his direction"""
            if vec_enemy_view > 0 and norm(vec_distance, 2) <= self.catch:
                self.state = CATCH
            # If zombie doesn't see Player it will turn to player
            elif self.damage_zone < norm(vec_distance, 2) <= self.catch:  # a trying to turn right
                temp = np.dot(self.direction_np.T, MTX_TURN_RIGHT)
                if np.dot(temp, self.visible_objects.position_np - self.position_np) > 0:
                    # if it ok we will save temp to enemy's direction
                    self.direction_np = temp
                else:
                    self.direction_np = -1 * temp  # either turn to left
            # if player are in damage zone Zombie will attack him
            elif norm(vec_distance, 2) < self.damage_zone:
                self.punch(self.visible_objects)
            # pass
        elif type(self.visible_objects) is Zombie and self.state is not CATCH:
            vec_distance = self.visible_objects.position_np - self.position_np
            vec_enemy_view = np.dot(vec_distance, self.direction_np)
            """if Zombie see Player it will be move and won't change his direction"""
            if vec_enemy_view > 0 and norm(vec_distance, 2) <= 5:
                self.direction_np = -1 * self.direction_np
                self.visible_objects.direction_np = -1 * self.visible_objects.direction_np
            self.state = MOVE
        else:
            self.state = MOVE

