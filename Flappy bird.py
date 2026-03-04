import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 55

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_speed = 4
bird_size = 30
bird_color = BLUE  # Change bird color

# Gravity and jump variables
gravity = 1
jump = -15
bird_velocity = 0

# Pillar properties
pipe_width = 50
pipe_height = 300
pipe_gap = 200
pipe_speed = 4
pipes = []

# Score and high score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Load high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Save high score to a file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def draw_bird(x, y):
    pygame.draw.circle(screen, bird_color, (x, y), bird_size)

def draw_pipe(pipe_x, opening_y):
    pipe_color = GREEN  # Change pillar color
    pygame.draw.rect(screen, pipe_color, (pipe_x, 0, pipe_width, opening_y))
    pygame.draw.rect(screen, pipe_color, (pipe_x, opening_y + pipe_gap, pipe_width, HEIGHT - opening_y - pipe_gap))

def game_over():
    global bird_y, bird_velocity, score, high_score, pipes

    # Update high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    text = font.render(f"Game Over! Score: {score} High Score: {high_score}", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)

    # Reset game variables
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipes = []

def main():
    global bird_y, bird_velocity, score, high_score

    # Load high score at the beginning
    high_score = load_high_score()

    fullscreen = False
    screen_mode = 0  # 0 for windowed, 1 for fullscreen
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Wait for right mouse button press to start the game
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse button
                waiting_for_start = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump
                elif event.key == pygame.K_r:  # Restart on 'R' key press
                    game_over()

            # Toggle fullscreen on 'F' key press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen_mode = pygame.FULLSCREEN
                else:
                    screen_mode = 0
                pygame.display.set_mode((WIDTH, HEIGHT), screen_mode)

        # Update bird position and velocity
        bird_velocity += gravity
        bird_y += bird_velocity

        # Check for collision with the ground
        if bird_y > HEIGHT:
            game_over()

        # Generate pillars
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            opening_y = random.randint(pipe_gap, HEIGHT - pipe_gap)
            pipes.append([WIDTH, opening_y])

        # Update pillar positions
        for pipe in pipes:
            pipe[0] -= pipe_speed

        # Check for collision with pillars
        for pipe in pipes:
            if bird_x < pipe[0] + pipe_width and bird_x + bird_size > pipe[0]:
                if bird_y < pipe[1] or bird_y + bird_size > pipe[1] + pipe_gap:
                    game_over()

        # Check for passing pillars
        if pipes and bird_x > pipes[0][0] + pipe_width:
            pipes.pop(0)
            score += 1

        # Draw background
        screen.fill(WHITE)

        # Draw pillars
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1])

        # Draw bird
        draw_bird(bird_x, int(bird_y))

        # Draw score
        score_text = font.render(f"Score: {score} High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Set the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()