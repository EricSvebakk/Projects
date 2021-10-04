
from gameboard import Gameboard
from math import pi
import pygame

# Background fill colour
backgroundColour = (128, 81, 9)

# Specifies window properties
width = 800
height = 600
pygame.display.set_caption("Elastic Collision")
screen = pygame.display.set_mode((width, height))

# gameboard is a class for creating objects inside the pygame window.
gameboard = Gameboard(pygame, [0, width], [0, height])

# .physicsProperties defines how objects are affected inside the pygame window
# gameboard.physicsProperties([pi, 0.001], 0.01, 0.75)
gameboard.physicsProperties(False, 0.00, 1)

# .generate specifies how many particle objects to create.
gameboard.addParticles(8)

time = 10 * 1000000

# Game loop
running = True
while running:

    # For-loop that tests for specific inputs
    for event in pygame.event.get():
        
        # Stops program if pygame window is closed
        if event.type == pygame.QUIT:
            running = False

        # Selects a given object if the mouse is clicked and
        # the objects position matches the cursors position
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            gameboard.selectObject(mouseX, mouseY)
        
        # Deselects any given object if the mouse is no longer clicked
        if event.type == pygame.MOUSEBUTTONUP:
            gameboard.selectedParticle = None
        
        # Ends program with "Q"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            
    
    # Draws the background
    screen.fill(backgroundColour)

    # Updates and draws all particle objects
    gameboard.update()
    gameboard.display(screen)

    # Updates screen with current content
    pygame.display.flip()

    time -= 1
    if time < 0:
        running = False

# ???
total = 0
for i in gameboard.particleList:
    total += i.maxSpeed
print(total)