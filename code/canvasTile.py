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
        self.is_empty = False
    
    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case "terrain": self.has_terrain = True
            case "water": self.has_water = True
            case "enemy": self.enemy = tile_id
            case "coin": self.coin = tile_id
            
    def remove_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case "terrain": self.has_terrain = False
            case "water": self.has_water = False
            case "enemy": self.enemy = None
            case "coin": self.coin = None
        
        self.check_content()
        
    def check_content(self):
        if not self.has_terrain and not self.has_water and not self.coin and not self.enemy:
            self.is_empty = True 
        