
from gameboard import Gameboard
from random import randint as ri
from os import system as sys
import pygame


screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("A* Search Algorithm")


size = 100
start = [ri(0, size-1), ri(0, size-1)]
end = [ri(0, size-1), ri(0, size-1)]

gameboard = Gameboard(pygame, size, start, end, 30)


# Game-loop variables
running = True
dragging = False

timerObject = pygame.time.Clock()

backgroundColour = (50, 50, 50)

screen.fill(backgroundColour)
gameboard.drawGrid(screen)
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
			dragging = False

		elif event.type == pygame.KEYDOWN:
			sys("cls")
			
			# Ends gameloop
			if event.key == pygame.K_q:
				running = False
			
			# clears all cells
			elif event.key == pygame.K_c:
				gameboard.clearBoard()
				gameboard.drawGrid(screen)
				print("Board cleared")

			# randomizes walls
			elif event.key == pygame.K_r:
				gameboard.randomizeCells()
				gameboard.drawGrid(screen)
				# gameboard.createGrid(start, end)
				# screen.fill(backgroundColour)
				# gameboard.drawAll(screen)
			
			# randomizes start/end-point
			elif event.key == pygame.K_p:
				start = [ri(0, size-1), ri(0, size-1)]
				end = [ri(0, size-1), ri(0, size-1)]
				gameboard.pickPoints(start,end)
				gameboard.drawGrid(screen)
				
			# debug-info
			elif event.key == pygame.K_i:
				print("path:      ", gameboard.path)
				print("openSet:   ", gameboard.openSet)
				print("closedSet: ", gameboard.closedSet)
			
			# pauses/unpauses gameloop
			elif event.key == pygame.K_SPACE:
				if gameboard.isPaused():
					gameboard.unpause()
					print(f"board running ({pygame.FPS})")
				else:
					gameboard.pause()
					print(f"board stopped ({pygame.FPS})")
			
			# increments timestep of gameloop
			elif event.key == pygame.K_UP:
				gameboard.incrementFrequency(1)
				print(f"speed increased (FPS:{gameboard.getFrequency()})")

			# decrements timestep of gameloop
			elif event.key == pygame.K_DOWN:
				if gameboard.getFrequency() <= 1:
					print(f"speed not decreased (FPS:{gameboard.getFrequency()})")
				else:
					gameboard.incrementFrequency(-1)
					print(f"speed decreased (FPS:{gameboard.getFrequency()})")

		# screen.fill(backgroundColour)
		gameboard.drawGrid(screen)	
		gameboard.draw(screen)
		pygame.display.flip()
	
	if not gameboard.isPaused():
		# screen.fill(backgroundColour)
		gameboard.update()
		gameboard.draw(screen)
		pygame.display.flip()
	
	timerObject.tick(pygame.FPS)
