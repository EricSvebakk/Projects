
from gameboard import Gameboard
from cell import Cell
from os import system as sys
import pygame

backgroundColour = (50, 50, 50)

# Initial game speed
pygame.FPS = 10
timerObject = pygame.time.Clock()

# Display size, title and attributes
screen = pygame.display.set_mode((600, 600),pygame.RESIZABLE)
pygame.display.set_caption("Game of Life")
# print(pygame.display.Info())
# print(pygame.display.mode_ok((600,600),0,8))


# Game of Life: S23/B3
# Day & night:  S24678/B3678
# Seed:         S/B2
# Gnarl:        S1/B1
gameboard = Gameboard(pygame, 40, [2,3], [3])

xPos = 0
yPos = 0
obj = None

# Game-loop variables
runLoop = False
running = True
toggle = True

screen.fill(backgroundColour)
gameboard.drawBoard(screen, xPos, yPos)
pygame.display.flip()

# Gameloop
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

            elif event.key == pygame.K_UP:
                pygame.FPS += 1
                print(f"speed increased (FPS:{pygame.FPS})")

            elif event.key == pygame.K_DOWN:
                if pygame.FPS <= 1:
                    print(f"speed not decreased (FPS:{pygame.FPS})")
                else:
                    pygame.FPS -= 1
                    print(f"speed decreased (FPS:{pygame.FPS})")

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

    if runLoop:
        gameboard.update()
        screen.fill(backgroundColour)
        gameboard.drawBoard(screen, xPos, yPos)
        pygame.display.flip()

    timerObject.tick(pygame.FPS)
    
# print("\n===============")
# for i in list(globals()):
#     if "_" not in i:

#         if type(i) == object:
#             print(i)
#             for j in dir(i):
#                 if "_" not in j:
#                     print(j)
#         else:
#             print(i)

# while (command := input("> ")) != "exit":
#     eval(command)
