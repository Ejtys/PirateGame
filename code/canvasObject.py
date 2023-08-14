import pygame
from pygame.math import Vector2 as Vector
from settings import *


class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        
        #animation
        self.frames = frames
        self.frame_index = 0
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        #movement
        self.distance_to_origin = Vector(self.rect.topleft) - origin
        self.selected = False
        self.mouse_offset =  Vector()
        
    def start_drag(self):
        self.selected = True
        self.mouse_offset = Vector(pygame.mouse.get_pos()) - Vector(self.rect.topleft) 
    
    def drag(self):
        if self.selected:
            self.rect.topleft = Vector(pygame.mouse.get_pos()) - self.mouse_offset
    
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index >= len(self.frames):
            self.frame_index -= len(self.frames)
        
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin
        
    def update(self, dt):
        self.animate(dt)
        self.drag()
        
    
        