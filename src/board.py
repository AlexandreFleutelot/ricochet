import pygame
from constants import CELL_SIZE, WIDTH, HEIGHT, Color
from tiles import Empty, Wall, Robot, Target

class Board():
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[Empty() for y in range(n_cols)] for x in range(n_rows)]
        self.robots = {} # color -> (x, y)
        self.targets = {} # color -> (x, y)
        self.walls = set() # (x, y)
    
    def get_tile(self, x, y):
        return self.grid[x][y]
    
    def spawn_wall(self, x, y):
        self.walls.add((x, y))
        self.grid[x][y] = Wall()

    def spawn_robot(self, x, y, color=Color.RED, selected=False):
        self.robots[color] = (x, y)
        self.grid[x][y] = Robot(color, selected)
    
    def spawn_target(self, x, y, color=Color.RED):
        self.targets[color] = (x, y)
        self.grid[x][y] = Target(color)

    def despawn_target(self, x, y):
        del self.targets[self.grid[x][y].color]
        self.grid[x][y] = Empty()

    def move_robot(self, robot_color, direction):
        dx, dy = direction
        x, y = self.robots[robot_color]
        new_x,new_y = x,y

        while 0 <= new_x+dx < self.n_cols and 0 <= new_y+dy < self.n_rows:
            if (new_x+dx, new_y+dy) in self.walls:
                break
            if (new_x+dx, new_y+dy) in self.robots.values():
                break

            new_x, new_y = new_x + dx, new_y + dy            
            if robot_color in self.targets and (new_x, new_y) == self.targets[robot_color]:
                break
        
        if (x,y) != (new_x, new_y):
            self.grid[new_x][new_y] = self.grid[x][y]
            if (x,y) == self.targets[robot_color]:
                self.grid[x][y] = Target(robot_color)
            else:
                self.grid[x][y] = Empty()
            self.robots[robot_color] = (new_x, new_y)

    def draw_board(board, screen):
        screen.fill((255, 255, 255))

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y))

        for x,row in enumerate(board.grid):
            for y,tile in enumerate(row):
                tile.draw(screen, x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2)
