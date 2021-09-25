import pygame
import random
import math
from pygame import mixer

pygame.init()

# Screensize
screensizeX = 800
screensizeY = 600

# Create Game Screen in (x, y) format with (0, 0) at top left corner
screen = pygame.display.set_mode((screensizeX, screensizeY))

# Title, Icon & Background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images\spaceship1.png")
# background = pygame.image.load("images\Background1_resize.png")
background = pygame.image.load("images\Background4.png")
collision_img = pygame.image.load("images\explosion.png")
pygame.display.set_icon(icon)

# Background Music
mixer.music.load("sound\Background.wav")
mixer.music.play(-1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def show_Score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Player
playerImg = pygame.image.load("images\player1.png")
playerX = 400
playerY = 500
playerX_Change = 0
playerY_Change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = pygame.image.load("images\enemy1.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(0, 250)
def spawnEnemy():
    global enemyX
    global enemyY
    enemyX = random.randint(0, 736)
    enemyY = random.randint(0, 250)
enemyX_Change = 3
enemyY_Change = 20

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Bullet
bulletImg = pygame.image.load("images\Bullet.png")
bulletX = playerX
bulletY = playerY
bulletX_Change = 3
bulletY_Change = 10
bullet_State = "ready" # Bullet is ready to fire, can't see the Bullet on screen

def fire_Bullet(x, y):
    global bullet_State
    bullet_State = "fired" # Bullet fired by clicking on Spacebar, can see Bullet on screen
    screen.blit(bulletImg, (x + 16, y + 10))

# Determining distance between Bullet & Enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    diffX = enemyX - bulletX
    diffY = enemyY - bulletY
    sqX = math.pow(diffX, 2)
    sqY = math.pow(diffY, 2)
    distance = math.sqrt(sqX + sqY)
    if distance < 27:
        return True
    else:
        return False

# Game
running = True
while running:

    # BG color in (R, G, B) format
    screen.fill((16,16,16))
    
    # Adding Background Image
    screen.blit(background, (0, 0))

    '''Player moves
    playerX += 0.1
    playerY -= 0.1'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Checking Keys pressed, then assigning change values
        if event.type == pygame.KEYDOWN:
            # print("Key has been pressed")
            if event.key == pygame.K_LEFT:
                # print("Left Key has been pressed")
                playerX_Change = -4
            if event.key == pygame.K_RIGHT:
                # print("Right Key has been pressed.")
                playerX_Change = 4
            if event.key == pygame.K_UP:
                # print("Up Key has been pressed.")
                playerY_Change = -4
            if event.key == pygame.K_DOWN:
                # print("Down Key has been pressed.")
                playerY_Change = 4
            if event.key == pygame.K_SPACE:
                if bullet_State == "ready":
                    bullet_Sound = mixer.Sound("sound\laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX # Bullet has initial x-coordinate of the player
                    fire_Bullet(bulletX, bulletY)
        
        # Checking Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # print("Key has been released")
                playerX_Change = 0
                playerY_Change = 0

    # Moving player
    playerX += playerX_Change
    playerY += playerY_Change

    # Checking for X boundary for player
    if playerX < 0:
        playerX = 0
    elif playerX > screensizeX - 64:
        playerX = screensizeX - 64

    # Checking for Y boundary for player
    if playerY < 400:
        playerY = 400
    elif playerY > screensizeY - 64:
        playerY = screensizeY - 64

    # Moving enemy
    enemyX += enemyX_Change

    # Checking for X boundary for enemy
    if enemyX < 0:
        enemyX_Change = 3
        enemyY += enemyY_Change
    elif enemyX > screensizeX - 64:
        enemyX_Change = -3
        enemyY += enemyY_Change

    '''Checking for Y boundary for enemy
    if enemyY < 300:
        enemyY_Change = 0.2
    elif enemyY > screensizeY - 64:
        enemyY_Change = 0.2'''

    # Bullet Movement
    if bulletY < 0:
        bulletY = playerY
        bullet_State = "ready"
    if bullet_State == "fired":
        fire_Bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        explosion_Sound = mixer.Sound("sound\explosion.wav")
        explosion_Sound.play()
        score_value += 1
        bullet_State = "ready"
        bulletY = playerY
        screen.blit(collision_img, (enemyX, enemyY))
        spawnEnemy()
        # print(score_value)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_Score(scoreX, scoreY)
    pygame.display.update()