import pygame, sys, os, random , math 
from pygame.locals import *


# INIT GAME 

pygame.init()
fps = pygame.time.Clock()

# COLORS USING RGB VALUES 

WHITE = (255, 255, 255)
RED = (255, 0,0) 
GREEN = (0, 255, 0) 
BLACK = (0,0,0)



# GLOBAL VARIABLES THAT IM GONNA USE 

WIDTH = 800
HEIGHT = 600 
time = 0



# GAME WINDOW 

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('==👾Asteroids Game👾==')


# LOAD IMAGES FROM DIRECTORY 

bg = pygame.image.load(os.path.join('images', 'bg.jpg'))
debris = pygame.image.load(os.path.join('images','debris2_brown.png'))
ship = pygame.image.load(os.path.join('images','ship.png'))

# CREATING VALUES FOR COORDINATES IN CASE OF FUTURE CHANGES 

ship_x = WIDTH/2 - 50
ship_y = HEIGHT/2 - 50
ship_angle = 0

# FUNCTION FOR ROTATING IMAGE
 
def rot_center(image, angle):

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center 
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image



# FUNCTIONS TO DRAW GAME ELEMENTS 

def draw(canvas):
    global time
    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris,(time*.3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))
    time =time + 1
    canvas.blit(rot_center(ship,ship_angle), (ship_x, ship_y))

# FUNCTION TO HANDLE USER (MOUSE, KEYBOARD, ETC)
def handle_input():
    global ship_angle
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                ship_angle = ship_angle + 1 

# FUNCTION TO UPDATE THE SCREEN 

def update_screen():
    pygame.display.update()
    fps.tick(60) 
    

# ASTEROIDS GAME LOOP

while True: 
    draw(window)
    handle_input()
    # game_logic() 
    update_screen()