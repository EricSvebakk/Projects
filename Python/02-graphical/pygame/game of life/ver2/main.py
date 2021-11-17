
from gameboard import Gameboard
from cell import Cell
from os import system as sys, environ
import pygame


# Display size, title and attributes
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Game of Life")


# Game of Life: S23/B3
# Day & night:  S24678/B3678
# Seed:         S/B2
# Gnarl:        S1/B1
gameboard = Gameboard(pygame, 100, [2,3], [3], True)


# Game-loop variables
running = True
dragging = False

timerObject = pygame.time.Clock()

backgroundColour = (50, 50, 50)

screen.fill(backgroundColour)
gameboard.drawBoard(screen)
pygame.display.flip()


# Gameloop
while running:

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				dragging = True
				(xPos, yPos) = pygame.mouse.get_pos()
				gameboard.setMouseMode(1)
				gameboard.selectWithMouse(xPos, yPos)
				
			elif event.button == 3:
				dragging = True
				(xPos, yPos) = pygame.mouse.get_pos()
				gameboard.setMouseMode(3)
				gameboard.selectWithMouse(xPos, yPos)
			
		elif event.type == pygame.MOUSEMOTION:
			if dragging:
				(xPos, yPos) = pygame.mouse.get_pos()
				gameboard.selectWithMouse(xPos, yPos)

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				dragging = False

		elif event.type == pygame.KEYDOWN:
			sys("cls")

			if event.key == pygame.K_q:
				running = False

			elif event.key == pygame.K_c:
				gameboard.clearBoard()
				print("Board cleared")

			elif event.key == pygame.K_r:
				gameboard.generate()
				print("Board regenerated!")
					
			# elif event.key == pygame.K_1:
			# 	gameboard.setMouseMode(1)
			
			# elif event.key == pygame.K_2:
			# 	gameboard.setMouseMode(2)
			
			# elif event.key == pygame.K_3:
			# 	gameboard.setMouseMode(3)

			elif event.key == pygame.K_SPACE:
				if gameboard.isPaused():
					gameboard.unpause()
					print(f"board running ({pygame.FPS})")
				else:
					gameboard.pause()
					print(f"board stopped ({pygame.FPS})")
			
			elif event.key == pygame.K_UP:
				gameboard.updateFrequency(1)
				print(f"speed increased (FPS:{gameboard.getFrequency()})")

			elif event.key == pygame.K_DOWN:
				if gameboard.getFrequency() <= 1:
					print(f"speed not decreased (FPS:{gameboard.getFrequency()})")
				else:
					gameboard.updateFrequency(-1)
					print(f"speed decreased (FPS:{gameboard.getFrequency()})")
	
		screen.fill(backgroundColour)
		gameboard.drawBoard(screen)
		pygame.display.flip()

	if not gameboard.isPaused():
		gameboard.update()
		screen.fill(backgroundColour)
		gameboard.drawBoard(screen)
		pygame.display.flip()

	timerObject.tick(pygame.FPS)
