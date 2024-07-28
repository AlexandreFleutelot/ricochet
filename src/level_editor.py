# level_editor.py

import pygame
import json
import os

from board import Board
from constants import CELL_SIZE, WIDTH, HEIGHT, Color, Type
from tiles import Wall, Robot, Target, Empty

class LevelEditor:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(n_rows=12, n_cols=12)
        self.current_tool = None
        self.toolbar_height = 50
        self.button_width = WIDTH // 6
        self.dropup_open = None
        self.buttons = [
            {'name': 'Wall', 'tool': Wall()},
            {'name': 'Robot', 'tool': None, 'submenu': ['Red', 'Green', 'Blue']},
            {'name': 'Target', 'tool': None, 'submenu': ['Red', 'Green', 'Blue']},
            {'name': 'Eraser', 'tool': None},
            {'name': 'Save', 'tool': None},
            {'name': 'Load', 'tool': None},
        ]

    def handle_mouse_click(self, pos):
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        
        if x < 0 or x >= self.board.n_cols or y < 0 or y >= self.board.n_rows:
            return

        if self.current_tool:
            if isinstance(self.current_tool, str) and self.current_tool == 'Eraser':
                self.board.grid[x][y] = Empty()
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
            elif isinstance(self.current_tool, Wall):
                self.board.spawn_wall(x, y)
            elif isinstance(self.current_tool, Robot):
                color = self.current_tool.color
                if color in self.board.robots:
                    old_x, old_y = self.board.robots[color]
                    self.board.grid[old_x][old_y] = Empty()
                self.board.spawn_robot(x, y, color)
            elif isinstance(self.current_tool, Target):
                color = self.current_tool.color
                if color in self.board.targets:
                    old_x, old_y = self.board.targets[color]
                    self.board.grid[old_x][old_y] = Empty()
                self.board.spawn_target(x, y, color)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (0, HEIGHT, WIDTH, self.toolbar_height))
        
        for i, button in enumerate(self.buttons):
            button_rect = pygame.Rect(i * self.button_width, HEIGHT, self.button_width, self.toolbar_height)
            
            # Highlight the current tool
            if ((isinstance(self.current_tool, str) and button['name'] == self.current_tool) or
                (isinstance(self.current_tool, (Robot, Target)) and button['name'] == self.current_tool.__class__.__name__)):
                pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            else:
                pygame.draw.rect(self.screen, (150, 150, 150), button_rect, 1)
            
            font = pygame.font.Font(None, 24)
            text = font.render(button['name'], True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

            # If it's a Robot or Target button and it's the current tool, show the color
            if button['name'] in ['Robot', 'Target'] and isinstance(self.current_tool, (Robot, Target)) and button['name'] == self.current_tool.__class__.__name__:
                color_rect = pygame.Rect(button_rect.right - 20, button_rect.centery - 10, 20, 20)
                pygame.draw.rect(self.screen, self.current_tool.color.value, color_rect)

        if self.dropup_open:
            self.draw_dropup_menu()

    def draw_dropup_menu(self):
        button_index = next(i for i, b in enumerate(self.buttons) if b['name'] == self.dropup_open)
        submenu = self.buttons[button_index]['submenu']
        
        menu_height = len(submenu) * 30
        menu_rect = pygame.Rect(button_index * self.button_width, HEIGHT - menu_height, self.button_width, menu_height)
        pygame.draw.rect(self.screen, (220, 220, 220), menu_rect)

        for i, option in enumerate(submenu):
            option_rect = pygame.Rect(menu_rect.left, menu_rect.top + i * 30, self.button_width, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), option_rect, 1)
            
            font = pygame.font.Font(None, 24)
            text = font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=option_rect.center)
            self.screen.blit(text, text_rect)

            # Draw colored circle to represent the color option
            color = getattr(Color, option.upper()).value
            pygame.draw.circle(self.screen, color, (option_rect.left + 15, option_rect.centery), 10)

    def handle_toolbar_click(self, pos):
        clicked_index = pos[0] // self.button_width
        clicked_button = self.buttons[clicked_index]

        if 'submenu' in clicked_button:
            if self.dropup_open == clicked_button['name']:
                self.dropup_open = None
            else:
                self.dropup_open = clicked_button['name']
        else:
            self.dropup_open = None
            if clicked_button['name'] == 'Save':
                self.save_level()
            elif clicked_button['name'] == 'Load':
                self.load_level()
            else:
                self.current_tool = clicked_button['tool'] or clicked_button['name']

    def handle_dropup_click(self, pos):
        try:
            button_index = next(i for i, b in enumerate(self.buttons) if b['name'] == self.dropup_open)
            submenu = self.buttons[button_index]['submenu']
            menu_height = len(submenu) * 30
            clicked_index = len(submenu) - (HEIGHT - pos[1]) // 30 - 1
            
            if 0 <= clicked_index < len(submenu):
                color = submenu[clicked_index]
                
                if self.dropup_open == 'Robot':
                    self.current_tool = Robot(getattr(Color, color.upper()))
                elif self.dropup_open == 'Target':
                    self.current_tool = Target(getattr(Color, color.upper()))
                
                print(f"Selected tool: {self.current_tool}")  # Debug print
            else:
                print(f"Clicked outside submenu range. Clicked index: {clicked_index}")
            
            self.dropup_open = None
        except Exception as e:
            print(f"Error in handle_dropup_click: {e}")
            print(f"Dropup open: {self.dropup_open}")
            print(f"Click position: {pos}")
            self.dropup_open = None

    def save_level(self):
        level_data = {
            'walls': list(self.board.walls),
            'robots': {color.name: pos for color, pos in self.board.robots.items()},
            'targets': {color.name: pos for color, pos in self.board.targets.items()}
        }

        # Create a 'levels' directory if it doesn't exist
        if not os.path.exists('levels'):
            os.makedirs('levels')

        # Get user input for the filename
        filename = input("Enter a name for your level: ")
        filepath = os.path.join('levels', f"{filename}.json")

        # Save the level data to a JSON file
        with open(filepath, 'w') as f:
            json.dump(level_data, f, indent=2)

        print(f"Level saved as {filepath}")

    def load_level(self):
        # Create a 'levels' directory if it doesn't exist
        if not os.path.exists('levels'):
            os.makedirs('levels')

        # List all JSON files in the 'levels' directory
        level_files = [f for f in os.listdir('levels') if f.endswith('.json')]

        if not level_files:
            print("No saved levels found.")
            return

        # Print available levels
        print("Available levels:")
        for i, file in enumerate(level_files):
            print(f"{i + 1}. {file[:-5]}")  # Remove '.json' from the displayed name

        # Get user input for level selection
        while True:
            try:
                choice = int(input("Enter the number of the level you want to load: ")) - 1
                if 0 <= choice < len(level_files):
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

        # Load the selected level
        filepath = os.path.join('levels', level_files[choice])
        with open(filepath, 'r') as f:
            level_data = json.load(f)

        # Clear the current board
        self.board = Board(n_rows=12, n_cols=12)

        # Reconstruct the board state
        for wall in level_data['walls']:
            self.board.spawn_wall(*wall)

        for color_name, pos in level_data['robots'].items():
            color = getattr(Color, color_name)
            self.board.spawn_robot(*pos, color)

        for color_name, pos in level_data['targets'].items():
            color = getattr(Color, color_name)
            self.board.spawn_target(*pos, color)

        print(f"Level {level_files[choice][:-5]} loaded successfully.")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dropup_open:
                        self.handle_dropup_click(event.pos)
                    else:
                        if event.pos[1] < HEIGHT:
                            self.handle_mouse_click(event.pos)
                        else:
                            self.handle_toolbar_click(event.pos)
                        

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.screen)
            self.draw_toolbar()
            pygame.display.flip()

        pygame.quit()