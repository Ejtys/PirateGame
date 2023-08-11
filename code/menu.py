from typing import Any
import pygame
from settings import *

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_data()
        self.create_buttons()
       
    def create_data(self):
        self.menu_surfaces = {}
        for key, value in EDITOR_DATA.items():
            if value["menu"]:
                if not value["menu"] in self.menu_surfaces:
                    self.menu_surfaces[value["menu"]] = [(key, pygame.image.load(value["menu_surf"]))]
                else:
                    self.menu_surfaces[value["menu"]].append((key, pygame.image.load(value["menu_surf"])))
        
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
        
        #create buttons
        self.buttons = pygame.sprite.Group()
        Button(self.tile_button_rect, self.buttons, self.menu_surfaces["terrain"])
        Button(self.coin_button_rect, self.buttons, self.menu_surfaces["coin"])
        Button(self.enemy_button_rect, self.buttons, self.menu_surfaces["enemy"])
        Button(self.palm_button_rect, self.buttons, self.menu_surfaces["palm fg"], self.menu_surfaces["palm bg"])
    
    def click(self, mouse_pos, mouse_button):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                if mouse_button[1]: #middle button
                    sprite.main_active = not sprite.main_active if sprite.items['alt'] else True
                if mouse_button[2]: #right button
                    sprite.switch()
                return sprite.get_id()
    
    def display(self,dt):
        self.buttons.update(dt)
        self.buttons.draw(self.display_surface)
    
class Button(pygame.sprite.Sprite):
    def __init__(self, rect, group, items, items_alt = None):
        super().__init__(group)
        self.image = pygame.Surface(rect.size)
        self.rect = rect
        
        #items
        self.items = {"main":items, "alt":items_alt}
        self.index = 0
        self.main_active = True 
        
    def get_id(self):
        return self.items["main" if self.main_active else "alt"][self.index][0]
        
    def switch(self):
        self.index += 1
        self.index = 0 if self.index >= len(self.items["main" if self.main_active else "alt"]) else self.index
        
    def update(self, dt):
        self.image.fill(BUTTON_BG_COLOR)
        surface = self.items["main" if self.main_active else "alt"][self.index][1]
        rect = surface.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
        self.image.blit(surface, rect)