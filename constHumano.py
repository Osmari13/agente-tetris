import pygame as pg

vector = pg.math.Vector2


TETRAMINOS = {
    'T': [(0,0),(-1,0),(1,0),(0,-1)],
    'O': [(0,0),(0,-1),(1,0),(1,-1)],
    'J': [(0,0),(-1,0),(0,-1),(0,-2)],
    'L': [(0,0),(1,0),(0,-1),(0,-2)],
    'I': [(0,0),(0,1),(0,-1),(0,-2)],
    'S': [(0,0),(-1,0),(0,-1),(1,-1)],
    'Z': [(0,0),(1,0),(0,-1),(-1,-1)]
}


DIRECCIONES = {'left': vector(-1, 0), 'right': vector(1, 0), 'down': vector(0, 1)}

FPS = 60
FIELD_COLOR = (48,39,32)

SPRITE_DIR_PATH = 'assets/sprites'
FONT_PATH = 'assets/font/FREAKSOFNATUREMASSIVE.ttf'

ANIM_TIME_INTERVAL = 400 #MILISEGUNDOS 150
FAST_ANIM_TIME_INTERVAL = 15

TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 30 ,20
FIELD_RES_HUMANO = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

# Tamaño de cada celda

start_x = FIELD_W // 2
#INIT_POS_OFFESET = vector(FIELD_W // 2 - 1, 0) 
INIT_POS_OFFESET = vector(FIELD_W // 1.2 , 0) 
NEXT_POS_OFFSET = vector(FIELD_W * 0.6, FIELD_H * 0.45)



# para las puntuaciones 
FILED_SCALE_W, FIELD_SCALE_H =1.7, 1.0 
#amplia la resolucion de la ventana
WIN_RES_HUMAN = WIN_W, WIN_H = FIELD_RES_HUMANO[0] * FILED_SCALE_W , FIELD_RES_HUMANO[1] * FIELD_SCALE_H 
BG_COLOR = (24,89,117)