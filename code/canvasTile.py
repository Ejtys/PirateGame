import pygame
from settings import *


class CanvasTile:
    def __init__(self, tile_id):
        
        #terrain
        self.has_terrain = False
        self.terrain_neighbors = []
        
        #water
        self.has_water = False
        self.water_on_top = False
        
        #coin
        self.coin = None
        
        #enemy
        self.enemy = None
        
        #objects
        self.objects = []
        
        self.add_id(tile_id)
    
    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        print(options)
        