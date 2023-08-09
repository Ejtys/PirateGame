import pygame
from settings import *
from editor import Editor

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.editor = Editor()
        
        #cursor
        surf = pygame.image.load("../graphics/cursors/mouse.png").convert_alpha()
        cursor = pygame.cursors.Cursor((0,0 ), surf)
        pygame.mouse.set_cursor(cursor)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.editor.run(dt)
            pygame.display.update()
            
if __name__ == "__main__":
    Main().run()