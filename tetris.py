import random
from constHumano import FIELD_RES_HUMANO, WIN_RES_HUMAN
from constantes import *

#from constHumano import *

from agente import Agente, Text
import sys
import pathlib

from humano import Humano, TextHumano

class Juego:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
       
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        
        self.agente = Agente(self)
        self.text= Text(self)

        self.humano = Humano(self)
        self.textHumano= TextHumano(self)
    
    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_evet = pg.USEREVENT + 1
        self.fast_anim_trigger = False
        self.anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_evet, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.agente.update()
        self.humano.update()
        self.clock.tick(FPS)
    
    # def create_board(self):
    #     return [[0] * FIELD_W for _ in range(FIELD_H)]

    def draw(self):
        
        self.screen.fill(color=BG_COLOR, rect=(500,0,*FIELD_RES))
        self.screen.fill(color=FIELD_COLOR, rect=(0,0,*FIELD_RES))
        self.screen.fill(color=FIELD_COLOR, rect=(1000,0, *FIELD_RES_HUMANO))
        self.agente.draw()
        self.humano.draw()
        self.text.draw()
        self.textHumano.draw()
        pg.display.flip()
    
    def check_event(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.humano.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger= True
            elif event.type == self.fast_user_evet:
                self.fast_anim_trigger= True
    

    # def check_agente(self):
    #     self.anim_trigger = False
    #     self.fast_anim_trigger = False
    #     direcciones = random.choice(list(DIRECCIONES.keys()))
        
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
    #             pg.quit()
    #             sys.exit()
        
    #         # if self.should_activate_anim_trigger():
    #         #     self.anim_trigger = True
    #         # elif self.should_activate_fast_anim_trigger():
    #         #     self.fast_anim_trigger = True
    #         else:     
    #             self.agente.agente_control()
      
    def check_agente(self):
      
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # Obtener el mejor movimiento del agente
        # best_move = self.agente.tetramino.agente_control()
        # print(best_move)
        # if best_move is not None:
            
        #     if best_move[0] == 'left':
        #         self.agente.tetramino.move_left()
        #     elif best_move[0] == 'right':
        #         self.agente.tetramino.move_right()
        #     elif best_move[0] == 'rotate':
        #         self.agente.tetramino.rotate()
        #     elif best_move[0] == 'next_piece':
        #         self.agente.tetramino.move_down()

        
      #  self.agente.tetramino.move_down()

 

    def run(self):
        while True:
            self.check_event()
            self.check_agente()
            self.update()
            self.draw()
       
if __name__ == '__main__':
    app = Juego()
    app.run()
