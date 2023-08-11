import pygame
from settings import *

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_buttons()
        
    def create_buttons(self):
        #menu area
        size = 180
        margin = 6
        topleft = (WINDOW_WIDTH - size - margin, WINDOW_HEIGHT - size - margin)
        self.rect = pygame.Rect(topleft, (size, size))
        
        #buttons areas
        generic_rect = pygame.Rect(topleft, (self.rect.width /2, self.rect.height / 2))
        button_margin = 7 
        self.tile_button_rect = generic_rect.copy().inflate(-button_margin, -button_margin)
        self.coin_button_rect = generic_rect.move(self.rect.width/2, 0).inflate(-button_margin, -button_margin)
        self.enemy_button_rect = generic_rect.move(self.rect.width/2, self.rect.height/2).inflate(-button_margin, -button_margin)
        self.palm_button_rect = generic_rect.move(0, self.rect.height/2).inflate(-button_margin, -button_margin)
    
    def display(self):
        pygame.draw.rect(self.display_surface, "black", self.tile_button_rect)
        pygame.draw.rect(self.display_surface, "yellow", self.coin_button_rect) 
        pygame.draw.rect(self.display_surface, "red", self.enemy_button_rect) 
        pygame.draw.rect(self.display_surface, "green", self.palm_button_rect)  