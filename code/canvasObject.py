import pygame
from pygame.math import Vector2 as Vector


class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        
        self.image = pygame.Surface((100,200))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = pos)
        
        #movement
        self.distance_to_origin = Vector(self.rect.topleft) - origin
        
    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin