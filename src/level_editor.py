# level_editor.py

import pygame
from board import Board
from constants import CELL_SIZE, WIDTH, HEIGHT, Color, Type
from tiles import Wall, Robot, Target

class LevelEditor:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(n_rows=12, n_cols=12)
        self.current_tool = None
        self.tools = {
            'wall': Wall(),
            'robot_red': Robot(Color.RED),
            'robot_green': Robot(Color.GREEN),
            'robot_blue': Robot(Color.BLUE),
            'target_red': Target(Color.RED),
            'target_green': Target(Color.GREEN),
            'target_blue': Target(Color.BLUE),
            'eraser': None
        }
        self.toolbar_height = 50

    def handle_mouse_click(self, pos):
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        
        # Check if the click is within the board area
        if x < 0 or x >= self.board.n_cols or y < 0 or y >= self.board.n_rows:
            return

        if self.current_tool:
            if self.current_tool == 'eraser':
                self.board.grid[x][y] = self.tools['eraser']
                if (x, y) in self.board.walls:
                    self.board.walls.remove((x, y))
                for color in list(self.board.robots.keys()):
                    if self.board.robots[color] == (x, y):
                        del self.board.robots[color]
                        break
                for color in list(self.board.targets.keys()):
                    if self.board.targets[color] == (x, y):
                        del self.board.targets[color]
                        break
            elif isinstance(self.tools[self.current_tool], Wall):
                self.board.spawn_wall(x, y)
            elif isinstance(self.tools[self.current_tool], Robot):
                color = self.tools[self.current_tool].color
                self.board.spawn_robot(x, y, color)
            elif isinstance(self.tools[self.current_tool], Target):
                color = self.tools[self.current_tool].color
                self.board.spawn_target(x, y, color)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (0, HEIGHT, WIDTH, self.toolbar_height))
        
        tool_width = WIDTH // len(self.tools)
        for i, (tool_name, tool) in enumerate(self.tools.items()):
            tool_rect = pygame.Rect(i * tool_width, HEIGHT, tool_width, self.toolbar_height)
            pygame.draw.rect(self.screen, (150, 150, 150), tool_rect, 1)
            
            if tool_name == self.current_tool:
                pygame.draw.rect(self.screen, (100, 100, 100), tool_rect)
            
            if tool:
                tool.draw(self.screen, tool_rect.centerx, tool_rect.centery)
            else:  # Eraser
                pygame.draw.line(self.screen, (255, 0, 0), tool_rect.topleft, tool_rect.bottomright, 2)
                pygame.draw.line(self.screen, (255, 0, 0), tool_rect.bottomleft, tool_rect.topright, 2)

    def save_level(self):
        # Implement level saving logic here
        print("Level saved!")

    def load_level(self):
        # Implement level loading logic here
        print("Level loaded!")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < HEIGHT:
                        self.handle_mouse_click(event.pos)
                    else:
                        clicked_tool = event.pos[0] // (WIDTH // len(self.tools))
                        self.current_tool = list(self.tools.keys())[clicked_tool]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_level()
                    elif event.key == pygame.K_l:
                        self.load_level()

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.screen)
            self.draw_toolbar()
            pygame.display.flip()

        pygame.quit()