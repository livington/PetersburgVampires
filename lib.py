"""
Файл для своих локальных общих функций
"""
import time
import random
from numba import jit
from numpy.linalg import norm

from Constants import *


def check_position(position, limit):
    return limit[X][MIN] < position[X] < limit[X][MAX] and limit[Y][MIN] < position[Y] <= limit[Y][MAX]


def check_vec_position(position):
    if np.dot(SCREEN_WIDTH_np, position) < 0 or np.dot(SCREEN_HEIGHT_np, position) < 0:
        return False
    else:
        return True


def dir_vec_to_base(direction):
    if direction is UP_np:
        return UP
    elif direction is DOWN_np:
        return DOWN
    elif direction is RIGHT_np:
        return RIGHT
    elif direction is LEFT_np:
        return LEFT
    else:
        return False


def dir_base_to_vec(direction):
    if direction == UP:
        return UP_np
    elif direction == DOWN:
        return DOWN_np
    elif direction == RIGHT:
        return RIGHT_np
    elif direction == LEFT:
        return LEFT_np
    else:
        return False


def get_visible_obj(main, sub):
    limit = [[main.position_np[X] - 200, main.position_np[X] + 200],
             [main.position_np[Y] - 200, main.position_np[Y] + 200]]

    if limit[X][MIN] < sub.position_np[X] < limit[X][MAX] and limit[Y][MIN] < sub.position_np[Y] < limit[Y][MAX]:
        main.visible_objects = sub
    else:
        main.visible_objects = None


def by_position_x_get_key(obj):
    return obj.position_np[X]


@jit()
def get_grid_xy(position_np, obj_size):
    x = int((position_np[X] + obj_size[X] / 2) / obj_size[X] * 2)
    y = int((position_np[Y] + obj_size[Y] / 2) / obj_size[Y] * 2)

    if x < 0:
        x = 0
    else:
        if x >= GRID_WIDTH:
            x = GRID_WIDTH - 1
    if y < 0:
        y = 0
    else:
        if y >= GRID_HEIGHT:
            y = GRID_HEIGHT - 1

    return x, y


@jit()
def get_distance(vec_distance):
    return norm(vec_distance, 2)


def get_vec_view_and_distance(first_position_np, second_position_np, direction_np):
    vec_distance = second_position_np - first_position_np
    vec_enemy_view = np.dot(vec_distance, direction_np)
    distance = get_distance(vec_distance)

    return vec_distance, vec_enemy_view, distance


# @jit()
def get_grid_visible(direction_np, rad):
    if np.dot(direction_np, UP_np) == 1 or np.dot(direction_np, DOWN_np) == 1:
        radx = [-rad, rad + 2]
        if np.dot(direction_np, UP_np) == 1:
            rady = [-rad, 1]
        else:
            rady = [0, rad + 1]
    else:
        rady = [-rad, rad + 1]
        if np.dot(direction_np, RIGHT_np) == 1:
            radx = [0, rad + 1]
        else:
            radx = [-rad, 1]
    return radx, rady
