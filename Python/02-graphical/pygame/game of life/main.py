
from gameboard import Gameboard
from os import system as sys
import pygame


# Display size, title and attributes
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Game of Life")


# Game of Life : S23 / B3
# Day & night  : S24678 / B3678
# Seed         : S / B2
# Gnarl        : S1 / B1
gameboard = Gameboard(pygame, 100, [2,3], [3], True)


# Game-loop variables
running = True
dragging = False

timerObject = pygame.time.Clock()

backgroundColour = (50, 50, 50)

screen.fill(backgroundColour)
gameboard.drawBoard(screen)
pygame.display.flip()


# gameloop
while running:

	for event in pygame.event.get():
		
		# Ends gameloop
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
		
			# left-click adds living cells
			if event.button == 1:
				dragging = True
				(xPos, yPos) = pygame.mouse.get_pos()
				gameboard.setMouseMode(1)
				gameboard.selectWithMouse(xPos, yPos)
			
			# right-click clears cells
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
			if event.button == 1 or event.button == 3:
				dragging = False

		elif event.type == pygame.KEYDOWN:
			sys("cls")

			# Ends gameloop
			if event.key == pygame.K_q:
				running = False

			# clears all cells
			elif event.key == pygame.K_c:
				gameboard.clearBoard()

			# randomizes all cells
			elif event.key == pygame.K_r:
				gameboard.generate()
			
			# increases brush size
			elif event.key == pygame.K_RIGHT:
				gameboard.increaseSelectSize()
				gameboard.showBrushSize()

			# decreases brush size
			elif event.key == pygame.K_LEFT:
				gameboard.decreaseSelectSize()
				gameboard.showBrushSize()
			
			# increments timestep of gameloop
			elif event.key == pygame.K_UP:
				gameboard.updateFrequency(1)
				gameboard.showFPS()
			
			# decrements timestep of gameloop
			elif event.key == pygame.K_DOWN:
				gameboard.updateFrequency(-1)
				gameboard.showFPS()
				
			# pauses/unpauses gameloop
			elif event.key == pygame.K_SPACE:
				gameboard.showFPS()
				if gameboard.isPaused():
					gameboard.unpause()
				else:
					gameboard.pause()
	
		screen.fill(backgroundColour)
		gameboard.drawBoard(screen)
		pygame.display.flip()

	# updates board logic and content
	if not gameboard.isPaused():
		gameboard.update()
		screen.fill(backgroundColour)
		gameboard.drawBoard(screen)
		pygame.display.flip()

	timerObject.tick(pygame.FPS)
