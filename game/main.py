# Pygame template - skeleton for a new pygame project
import pygame
import random
import os
import time

WIDTH = 900
HEIGHT = 1050
FPS = 30
DEFAULT_IMAGE_SIZE = (40, 40)
DEFAULT_BAT_SIZE = (100, 100)
DEFAULT_PITCH_SIZE = (800, 1000)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folders
# Windows : "C:\Users\"
# Mac: "/Users/"
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


class Bowler(pygame.sprite.Sprite):
    # sprite for the bowler
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bumrah1.png")).convert()
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 850
        self.speedx = 5

    def update(self):
        # get all the keys that were pressed
        keystate = pygame.key.get_pressed()
        # figure out which key was pressed
        # This actually moves the rectangle
        self.rect.x += self.speedx

        # Trying to ensure the player doesnt go beyond boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -5
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = 5

    def bowl(self):
        ball = Ball(self.rect.centerx, self.rect.bottom)
        all_sprites.add(ball)
        balls.add(ball)


class Bat(pygame.sprite.Sprite):
    # sprite for the bat
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(os.path.join(img_folder, "cricket-bat.png")).convert()
        self.image_orig = pygame.transform.scale(self.image_orig, DEFAULT_BAT_SIZE)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.rot = 0

    def update(self):
        self.speedx = 0
        # get all the keys that were pressed
        keystate = pygame.key.get_pressed()
        # figure out which key was pressed
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        # This actually moves the rectangle
        self.rect.x += self.speedx
        # Trying to ensure the player doesnt go beyond boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def hit(self):
        ball = Ball(self.rect.centerx, self.rect.top)
        all_sprites.add(ball)
        balls.add(ball)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "cricket-ball1.png")).convert()
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.bottom < 0:
            self.kill()

    def goup(self):
        self.speedy = -20


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mr. cricket balls")
clock = pygame.time.Clock()

# load the graphics for the game
background = pygame.image.load(os.path.join(img_folder, "grass1.png")).convert()
background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
bat = Bat()
bat_group = pygame.sprite.Group()
balls = pygame.sprite.Group()
badaboom_monkey = Bowler()
all_sprites.add(badaboom_monkey)
all_sprites.add(bat)
bat_group.add(bat)

score = 0

# Game loop
running = True

while running:
    # keep the loop running at the right speed
    clock.tick(FPS)
    # Randomly make the bowler ball
    random_number = random.randrange(30)
    if random_number == 1:
        badaboom_monkey.bowl()
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Do something with the bat
                print("TODO")

    # Update
    all_sprites.update()


    # check if a ball was hit by the bat
    hits = pygame.sprite.spritecollide(bat, balls, False)
    if hits:
    #running = False
        for ball in hits:
            ball.goup()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything flip the display
    pygame.display.flip()

pygame.quit()
