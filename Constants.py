import numpy as np

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

SCREEN_WIDTH_np = np.array([SCREEN_WIDTH, 0])
SCREEN_HEIGHT_np = np.array([0, SCREEN_HEIGHT])

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

UP_np = np.array([0, -1])
DOWN_np = np.array([0, 1])
RIGHT_np = np.array([1, 0])
LEFT_np = np.array([-1, 0])

MTX_TURN_RIGHT = np.array([[0, -1], [1, 0]])
MTX_TURN_LEFT = np.array([[0, 1], [-1, 0]])

ALIVE = 0
DEAD = 1
MOVE = 3
STOP = -1

"""base game state constants"""
FIRST_ENTER = 0
GAME = 1
PAUSE = 2
END = 3

X = 0
Y = 1
D = 2

MIN = 0
MAX = 1

START_X = 300
START_Y = 700

MAX_HP = 100
MAX_MP = 100

PLAYER_SIZE = [64, 64]
VAMPIRE_SIZE = [64, 64]
ZOMBIE_SIZE = [32, 64]

PLAYER_SPEED = 5
VAMPIRE_SPEED = 2
ZOMBIE_SPEED = 1

PLAYER_PNG_PATH = "data/player.png"
BAT_PNG_PATH = "data/vampire2.png"
ZOMBIE_PNG_PATH = "data/zombie3.png"
BACK_GROUND_PATH = 'data/background.jpg'
START_BUTTON_PATH = 'data/start.png'
END_BUTTON_PATH = 'data/end.png'

GAME_ZONE_DEFAULT = [[0, SCREEN_WIDTH], [SCREEN_HEIGHT/3 + 60, SCREEN_HEIGHT]]
VAMPIRE_ZONE = [[0, SCREEN_WIDTH], [0, SCREEN_HEIGHT/4]]

GRAD_TO_RAD = 0.0174533