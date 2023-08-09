import pygame, sys
from settings import *

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
    def event_loop(self):
        for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
    def run(self, dt):
        self.event_loop( )