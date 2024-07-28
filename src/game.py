import pygame
import time
from board import Board
from solver import Solver
from constants import Color

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(n_rows=12, n_cols=12)
        self.setup_initial_board()
        self.robot_colors = list(self.board.robots.keys())
        self.selected_robot_color = self.robot_colors[0]

    def setup_initial_board(self):
        # Setup initial board state (robots, targets, walls)
        self.board.spawn_robot(3, 3, Color.RED, selected=True)
        self.board.spawn_robot(6, 8, Color.GREEN, selected=False)
        self.board.spawn_target(2, 8, Color.GREEN)
        self.board.spawn_target(8, 8, Color.RED)
        self.board.spawn_wall(5, 5)
        self.board.spawn_wall(4, 5)
        self.board.spawn_wall(3, 5)
        self.board.spawn_wall(8, 3)
        self.board.spawn_wall(8, 4)
        self.board.spawn_wall(7, 9)
        self.board.spawn_wall(8, 9)

    def _switch_selected_robot(self):
        current_index = self.robot_colors.index(self.selected_robot_color)
        next_index = (current_index + 1) % len(self.robot_colors)
        self.selected_robot_color = self.robot_colors[next_index]
        
        # Update the selected status of robots
        for color, (x, y) in self.board.robots.items():
            self.board.grid[x][y].selected = (color == self.selected_robot_color)

    def solve_puzzle(self):
        solver = Solver(self.board)
        solution = solver.solve()
        if solution:
            print("\nSolution found!")
            print("==============")
            for step, (robot_color, direction) in enumerate(solution, 1):
                dx, dy = direction
                if dx == -1:
                    direction_name = "LEFT"
                elif dx == 1:
                    direction_name = "RIGHT"
                elif dy == -1:
                    direction_name = "UP"
                elif dy == 1:
                    direction_name = "DOWN"
                else:
                    direction_name = "UNKNOWN"
                
                print(f"Step {step}: Move {robot_color.name} robot {direction_name}")
                
                self.board.move_robot(robot_color, direction)
                self.draw()
                time.sleep(0.5)
                pygame.event.pump()
            print(f"\nPuzzle solved in {len(solution)} moves!")
        else:
            print("\nNo solution found")
    

    def handle_key_press(self, key):
        match key:
            case pygame.K_SPACE:
                self._switch_selected_robot()
            case pygame.K_LEFT:
                self.board.move_robot(self.selected_robot_color, (-1, 0))
            case pygame.K_RIGHT:
                self.board.move_robot(self.selected_robot_color, (1, 0))
            case pygame.K_UP:
                self.board.move_robot(self.selected_robot_color, (0, -1))
            case pygame.K_DOWN:
                self.board.move_robot(self.selected_robot_color, (0, 1))  
            case pygame.K_r: #reset
                self.__init__(self.screen)
            case pygame.K_s: #solve the puzzle
                self.solve_puzzle()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.board.draw_board(self.screen)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)

            self.draw()

        pygame.quit()
