import pygame, sys, os, random , math 
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# COLORS

WHITE = (255, 255, 255)
RED = (255, 0,0) 
GREEN = (0, 255, 0) 
BLACK = (0,0,0)



# GLOBALS

WIDTH = 800
HEIGHT = 600 
time = 0



# CANVAS DECLARATION

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Asteroids')


# LOAD IMAGES 

bg = pygame.image.load(os.path.join('images', 'bg.jpg'))
debris = pygame.image.load(os.path.join('images','debris2_brown.png'))

# ASTEROIDS GAME LOOP

while True: 
    draw(window)
    handle_input()
    # game_logic() 
    update_screen()