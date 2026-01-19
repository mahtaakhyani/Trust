import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the paddle (single player)
paddle_width = 10
paddle_height = 60
paddle_speed = 5
paddle_pos = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Left wall position (static)
wall_x = 0

# Set up the ball
ball_radius = 10
ball_speed_x = 3
ball_speed_y = 3
ball_pos = pygame.Rect(width // 2 - ball_radius // 2, height // 2 - ball_radius // 2, ball_radius, ball_radius)
ball_direction = random.choice([-1, 1])

# Set up the game clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_pos.y > 0:
        paddle_pos.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_pos.y < height - paddle_height:
        paddle_pos.y += paddle_speed

    # Move the ball
    ball_pos.x += ball_speed_x * ball_direction
    ball_pos.y += ball_speed_y

    # Check for collision with left wall
    if ball_pos.x <= wall_x:
        ball_direction *= -1
        ball_pos.x = wall_x  # Prevent ball from going through wall
    
    # Check for collision with paddle
    if ball_pos.colliderect(paddle_pos):
        ball_direction *= -1

    # Check for collisions with walls
    if ball_pos.y <= 0 or ball_pos.y >= height - ball_radius:
        ball_speed_y *= -1

    # Check for scoring (ball goes past the right side)
    if ball_pos.x >= width - ball_radius:
        # Reset ball position
        ball_pos.x = width // 2 - ball_radius // 2
        ball_pos.y = height // 2 - ball_radius // 2

        # Reset ball speed
        ball_speed_x = 3
        ball_speed_y = 3
        ball_direction = random.choice([-1, 1])

    # Clear the window
    window.fill(BLACK)

    # Draw the left wall, paddle, and ball
    pygame.draw.line(window, WHITE, (wall_x, 0), (wall_x, height), 2)
    pygame.draw.rect(window, WHITE, paddle_pos)
    pygame.draw.ellipse(window, WHITE, ball_pos)

    # Update the window
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
