from constHumano import *
from tetraminoHumano import Block, Tetramino
import pygame.freetype as ft


class TextHumano:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)


    def draw(self):
     
        self.font.render_to(self.app.screen, (800, WIN_H * 0.8),
                            text=f'{self.app.humano.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)
        
        self.font.render_to(self.app.screen, (800, WIN_H * 0.3),
                            text='Humano', fgcolor='white',
                            size=TILE_SIZE * 0.64)
        
        self.font.render_to(self.app.screen, (800, WIN_H * 0.9),
                            text='Humano', fgcolor='white',
                            size=TILE_SIZE * 0.64)
                            
                            

class Humano:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        
        self.tetramino = Tetramino(self)
        self.next_tetromino = Tetramino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.huecos = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

      
        
    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0
    
    def check_lineas_completas(self):
        row = FIELD_H -1
        colum =FIELD_W -20
       
        #se intera el tablero de arriba a abajo, izquierda a derecha
        for y in range(FIELD_H - 1 ,-1,-1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
               
                if self.field_array[y][x]:                 
                    self.field_array[row][x].pos = vector(x, y)
            
            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
                        
            else:
                for x in range(FIELD_W):               
                    self.field_array[row][x].alive = False                                       
                    self.field_array[row][x] = 0             
                              
                self.full_lines += 1 
               
                
    def put_tetromino_in_array(self):
        for block in self.tetramino.blocks:
            x,y=int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

 
    def get_field_array(self):
        #para tener informacion sobre los tetrominos aterrizados 
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    def game_over(self):
        if self.tetramino.blocks[0].pos.y == INIT_POS_OFFESET[1]:
            pg.time.wait(300)
            return True    



        
    def control(self, pressed_key):
        #humano
        if pressed_key == pg.K_LEFT:
            self.tetramino.move(direccion='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetramino.move(direccion='right')
        elif pressed_key == pg.K_UP:
            self.tetramino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        
        
    def draw_tablero(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'YELLOW', 
                            ( x * TILE_SIZE, y * TILE_SIZE, 1050, 1050), 1 )
        
                
    def check_tetromino_landing(self):
        if self.tetramino.landing:
            if self.game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_in_array()
                self.next_tetromino.current = True
                self.tetramino = self.next_tetromino
                self.next_tetromino= Tetramino(self, current=False)

    def update(self):
       # trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        
        #if trigger:
            self.check_lineas_completas()  
            self.tetramino.update()
            self.check_tetromino_landing()
            self.get_score()
            self.sprite_group.update()


    def draw(self):
       self.draw_tablero()
       self.sprite_group.draw(self.app.screen)

