from enum import Enum

WIDTH, HEIGHT = 800, 800
GRID_SIZE = 12
CENTER_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
ROBOT_SIZE = CELL_SIZE // 3 
TARGET_SIZE = CELL_SIZE // 2

class Type(Enum):
    EMPTY = 0
    WALL = 1
    ROBOT = 2
    TARGET = 3

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)