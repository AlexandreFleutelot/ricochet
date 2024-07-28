# main.py

import pygame
from game import Game
from level_editor import LevelEditor
from constants import WIDTH, HEIGHT

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Ricochet Robot")

def main_menu():

    menu = True
    while menu:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        
        play_text = font.render("1. Play Game", True, (0, 0, 0))
        editor_text = font.render("2. Level Editor", True, (0, 0, 0))
        quit_text = font.render("3. Quit", True, (0, 0, 0))
        
        screen.blit(play_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(editor_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "editor"
                elif event.key == pygame.K_3:
                    return "quit"

if __name__ == "__main__":
    choice = main_menu()
    
    if choice == "play":
        game = Game(screen)
        game.run()
    elif choice == "editor":
        editor = LevelEditor(screen)
        editor.run()
    elif choice == "quit":
        pygame.quit()