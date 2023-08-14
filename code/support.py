import pygame
from os import walk

def import_folder(path):
    surface_list = []
    
    for folder_name, sub_folder, image_files in walk(path):
        for image_name in image_files:
            fullpath = path + "/" +  image_name
            image_surface = pygame.image.load(fullpath).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list

def import_folder_dict(path):
    surface_dict = {}
    
    for folder_name, sub_folder, image_files in walk(path):
        for image_name in image_files:
            fullpath = path + "/" +  image_name
            image_surface = pygame.image.load(fullpath).convert_alpha()
            surface_dict[image_name.split(".")[0]] = image_surface

    return surface_dict