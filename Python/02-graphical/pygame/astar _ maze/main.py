
from gameboard import Gameboard
import pygame
import time
from random import randint as ri


backgroundColour = (255,255,255)

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("A* Search Algorithm")

size = 100
start = [ri(0, size-1), ri(0, size-1)]
end = [ri(0, size-1), ri(0, size-1)]
gameboard = Gameboard(pygame, size, start, end, 30)

screen.fill(backgroundColour)
gameboard.drawAll(screen)
pygame.display.flip()

#=============================================================================
# Gameloop variable
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_r:
                start = [ri(0, size-1), ri(0, size-1)]
                end = [ri(0, size-1), ri(0, size-1)]
                gameboard.generate(start, end)
                screen.fill(backgroundColour)
                gameboard.drawAll(screen)

    # screen.fill(backgroundColour)
    gameboard.update()
    # gameboard.drawAll(screen)
    gameboard.draw(screen)
    pygame.display.flip()
