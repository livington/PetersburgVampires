"""
Файл для своих локальных общих функций
"""
import numpy as np
import pygame
import time
import random

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