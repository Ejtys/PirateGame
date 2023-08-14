import pygame, sys
from pygame.math import Vector2 as Vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

from settings import *
from support import *
from menu import Menu
from canvasTile import CanvasTile
from canvasObject import CanvasObject
from timer import Timer

class Editor:
    def __init__(self, land_tiles):
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}
        
        #imports
        self.land_tile = land_tiles
        self.imports()
        
        #navigation
        self.origin = Vector( )
        self.pan_active = False
        self.pan_offset = Vector()
        
        #support lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)
        
        #selection
        self.selection_index = 2
        self.last_selected_cell = None
        
        #menu
        self.menu = Menu()
        
        #objects
        self.canvas_objects = pygame.sprite.Group()
        self.object_drag_active = False
        self.object_timer = Timer(400)
        
        #player
        CanvasObject((200, WINDOW_HEIGHT/2), self.animations[0]["frames"], 0, self.origin, self.canvas_objects)
        
        self.sky_handle = CanvasObject(
            pos = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
            frames = [self.sky_handle_surface],
            tile_id = 1,
            origin = self.origin,
            group = self.canvas_objects
        )
  
    #support
    def get_current_cell(self):
        x = (Vector(mouse_pos()) - self.origin).x / TILE_SIZE
        y = (Vector(mouse_pos()) - self.origin).y / TILE_SIZE
        x = int(x) - 1 if x < 0 else int(x)
        y = int(y) - 1 if y < 0 else int(y)
        return x, y

    def check_neighbors(self, cell_pos):
        
        #local cluster
        cluster_size = 3
        local_cluster = [ 
                         (cell_pos[0] + col - int(cluster_size/2), cell_pos[1] + row - int(cluster_size/2))
                         for col in range(cluster_size)
                         for row in range(cluster_size)
                         ]
        
        for cell in local_cluster:
            if cell in self.canvas_data:
                self.canvas_data[cell].terrain_neighbors = []
                self.canvas_data[cell].water_on_top = False
                for name, side in NEIGHBOR_DIRECTIONS.items():
                    neighbor_cell = (cell[0] + side[0], cell[1] + side[1])
                    if neighbor_cell in self.canvas_data:
                        #terrain
                        if self.canvas_data[neighbor_cell].has_terrain:
                            self.canvas_data[cell].terrain_neighbors.append(name)
                        #water
                        if self.canvas_data[neighbor_cell].has_water and self.canvas_data[cell].has_water and name == "A":
                            self.canvas_data[cell].water_on_top = True
        
    def imports(self):
        self.water_bottom = pygame.image.load("../graphics/terrain/water/water_bottom.png").convert_alpha()
        self.sky_handle_surface = pygame.image.load("../graphics/cursors/handle.png").convert_alpha()
        
        #animation
        self.animations = {}
        for key, value in EDITOR_DATA.items():
            if value["graphics"]:
                graphics = import_folder(value["graphics"])
                self.animations[key] = {
                    "frame index": 0,
                    "frames": graphics,
                    "length": len(graphics)           
                }
    
    def animation_update(self, dt):
         for value in self.animations.values():
             value["frame index"] += ANIMATION_SPEED * dt
             if value["frame index"] >= value["length"]:
                 value["frame index"] -= value["length"]
    
    #input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            
            self.object_drag(event)
            
            self.canvas_add()
            self.canvas_remove()
            
    
    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = Vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False
            
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * TILE_SIZE
            else:
                self.origin.x -= event.y * TILE_SIZE
                
            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)
        
        if self.pan_active:
            self.origin = Vector(mouse_pos()) - self.pan_offset
            
            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index += 1
            if event.key == pygame.K_LEFT:
                self.selection_index -= 1
            if self.selection_index > 18:
                self.selection_index = 2
            elif self.selection_index < 2:
                self.selection_index = 18

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            index = self.menu.click(mouse_pos(), mouse_buttons())
            self.selection_index = index if index else self.selection_index

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()) and not self.object_drag_active:
            current_cell = self.get_current_cell()
            if EDITOR_DATA[self.selection_index]["type"] == "tile":
            
                if current_cell != self.last_selected_cell:
                    if current_cell in self.canvas_data:
                        self.canvas_data[current_cell].add_id(self.selection_index)
                    else:
                        self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                
                    self.check_neighbors(current_cell)
                    self.last_selected_cell = current_cell
            else:
                CanvasObject(
                    pos=mouse_pos(),
                    frames=self.animations[self.selection_index]["frames"],
                    tile_id=self.selection_index,
                    origin=self.origin,
                    group=self.canvas_objects
                )

    def canvas_remove(self):
        if mouse_buttons()[2] and not self.menu.rect.collidepoint(mouse_pos()):
            
            if self.canvas_data:
                current_cell = self.get_current_cell()
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].remove_id(self.selection_index)
                    if self.canvas_data[current_cell].is_empty:
                        del self.canvas_data[current_cell]
                
                self.check_neighbors(current_cell)

    def object_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            for sprite in self.canvas_objects:
                if sprite.rect.collidepoint(event.pos):
                    sprite.start_drag()
                    self.object_drag_active = True
        if event.type == pygame.MOUSEBUTTONUP and not mouse_buttons()[0] and self.object_drag_active:
            for sprite in self.canvas_objects:
                sprite.end_drag(self.origin)
                self.object_drag_active = False

    #draw
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE
        
        origin_offset = Vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE,
        )
        
        self.support_line_surf.fill("green")
        
        for col in range(cols + 1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))
        
        self.display_surface.blit(self.support_line_surf, (0,0))

    def draw_level(self):
        for cell_poss, tile in self.canvas_data.items():
            pos = self.origin + Vector(cell_poss) * TILE_SIZE
            
            if tile.has_water:
                if tile.water_on_top:
                    self.display_surface.blit(self.water_bottom, pos)
                else:
                    surface = self.animations[3]["frames"][int(self.animations[3]["frame index"])]
                    self.display_surface.blit(surface, pos)
            
            if tile.has_terrain:
                terrain_string = "".join(tile.terrain_neighbors)
                terrain_style = terrain_string if terrain_string in self.land_tile else "X"
                self.display_surface.blit(self.land_tile[terrain_style], pos)
                
            if tile.coin:
                surface = self.animations[tile.coin]["frames"][int(self.animations[tile.coin]["frame index"])]
                rect = surface.get_rect(center = (pos[0] + TILE_SIZE //2, pos[1] + TILE_SIZE // 2))
                self.display_surface.blit(surface, rect)
                
            if tile.enemy:
                surface = self.animations[tile.enemy]["frames"][int(self.animations[tile.enemy]["frame index"])]
                rect = surface.get_rect(midbottom = (pos[0] + TILE_SIZE //2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surface, rect)
        
        self.canvas_objects.draw(self.display_surface)
        
    def run(self, dt):
        self.event_loop()
        
        self.animation_update(dt)
        self.canvas_objects.update(dt)
        
        self.display_surface.fill("grey")
        self.draw_level()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10)
        
        self.draw_tile_lines()
        self.menu.display(dt, self.selection_index)
        

        