
import copy
from constHumano import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetramino, pos):
        self.tetramino = tetramino
        self.pos =  vector(pos) + INIT_POS_OFFESET
        self.next_position = vector(pos) + NEXT_POS_OFFSET
        self.alive = True # para remover las lineas 
       
        super().__init__(tetramino.humano.sprite_group)
        self.image = tetramino.image
        
        self.rect = self.image.get_rect()
        

    def is_alive(self):
        if not self.alive:               
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
        if 20 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetramino.humano.field_array[y][x]):
            return False
        return True
    
  
             

class Tetramino:
    def __init__(self, humano, current=True):
        self.humano = humano
        
        self.shape = random.choice(list(TETRAMINOS.keys()))
        self.image = random.choice(humano.app.images)
        self.blocks = [Block(self, pos) for pos in TETRAMINOS[self.shape]]
       
        self.last_move = None
        self.landing = False
        self.current = current
    
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

    def update(self):
       
        self.move(direccion='down')
    
        for block in self.blocks:
            block.update()
        pg.time.wait(200)
           
    

