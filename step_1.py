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


# DRAW GAME FUNCTION

def draw(canvas):
    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris(time*3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))

# HANDLE INPUT FUNCTION 

def handle_input():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def update_screen():
    pygame.display.update()
    fps.tick(60)
    
# ASTEROIDS GAME LOOP

while True: 
    draw(window)
    handle_input()
    # game_logic() 
    update_screen()