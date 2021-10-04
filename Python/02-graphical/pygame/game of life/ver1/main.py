
from gameboard import Gameboard
from cell import Cell
from os import system as sys
import pygame

# from optparse import OptionParser
# import inspect

# for i in inspect.getmembers(OptionParser, predicate=inspect.isfunction):
#     print(i[0])

# for i in dir(Gameboard):
#     if "_" not in i:
#         print(f"- {i}")

backgroundColour = (50, 50, 50)

screen = pygame.display.set_mode((595, 595),pygame.RESIZABLE)
pygame.display.set_caption("Game of Life")
# print(pygame.display.Info())
# print(pygame.display.mode_ok((600,600),0,8))


# Game of Life: S23B/3
# Day & night:  S24678/B3678
# Seed:         S/B2
# Gnarl:        S1/B1
gameboard = Gameboard(pygame, 119, [1], [4])

xPos = 0
yPos = 0

# Game loop
runLoop = False
running = True
toggle = True

step = 5000
time = 50_000
clock = time

screen.fill(backgroundColour)
gameboard.drawBoard(screen, xPos, yPos)
pygame.display.flip()

while running:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            (xPos, yPos) = pygame.mouse.get_pos()
            (xPos, yPos) = gameboard.selectWithMouse(xPos, yPos)

        if event.type == pygame.KEYDOWN:
            sys("cls")

            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_c:
                gameboard.clearBoard()
                print("Board cleared")

            elif event.key == pygame.K_r:
                gameboard.generate()
                print("Board regenerated!")

            elif event.key == pygame.K_RSHIFT:
                if not toggle:
                    toggle = True
                    print(f"keys toggled: speed control")
                else:
                    toggle = False
                    print(f"keys toggled: moveable brush")

            if not toggle:
                if event.key == pygame.K_UP:
                    yPos -= 1

                elif event.key == pygame.K_RIGHT:
                    xPos += 1

                elif event.key == pygame.K_DOWN:
                    yPos += 1

                elif event.key == pygame.K_LEFT:
                    xPos -= 1
                elif event.key == pygame.K_SPACE:
                    gameboard.selectWithKeys(xPos, yPos)

            else:
                if event.key == pygame.K_UP:
                    time -= step
                    print(f"speed increased:{10-round(time/step, 3)}")

                elif event.key == pygame.K_DOWN:
                    time += step
                    print(f"speed decreased:{10-round(time/step, 3)}")

                elif event.key == pygame.K_SPACE:
                    if not runLoop:
                        runLoop = True
                        print("board running")
                    else:
                        runLoop = False
                        print("board stopped")

        screen.fill(backgroundColour)
        gameboard.drawBoard(screen, xPos, yPos)
        pygame.display.flip()

    clock -= 1
    if runLoop and clock <= 0:
        gameboard.update()
        screen.fill(backgroundColour)
        gameboard.drawBoard(screen, xPos, yPos)
        pygame.display.flip()
        clock = time
