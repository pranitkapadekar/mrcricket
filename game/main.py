# Pygame template - skeleton for a new pygame project
import pygame
import random
import os
import time

WIDTH = 1000
HEIGHT = 1100
FPS = 30
DEFAULT_IMAGE_SIZE = (40, 40)
DEFAULT_BAT_SIZE = (100, 100)
DEFAULT_PITCH_SIZE = (800, 1000)
DEFAULT_BOWLER_SIZE = (250, 250)

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

# Initiate variables for scoring
score = 0
miss = 0

game_time_seconds = 30

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Bowler(pygame.sprite.Sprite):
    # sprite for the bowler
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bumrah1.png")).convert()
        self.image = pygame.transform.scale(self.image, DEFAULT_BAT_SIZE)
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 1000
        self.speedx = 5

    def update(self):
        # get all the keys that were pressed
        keystate = pygame.key.get_pressed()
        # figure out which key was pressed
        # This actually moves the rectangle
        self.rect.x += self.speedx

        # Trying to ensure the bowler doesnt go beyond boundaries
        if self.rect.right > (WIDTH - 150):
            self.rect.right = WIDTH - 150
            self.speedx = -5
        if self.rect.left < 200:
            self.rect.left = 200
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
        self.rect.bottom = HEIGHT - 125
        self.speedx = 0
        self.rot = 0

    def update(self):
        self.speedx = 0
        # get all the keys that were pressed
        keystate = pygame.key.get_pressed()
        # figure out which key was pressed
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
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
        self.speedy = random.randrange(20, 50)
        self.missed = False

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            if not self.missed:
                self.missed = True
                print("Ball missed!")

    def goup(self):
        self.speedy = -100


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
balls = pygame.sprite.Group()
badaboom_monkey = Bowler()
all_sprites.add(badaboom_monkey)
all_sprites.add(bat)

# Game loop
running = True
start_time = time.time()
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
                print("scream-crowd")

    # Update
    all_sprites.update()

    # check if a ball was hit by the bat
    hits = pygame.sprite.spritecollide(bat, balls, False)
    if hits:
        score += 1
        # running = False
        for ball in hits:
            ball.goup()

    # Count and remove missed balls correctly
    # Count and remove missed balls correctly
    missed_balls = [ball for ball in balls if ball.missed]  # Collect missed balls BEFORE killing them

    if missed_balls:
        print(f"Found {len(missed_balls)} missed balls")

    for ball in missed_balls:
        miss += 1
        print(f"Missed count: {miss}")  # Debug print
        ball.kill()  # Properly remove ball from all sprite groups

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    current_time = time.time()
    draw_text(screen, "Hits :" + str(score), 18, WIDTH - 50, 20)
    elapsed_time = current_time - start_time
    str_elapsed_time = round(elapsed_time, 0)
    draw_text(screen, "Time :" + str(str_elapsed_time), 18, WIDTH - 50, 40)
    draw_text(screen, "Missed balls :" + str(miss), 18, WIDTH - 70, 60)
    # *after* drawing everything flip the display
    pygame.display.flip()
    if (elapsed_time > game_time_seconds):
        running = False

print(score)
# Game over screen
screen.fill(BLACK)
draw_text(screen, "Game Over!", 40, WIDTH / 2, HEIGHT / 3)
draw_text(screen, f"Hits: {score - miss}", 30, WIDTH / 2, HEIGHT / 2)
draw_text(screen, f"Missed Balls: {miss}", 30, WIDTH / 2, HEIGHT / 1.8)
total_balls_faced = score + miss
reaction_time = score/game_time_seconds
if score > 0:
    divide_by = game_time_seconds
    if (score + miss) < game_time_seconds:
        divide_by = score + miss
        reaction_time = score / divide_by

reaction_time = round(reaction_time, 3)
overall_score_level = round(((score - miss) / total_balls_faced) * 100, 2)
draw_text(screen, f"Overall score: {overall_score_level}", 30, WIDTH / 2, HEIGHT / 1.6)
draw_text(screen, f"Reaction time: {reaction_time} hits per second", 30, WIDTH / 2, HEIGHT / 1.4)

pygame.display.flip()

# Pause before quitting
time.sleep(5)
pygame.quit()
