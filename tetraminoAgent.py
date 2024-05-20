
import copy
from constantes import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetramino, pos):
        self.tetramino = tetramino
        self.pos = vector(pos) + INIT_POS_OFFESET
        self.next_position = vector(pos) + NEXT_POS_OFFSET
        self.alive = True # para remover las lineas 
      
        super().__init__(tetramino.agente.sprite_group)
        self.image = tetramino.image
        
        self.rect = self.image.get_rect()
        
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    def sfx_end_time(self):
        if self.tetramino.agente.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True
            
    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:                
                self.kill()
                
    def rotate(self, pivot_pos):
        if not isinstance(pivot_pos, pg.math.Vector2):
            pivot_pos = pg.math.Vector2(pivot_pos)
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
    
    def set_rect_pos(self):
        pos = [self.next_position, self.pos][self.tetramino.current]
        self.rect.topleft = pos * TILE_SIZE
      

    def update(self):
        self.is_alive()
        self.set_rect_pos()  # Llamar a rect_pos dentro de update

    def coliciones(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetramino.agente.field_array[y][x]):
            return False
        return True
    
  
             

class Tetramino:
    def __init__(self, agente, current=True):
        self.agente = agente
        self.shape = random.choice(list(TETRAMINOS.keys()))
        self.image = random.choice(agente.app.images)
        self.blocks = [Block(self, pos) for pos in TETRAMINOS[self.shape]]
        self.current_piece = self.get_random_piece()
        
        self.last_move = None
        self.landing = False
        self.current = current

        self.grid = [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)]
        
        self.current_piece_x = FIELD_W // 2 - len(self.current_piece[0]) // 2
        self.current_piece_y = 0
        self.score = 0
        self.full_lines = 0
       

    def get_random_piece(self):
        return [block.pos for block in self.blocks]
    
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.coliciones(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
                
 
    
    def coliciones(self, block_pos):
        return any(map(Block.coliciones, self.blocks, block_pos))

    def move(self, direccion):
       
        direcciones = DIRECCIONES[direccion] 
        new_block_pos = [block.pos + direcciones for block in self.blocks]
        colisiones = self.coliciones(new_block_pos)
     
        if not colisiones:
            for block in self.blocks:
                block.pos += direcciones 
        elif direccion == 'down':
            self.landing = True
    
  

    def check_lineas_completas(self):
        row = FIELD_H -1
        
        #se intera el tablero de arriba a abajo, izquierda a derecha
        for y in range(FIELD_H - 1 ,-1,-1):
            for x in range(FIELD_W):
                self.agente.field_array[row][x] = self.agente.field_array[y][x]

                if self.agente.field_array[y][x]:
                    #self.self.agente.field_array[row][x].pos = vector(x, y)
                    self.agente.field_array[row][x] = vector(x, y)

            if sum(map(bool, self.agente.field_array[y])) < FIELD_W:
                row -= 1
                #self.huecos = self.count_huecos(row)
            else:
                for x in range(FIELD_W):
                    self.agente.field_array[row][x].alive = False
                    self.agente.field_array[row][x] = 0
                self.full_lines += 1 
               

    def evaluate_board(self):
        # Evaluar la altura máxima del tablero
        altura = max(self.grid[i][j] for j in range(FIELD_W) for i in range(FIELD_H - 1, -1, -1))

        # Evaluar la rugosidad de la superficie
        bloqueos = sum(abs(self.grid[i][j] - self.grid[i][j + 1]) for j in range(FIELD_W - 1) for i in range(FIELD_H - 1, -1, -1))

        # Evaluar la cantidad de huecos
        huecos = sum(1 for i in range(FIELD_H - 1, -1, -1) for j in range(FIELD_W) if self.grid[i][j] == 0 and any(self.grid[k][j] == 1 for k in range(i + 1, FIELD_H)))
        lienas_completas = self.full_lines
        
        score = -altura * -10 - bloqueos * 2 - huecos * 5 + lienas_completas * 1

        # w_altura = -0.5 
        # w_lineas = 1 
        # w_agujeros = -0.3 
        # w_baches = -0.2

        # score = (
        #     w_altura * altura +
        #     w_lineas * lienas_completas +
        #     w_agujeros * huecos +
        #     w_baches * bloqueos  
        # )

        return score
 
    def alpha_beta(self,field_array, alpha, beta, depth):
        if depth == 0:
            return self.evaluate_board()


        best_score = float('-inf')
        best_move = None
        for _ in range(4):
            grid_copy = copy.deepcopy(self.grid)
            score = -self.alpha_beta(grid_copy, -beta, -alpha, depth - 1)  # Negar el resultado de la llamada recursiva
            
            if score > best_score:
                best_score = score
                
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score  
    
    def agente_control(self):
        best_score = float('-inf')
        #beta = float('inf')
        best_move = None
        #alpha = self.alpha_beta(self.current_piece, beta, best_score, 3)
        
        # Probar todas las rotaciones posibles
        for _ in range(4):
            # Probar mover a la izquierda
            
            for i in range(self.current_piece_x, -1, -1):
                if self.can_move_piece(self.current_piece, i, self.current_piece_y):
                    
                    grid_copy = copy.deepcopy(self.grid)
                    self.place_piece(self.current_piece, i, self.current_piece_y, grid_copy)
                    score = self.evaluate_board_copy(grid_copy)
                    if score > best_score:
                        best_score = score
                        best_move = ('left', i)
                    break
        
            # Probar mover a la derecha
            for i in range(self.current_piece_x, FIELD_W - len(self.current_piece[0]) + 1):
                if self.can_move_piece(self.current_piece, i, self.current_piece_y):
                
                    grid_copy = copy.deepcopy(self.grid)
                    self.place_piece(self.current_piece, i, self.current_piece_y, grid_copy)
                    score = self.evaluate_board_copy(grid_copy)
                    if score > best_score:
                        best_score = score
                        best_move = ('right', i)
                    break

            # Rotar la pieza
            rotated_piece = list(map(list, zip(*self.current_piece[::-1])))
            if self.can_move_piece(rotated_piece, self.current_piece_x, self.current_piece_y):
                
                grid_copy = copy.deepcopy(self.grid)
                self.place_piece(rotated_piece, self.current_piece_x, self.current_piece_y, grid_copy)
                score = self.evaluate_board_copy(grid_copy)
                if score > best_score:
                    best_score = score
                    best_move = ('rotate', None)
                self.current_piece = rotated_piece

            # Rotar la siguiente pieza
            next_piece = self.get_random_piece()
          
            for _ in range(4):
                if self.can_move_piece(next_piece, FIELD_W // 2 - len(next_piece[0]) // 2, 0):
                    
                    grid_copy = copy.deepcopy(self.grid)
                    self.place_piece(next_piece, FIELD_W // 2 - len(next_piece[0]) // 2, 0, grid_copy)
                    score = self.evaluate_board_copy(grid_copy)
                    if score > best_score:
                        best_score = score
                        best_move = ('next_piece', None)
                    next_piece = list(map(list, zip(*next_piece[::-1])))

        return best_move
    
    def can_move_piece(self, piece, x, y):
        for py in range(len(piece)):
            for px in range(len(piece[py])):
                if piece[py][px] == 1:
                    if y + py >= FIELD_H or x + px < 0 or x + px >= FIELD_W or self.grid[y + py][x + px] == 1:
                        return False
        return True


    def place_piece(self, piece, x, y, grid):
        for py in range(len(piece)):
            for px in range(len(piece[py])):
                if piece[py][px] == 1:
                    grid[y + py][x + px] = 1
    
    def evaluate_board_copy(self, grid):
        # Evaluar la altura máxima del tablero
        altura = max(grid[i][j] for j in range(FIELD_W) for i in range(FIELD_H - 1, -1, -1))

        # Evaluar la rugosidad de la superficie
        bloqueos = sum(abs(grid[i][j] - grid[i][j + 1]) for j in range(FIELD_W - 1) for i in range(FIELD_H - 1, -1, -1))

        # Evaluar la cantidad de huecos
        huecos = sum(1 for i in range(FIELD_H - 1, -1, -1) for j in range(FIELD_W) if grid[i][j] == 0 and any(grid[k][j] == 1 for k in range(i + 1, FIELD_H)))
        lienas_completas = self.full_lines
       
        score = -altura * -10 - bloqueos * 2 - huecos * 5 + lienas_completas * 1

        # w_altura = -10 
        # w_lineas = 30 
        # w_agujeros = -2
        # w_baches = -5

        # score = (
        #     w_altura * altura +
        #     w_lineas * lienas_completas +
        #     w_agujeros * huecos +
        #     w_baches * bloqueos  
        # )

        return score

    def update(self):
        #self.move(direccion='down')
        best_move = self.agente_control()
        if best_move is not None:
            
            if best_move[0] == 'left':
                self.move(direccion='left')
            elif best_move[0] == 'right':
                self.move(direccion='right')
            elif best_move[0] == 'rotate':
                self.rotate()
            elif best_move[0] == 'next_piece':
                self.move(direccion='down')
        self.move(direccion='down')
        #self.move_down()
        
        for block in self.blocks:
            block.update()
        pg.time.wait(200)
           
    


        