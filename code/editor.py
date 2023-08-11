import pygame, sys
from pygame.math import Vector2 as Vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

from settings import *
from menu import Menu
from canvasTile import CanvasTile

class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}
        
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
  
    #support
    def get_current_cell(self):
        x = (Vector(mouse_pos()) - self.origin).x / TILE_SIZE
        y = (Vector(mouse_pos()) - self.origin).y / TILE_SIZE
        x = int(x) - 1 if x < 0 else int(x)
        y = int(y) - 1 if y < 0 else int(y)
        return x, y
    
    #input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.canvas_add()
    
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
        
        if self.pan_active:
            self.origin = Vector(mouse_pos()) - self.pan_offset

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
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()):
            current_cell = self.get_current_cell()
            
            if current_cell != self.last_selected_cell:
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index)
                else:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                self.last_selected_cell = current_cell

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
            
            if tile.has_terrain:
                test_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surface.fill("brown")
                self.display_surface.blit(test_surface, pos)
        
  
    def run(self, dt):
        self.event_loop( )
        
        self.display_surface.fill("grey")
        self.draw_level()
        pygame.draw.circle(self.display_surface, "red", self.origin, 10)
        
        self.draw_tile_lines()
        self.menu.display(dt, self.selection_index)
        

        