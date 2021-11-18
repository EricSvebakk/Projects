
from gameboard import Gameboard
from random import randint as ri
import pygame


backgroundColour = (50, 50, 50)

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("A* Search Algorithm")

timerObject = pygame.time.Clock()

size = 100
start = [ri(0, size-1), ri(0, size-1)]
end = [ri(0, size-1), ri(0, size-1)]
gameboard = Gameboard(pygame, size, start, end, 30)

screen.fill(backgroundColour)
gameboard.drawGrid(screen)
pygame.display.flip()

dragging = False

#=============================================================================
# Gameloop variable
running = True
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
			dragging = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				running = False
			
			elif event.key == pygame.K_c:
				gameboard.clearBoard()
				gameboard.drawGrid(screen)
				print("Board cleared")

			elif event.key == pygame.K_r:
				gameboard.randomizeCells()
				gameboard.drawGrid(screen)
				# gameboard.createGrid(start, end)
				# screen.fill(backgroundColour)
				# gameboard.drawAll(screen)
			
			elif event.key == pygame.K_p:
				start = [ri(0, size-1), ri(0, size-1)]
				end = [ri(0, size-1), ri(0, size-1)]
				gameboard.pickPoints(start,end)
				gameboard.drawGrid(screen)
				
				
			elif event.key == pygame.K_i:
				print("path:      ", gameboard.path)
				print("openSet:   ", gameboard.openSet)
				print("closedSet: ", gameboard.closedSet)
			
			elif event.key == pygame.K_SPACE:
				if gameboard.isPaused():
					gameboard.unpause()
					print(f"board running ({pygame.FPS})")
				else:
					gameboard.pause()
					print(f"board stopped ({pygame.FPS})")
			
			elif event.key == pygame.K_UP:
				gameboard.incrementFrequency(1)
				print(f"speed increased (FPS:{gameboard.getFrequency()})")

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
