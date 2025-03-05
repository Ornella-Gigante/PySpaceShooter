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
ship_thrusted = pygame.image.load(os.path.join('images','ship_thrusted.png'))
asteroid = pygame.image.load(os.path.join('images','asteroid.png'))
shot = pygame.image.load(os.path.join('images','shot2.png'))

# VARIABLES OF THE ASTEROID COORDINATES IN A LIST 

asteroid_x = [] #random.randint(0, WIDTH)
asteroid_y = [] #random.randint(0,HEIGHT)
no_asteroids =  5


# CREATING VALUES FOR COORDINATES IN CASE OF FUTURE CHANGES 

ship_x = WIDTH/2 - 50
ship_y = HEIGHT/2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False 
ship_direction = 0
ship_speed = 0
asteroid_angle = []
asteroid_speed = 2
game_over = False
bullet_x = 0 
bullet_y = 0 
bullet_angle = 0 
bullets = [] # List to store active bullets

for i in range(0,10):
    asteroid_x.append(random.randint(0,WIDTH))
    asteroid_y.append(random.randint(0, HEIGHT))
    asteroid_angle.append(random.randint(0,365))




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
    global time, ship_is_forward, game_over, shot, bullet_y, bullet_x, bullet_angle

    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris,(time*.3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))
    time =time + 1

    for i in range(0,no_asteroids):
        canvas.blit(rot_center(asteroid,time),(asteroid_x[i],asteroid_y[i]))

    if ship_is_forward:
        canvas.blit(rot_center(ship_thrusted,ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rot_center(ship,ship_angle), (ship_x, ship_y))

     # Draw bullets
    for bullet in bullets:
        canvas.blit(rot_center(shot, bullet["angle"]), (bullet["x"], bullet["y"]))

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        canvas.blit(text, text_rect)


# FUNCTION TO HANDLE USER (MOUSE, KEYBOARD, ETC)

def handle_input():
    global ship_is_rotating, ship_angle, ship_direction, ship_speed, ship_is_forward, ship_x, ship_y, bullet_y, bullet_x, bullet_angle
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_RIGHT:
                ship_is_rotating = True 
                ship_direction = 1
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 10

            elif event.key == K_SPACE:
                ship_center_x = ship_x + ship.get_width() / 2
                ship_center_y = ship_y + ship.get_height() / 2
                bullet_offset = 20  # Adjust this value to position the bullet in front of the ship
                bullets.append({
                    "x": ship_center_x + math.cos(math.radians(ship_angle)) * bullet_offset,
                    "y": ship_center_y - math.sin(math.radians(ship_angle)) * bullet_offset,
                    "angle": ship_angle,
                    "speed": 10
                })

    
            print(f" x {bullet_x} y {bullet_y} ")

        elif event.type== KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False 
            else: 
                ship_is_forward = False 
        
      
            

    if ship_is_rotating:
        if ship_direction == 0: 
            ship_angle = ship_angle - 10 
        else: 
            ship_angle = ship_angle + 10


    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle)) * ship_speed)
        ship_y = (ship_y + -math.sin(math.radians(ship_angle)) * ship_speed)
        if ship_is_forward == False: 
            ship_speed = ship_speed - 0.2

    
# FUNCTION TO UPDATE BULLETS POSITION

def update_bullets():
    global bullets
    for bullet in bullets[:]: # Iterate through a copy of the list to allow removal
        bullet["x"] += math.cos(math.radians(bullet["angle"])) * bullet["speed"]
        bullet["y"] += -math.sin(math.radians(bullet["angle"])) * bullet["speed"]

        # Remove bullets that go off-screen
        if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
            bullets.remove(bullet)


# FUNCTION TO UPDATE THE SCREEN 

def update_screen():
    pygame.display.update()
    fps.tick(60) 


# FUNCTION OF COLLISION 

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27: 
        return True 
    else:
        return False 


# FUNCTION FOR MOVING ASTEROIDS 

def game_logic():
    global game_over
    global bullet_y, bullet_x, bullet_angle
    for i in range(0,no_asteroids):
        asteroid_x[i] = (asteroid_x[i] + math.cos(math.radians(asteroid_angle[i])) * asteroid_speed)
        asteroid_y[i] = (asteroid_y[i] + -math.sin(math.radians(asteroid_angle[i])) * asteroid_speed)
        #bullet_x = (bullet_x + math.cos(math.radians(bullet_angle))* ship_speed)
        #bullet_y = (bullet_y + - math.sin(math.radians(bullet_angle))* ship_speed)
        

        # FUNCTION FOR ASTEROID BOUNDARIES ON SCREEN (y,x)

        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT

        if asteroid_y[i] > HEIGHT:
            asteroid_y[i] = 0

            
        if asteroid_x[i] < 0:
            asteroid_x[i] = WIDTH

        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0

        if isCollision(ship_x,ship_y, asteroid_x[i], asteroid_y[i]):
            game_over = True

# ASTEROIDS GAME LOOP

while True: 
    draw(window)
    if not game_over:
        handle_input()
        game_logic() 
        update_bullets()
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Reset the game
                    game_over = False
                    ship_x = WIDTH/2 - 50
                    ship_y = HEIGHT/2 - 50
                    ship_angle = 0
                    ship_speed = 0
                    for i in range(0, no_asteroids):
                        asteroid_x[i] = random.randint(0, WIDTH)
                        asteroid_y[i] = random.randint(0, HEIGHT)
                        asteroid_angle[i] = random.randint(0, 365)
    update_screen()
    