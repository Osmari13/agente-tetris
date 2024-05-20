import copy
import pprint
from constantes import *
import math
from tetraminoAgent import Tetramino
import random
import pygame.freetype as ft


objeto_x = 1
objeto_y = 1
FIELD_W = 17
class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)
    
    def draw(self):
        self.font.render_to(self.app.screen, ( 600,  0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (600, WIN_H * 0.22),
                            text='next', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (600, WIN_H * 0.67),
                            text='score', fgcolor='orange',
                            size=TILE_SIZE * 1.4, bgcolor='black')
        self.font.render_to(self.app.screen, (600, WIN_H * 0.8),
                            text=f'{self.app.agente.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)
        
        self.font.render_to(self.app.screen, (600, WIN_H * 0.3),
                            text='Agente', fgcolor='white',
                            size=TILE_SIZE * 0.64)
        
        self.font.render_to(self.app.screen, (600, WIN_H * 0.9),
                            text='Agente', fgcolor='white',
                            size=TILE_SIZE * 0.64)

class Agente:
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

        # self.grid = [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)]
        # self.current_piece = self.tetramino.copia_bloks
        
        # self.current_piece_x = FIELD_W // 2 - len(self.current_piece[0]) // 2
        # self.current_piece_y = 0
        

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0
    
    def check_lineas_completas(self):
        row = FIELD_H -1
        #se intera el tablero de arriba a abajo, izquierda a derecha
        for y in range(FIELD_H - 1 ,-1,-1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    #self.field_array[row][x].pos = vector(x, y)
                    self.field_array[row][x] = vector(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
                #self.huecos = self.count_huecos(row)
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



    # def alpha_beta(self,field_array, alpha, beta, depth):
    #     if depth == 0 or self.is_terminal(field_array):
    #         return self.evaluacion(field_array)

    #     moves = self.generate_moves()
    #     best_score = float('-inf')
    #     best_move = None
    #     for move in moves:
    #         new_field_array = self.tetramino.apply_move(field_array, move)
    #         score = -self.alpha_beta(new_field_array, -beta, -alpha, depth - 1)  # Negar el resultado de la llamada recursiva
            
    #         self.undo_move()
    #         if score > best_score:
    #             best_score = score
    #             best_move = move
    #         alpha = max(alpha, best_score)
    #         if alpha >= beta:
    #             break
    #     return best_score  

  

    def draw_tablero(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black', 
                            ( x * TILE_SIZE, y * TILE_SIZE, 1050, 1050), 2 )


                
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
       
        self.check_lineas_completas()  
        self.tetramino.update()
        self.check_tetromino_landing()
        self.get_score()
        self.sprite_group.update()

    def draw(self):
       self.draw_tablero()
       self.sprite_group.draw(self.app.screen)

