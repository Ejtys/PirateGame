import pygame


class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        
        self.image = pygame.Surface((100,200))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = pos)