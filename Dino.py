import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Chrome Game")

# Set up the clock
clock = pygame.time.Clock()

# Game variables
dinosaur_rect = pygame.Rect(50, HEIGHT - GROUND_HEIGHT - 50, 50, 50)
dinosaur_speed = 0
jump_height = 100
is_jumping = False

cactus_list = []
spawn_timer = 0
score = 0
high_score = 0

# Load high score from file
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save high score to file
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))

            pygame.quit()
            sys.exit()

    # Update
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping and dinosaur_rect.y == HEIGHT - GROUND_HEIGHT - 50:
        is_jumping = True
        jump_height = 100

    if is_jumping:
        dinosaur_rect.y -= 5
        jump_height -= 5
        if jump_height <= 0:
            is_jumping = False

    if not is_jumping and dinosaur_rect.y < HEIGHT - GROUND_HEIGHT - 50:
        dinosaur_rect.y += 5  # Gravity

    spawn_timer += 1
    if spawn_timer == 45:
        spawn_timer = 0
        cactus_list.append(pygame.Rect(WIDTH, HEIGHT - GROUND_HEIGHT - 30, 20, 30))

    for cactus in cactus_list:
        cactus.x -= 5
        if dinosaur_rect.colliderect(cactus):
            print("Game Over! Score:", score)

            # Update high score
            if score > high_score:
                high_score = score

            # Save high score to file
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))

            pygame.quit()
            sys.exit()

    cactus_list = [cactus for cactus in cactus_list if cactus.x > -50]

    # Check for score increase
    for cactus in cactus_list:
        if cactus.x == dinosaur_rect.x:
            score += 1

    # Draw
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))  # Ground

    pygame.draw.rect(screen, RED, dinosaur_rect)  # Dinosaur
    for cactus in cactus_list:
        pygame.draw.rect(screen, BLACK, cactus)  # Cactus

    # Display Score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display High Score
    high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
    screen.blit(high_score_text, (10, 40))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
