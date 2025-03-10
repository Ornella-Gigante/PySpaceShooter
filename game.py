import pygame, sys, os, random, math 
from pygame.locals import *

# INIT GAME 
pygame.mixer.pre_init()
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
explosion = pygame.image.load(os.path.join('images', 'explosion_blue.png'))

# VARIABLES OF THE ASTEROID COORDINATES IN A LIST 
asteroid_x = []
asteroid_y = []
no_asteroids = 5

# LOAD SOUNDS
missile_sound = pygame.mixer.Sound(os.path.join('sounds', 'missile.ogg'))
missile_sound.set_volume(1)
thruster_sound = pygame.mixer.Sound(os.path.join('sounds', 'thrust.ogg'))
thruster_sound.set_volume(1)
explosion_sound = pygame.mixer.Sound(os.path.join('sounds', 'explosion.ogg'))
explosion_sound.set_volume(1)
pygame.mixer.music.load(os.path.join('sounds', 'game.ogg'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

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
bullets = []
score = 0 
victory = False 
ship_width = ship.get_width()
ship_height = ship.get_height()

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
    global time, ship_is_forward, game_over, shot, bullet_y, bullet_x, bullet_angle, score, victory

    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris,(time*.3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))
    time = time + 1

    if not game_over and not victory:
        for bullet in bullets:
            canvas.blit(shot, (bullet['x'], bullet['y']))

        for i in range(0,no_asteroids):
            canvas.blit(rot_center(asteroid,time),(asteroid_x[i],asteroid_y[i]))

        if ship_is_forward:
            canvas.blit(rot_center(ship_thrusted,ship_angle), (ship_x, ship_y))
        else:
            canvas.blit(rot_center(ship,ship_angle), (ship_x, ship_y))

    for bullet in bullets:
        canvas.blit(rot_center(shot, bullet["angle"]), (bullet["x"], bullet["y"]))

    font = pygame.font.SysFont("Comic Sans MS", 40)
    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    canvas.blit(score_text, (50, 20))

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        canvas.blit(text, text_rect)

        font_small = pygame.font.SysFont("Comic Sans MS", 30)
        restart_text = font_small.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 80))
        canvas.blit(restart_text, restart_rect)
        
    if victory:
        font = pygame.font.SysFont("Comic Sans MS", 74)
        text = font.render("YOU WIN!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        canvas.blit(text, text_rect)
        
        font_small = pygame.font.SysFont("Comic Sans MS", 30)
        restart_text = font_small.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 80))
        canvas.blit(restart_text, restart_rect)

# FUNCTION TO HANDLE USER (MOUSE, KEYBOARD, ETC)
def handle_input():
    global ship_is_rotating, ship_angle, ship_direction, ship_speed, ship_is_forward, ship_x, ship_y, bullet_y, bullet_x, bullet_angle, ship_width, ship_height
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
                bullet_offset = 20
                bullets.append({
                    "x": ship_center_x + math.cos(math.radians(ship_angle)) * bullet_offset,
                    "y": ship_center_y - math.sin(math.radians(ship_angle)) * bullet_offset,
                    "angle": ship_angle,
                    "speed": 10
                })
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False 
            elif event.key == K_UP:
                ship_is_forward = False

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle -= 10
        else:
            ship_angle += 10

    if ship_is_forward or ship_speed > 0:
        new_x = ship_x + math.cos(math.radians(ship_angle)) * ship_speed
        new_y = ship_y - math.sin(math.radians(ship_angle)) * ship_speed
        
        ship_width = ship.get_width()
        ship_height = ship.get_height()
        
        if 0 <= new_x <= WIDTH - ship_width:
            ship_x = new_x
        if 0 <= new_y <= HEIGHT - ship_height:
            ship_y = new_y
        
        if not ship_is_forward:
            ship_speed = max(0, ship_speed - 0.2)

    ship_x = max(0, min(ship_x, WIDTH - ship_width))
    ship_y = max(0, min(ship_y, HEIGHT - ship_height))

# FUNCTION TO UPDATE BULLETS POSITION
def update_bullets():
    for bullet in bullets[:]:
        bullet['x'] += math.cos(math.radians(bullet['angle'])) * 10
        bullet['y'] -= math.sin(math.radians(bullet['angle'])) * 10
        if bullet['x'] < 0 or bullet['x'] > WIDTH or bullet['y'] < 0 or bullet['y'] > HEIGHT:
            bullets.remove(bullet)

# FUNCTION OF COLLISION 
def isCollision(x1, y1, x2, y2, distance):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < distance

# FUNCTION TO UPDATE THE SCREEN 
def update_screen():
    pygame.display.update()
    fps.tick(60) 

# FUNCTION FOR MOVING ASTEROIDS 
def game_logic():
    global game_over, bullet_y, bullet_x, bullet_angle, score, victory

    if score >= 10:
        victory = True
        return

    for i in range(0,no_asteroids):
        asteroid_x[i] += math.cos(math.radians(asteroid_angle[i])) * asteroid_speed
        asteroid_y[i] -= math.sin(math.radians(asteroid_angle[i])) * asteroid_speed

        asteroid_x[i] %= WIDTH
        asteroid_y[i] %= HEIGHT

        if isCollision(ship_x + 25, ship_y + 25, asteroid_x[i] + 25, asteroid_y[i] + 25, 50):
            game_over = True

    for bullet in bullets[:]:
        for i in range(no_asteroids):
            if isCollision(bullet['x'], bullet['y'], asteroid_x[i] + 25, asteroid_y[i] + 25, 25):
                asteroid_x[i] = random.randint(0, WIDTH)
                asteroid_y[i] = random.randint(0, HEIGHT)
                asteroid_angle[i] = random.randint(0, 365)
                bullets.remove(bullet)
                explosion_sound.play()
                score += 1
                break

# ASTEROIDS GAME LOOP
while True: 
    draw(window)
    if not game_over and not victory:
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
                    game_over = False
                    victory = False
                    ship_x = WIDTH/2 - 50
                    ship_y = HEIGHT/2 - 50
                    ship_angle = 0
                    ship_speed = 0
                    bullets.clear()
                    score = 0 
                    for i in range(0, no_asteroids):
                        asteroid_x[i] = random.randint(0, WIDTH)
                        asteroid_y[i] = random.randint(0, HEIGHT)
                        asteroid_angle[i] = random.randint(0, 365)
    update_screen()
