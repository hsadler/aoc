import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Define a color with alpha (50% opacity)
red_with_alpha = (255, 0, 0, 128)

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
suface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Pygame Circle with Alpha")

def draw_screen():
    pygame.draw.rect(surface=suface, color=red_with_alpha, rect=(0, 0, WIDTH/2, HEIGHT/2))
    # pygame.draw.circle(screen, red_with_alpha, (400, 300), 50)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Clear the screen
    screen.fill("black")
    screen.blit(suface, (0, 0))
    draw_screen()
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
