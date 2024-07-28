from abc import ABC
import pygame
from constants import Type, Color, CELL_SIZE, ROBOT_SIZE, TARGET_SIZE

class Tile(ABC):
    pass

class Empty(Tile):
    def __init__(self, color=Color.WHITE):
        self.type = Type.EMPTY

    def draw(self, screen, x, y):
        pass

class Wall(Tile):
    def __init__(self, color=Color.BLACK):
        self.type = Type.WALL
        self.color = color

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, self.color.value, (x-CELL_SIZE//2, y-CELL_SIZE//2, CELL_SIZE, CELL_SIZE))

class Robot(Tile):
    def __init__(self, color=Color.RED, selected=False, on_target=False):
        self.type = Type.ROBOT
        self.color = color
        self.selected = selected
        self.on_target = on_target

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.color.value, (x, y), ROBOT_SIZE)
        if self.selected:
            pygame.draw.circle(screen, self.color.value, (x, y), ROBOT_SIZE+6, 4)

class Target(Tile):
    def __init__(self, color=Color.RED):
        self.type = Type.TARGET
        self.color = color

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, self.color.value, (x - TARGET_SIZE//2, y - TARGET_SIZE//2, TARGET_SIZE, TARGET_SIZE))