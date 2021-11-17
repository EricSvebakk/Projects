
from os import system as sys
from random import randint

import pygame
from cell import Cell

class Gameboard:
	
	def __init__(self, pygame, size, survive=[2,3], born=[3], wrapAround=False):
		"""The Gameboard class-object requires a number
		for rows and columns to initialize"""
		
		self._pygame = pygame
		
		(self._width, self._height) = self._pygame.display.get_surface().get_size()
		self._rows = size
		self._cols = size
		self._grid = []
		
		self._updateFrequency = 5
		self._pauseFrequency = 80
		self._pygame.FPS = self._pauseFrequency
		self._allowUpdate = True

		self._wrapAround = wrapAround
		
		self._mouseMode = 1
		
		self._selectedCellX = 0
		self._selectedCellY = 0
		
		self._survive = survive
		self._born = born

		self.generate()

	def generate(self):
		""" A method for creating the board with the specified\n
		dimensions and filling it with cells."""

		self._grid = []

		# Loop for creating each row
		for y in range(self._cols):
			self._grid.append([])

			# Loop for adding cells to each row
			for x in range(self._rows):
				
				
				cell = Cell(self._pygame)

				# Each cell has a 1/3 chance to start
				# generation 0 being alive
				if randint(0, 2) == 1:
					cell.alive()

				self._grid[y].append(cell)
	
	def pause(self):
		self._allowUpdate = True
		self._pygame.FPS = self._pauseFrequency
		
	def unpause(self):
		self._pygame.FPS = self._updateFrequency
		self._allowUpdate = False
	
	def isPaused(self):
		return self._allowUpdate
		
	def updateFrequency(self, increment):
		self._updateFrequency += increment
		self._pygame.FPS = self._updateFrequency
	
	def getFrequency(self):
		return self._updateFrequency

	# A method for drawing the current state of the board
	def drawBoard(self, screen, debug=False):

		cWidth = self._width / self._rows
		cHeight = self._height / self._cols
		b = [255, 50, 0]

		# self._grid[self._selectedCellX][self._selectedCellY].draw(
		# 	self._selectedCellX * cWidth,
		# 	self._selectedCellY * cHeight,
		# 	cWidth,
		# 	cHeight,
		# 	(255, 0, 0),
		# 	screen
		# 	)

		for y in range(self._cols):
			for x in range(self._rows):

				xPos = x * cWidth
				yPos = y * cHeight

				obj = self._grid[y][x]
				
				if obj.isUnlocked():
					if obj.isAlive():
						colour = (b[0], b[0], b[0])
					else:
						colour = (b[1], b[1], b[1])
				else:
					colour = (b[2], b[2], b[2])
				
				if obj.isAlive() or not obj.isUnlocked():
					obj.draw(xPos, yPos, cWidth, cHeight, colour, screen)

				if x == y and x == self._cols-1 - y:
					obj.draw(xPos, yPos, cWidth, cHeight, (0, 0, 255), screen)

				if x == y and x == self._cols-2 - y:
					obj.draw(xPos, yPos, cWidth, cHeight, (0, 0, 255), screen)

	#
	def clearBoard(self):
		
		for y in range(self._cols):
			for x in range(self._rows):

				self._grid[y][x].dead()
				self._grid[y][x].unlock()

	# A method which returns all neighbouring cells to a specified cell-position
	def findNeighbours(self, xC:int, yC:int) -> list:

		neighbours = []

		# iterates over the cells "above" and
		# "below" of a specified cell-position
		for yi in range(-1, 2):
			yi += yC

			# y-positions which are too small
			# or too large are skipped
			if self._wrapAround:
				if yi < 0:
					yi = self._cols-1
					
				elif yi > self._cols-1:
					yi = 0
			else:
				if yi < 0 or yi > self._cols-1:
					continue
			
			# iterates over the cells "left" and
			# "right" of a specified cell-position
			for xi in range(-1, 2):
				xi += xC

				# x-positions which are too small
				# or too large are skipped
				if self._wrapAround:
					if xi < 0:
						xi = self._rows-1

					elif xi > self._rows-1:
						xi = 0
				else:
					if xi < 0 or xi > self._rows-1:
						continue

				# The cell specified for findNeighbours() is 
				# not included among the list of neighbours
				if yi == yC and xi == xC:
					continue
				
				# The remainder of positions (which are all valid positions)
				# are added to the list of neighbours
				else:
					neighbours.append(self._grid[yi][xi])

		return neighbours

	# A method which follows the rules of "The Game Of Life" and
	# updates every cell on the gameboard and increases the current generation
	def update(self):

		changeToAlive = []
		changeToDead = []

		# Nested for-loop for iterating over every cell
		for y in range(self._cols):
			for x in range(self._rows):
				
				# Gets the surrounding neighbour cells for
				# the cell with position (x,y)
				neighbours = self.findNeighbours(x, y)
				aliveNeighbours = 0

				for neighbour in neighbours:
					if neighbour.isAlive():
						aliveNeighbours += 1

				# An if-statement which determines if a cell
				# updates from alive to dead in the next generation
				if self._grid[y][x].isAlive():
					if aliveNeighbours not in self._survive:
						changeToDead.append(self._grid[y][x])

				# An if-statement which determines if a cell
				# updates from dead to alive in the next generation
				else:
					if aliveNeighbours in self._born:
						changeToAlive.append(self._grid[y][x])

		# Two for-loops for flipping the state of certain cells
		for cell in changeToAlive:
			cell.alive()
		for cell in changeToDead:
			cell.dead()

	def setMouseMode(self, _mouseMode):
		self._mouseMode = _mouseMode

	#
	def selectWithMouse(self, mouseX, mouseY):
		
		if not self.isPaused():
			return 
		
		obj = None
		
		cWidth = self._width / self._rows
		cHeight = self._height / self._cols

		# keyX = 0
		# keyX = 0

		for y in range(self._cols):
			for x in range(self._rows):

				x1 = x * cWidth
				y1 = y * cHeight
				x2 = x1 + cWidth
				y2 = y1 + cHeight
				obj = self._grid[y][x]

				if mouseX >= x1 and mouseX < x2:
					if mouseY >= y1 and mouseY < y2:
						
						if self._mouseMode == 1:
							obj.alive()
						elif self._mouseMode == 2:
							obj.lock()
						elif self._mouseMode == 3:
							obj.dead()
							obj.unlock()
							
						self._selectedCellX = x
						self._selectedCellY = y
						# keyX = x
						# keyY = y
	
		# print("POS:", keyX, keyY)
		# return (keyX, keyY)

	#
	# def selectWithKeys(self, keyX, keyY):

	#     cWidth = self._width / self._rows
	#     cHeight = self._height / self._cols

	#     keyX = (keyX * cWidth) + cWidth/2
	#     keyY = (keyY * cHeight) + cHeight/2

	#     for y in range(self._cols):
	#         for x in range(self._rows):

	#             x1 = x * cWidth
	#             y1 = y * cHeight
	#             x2 = x1 + cWidth
	#             y2 = y1 + cHeight
	#             obj = self._grid[y][x]

	#             if keyX > x1 and keyX < x2:
	#                 if keyY > y1 and keyY < y2:

	#                     if obj.isAlive() and obj.isUnlocked():
	#                         obj.dead()
	#                         obj.lock()

	#                     elif not obj.isAlive() and not obj.isUnlocked():
	#                         obj.unlock()

	#                     elif not obj.isAlive() and obj.isUnlocked():
	#                         obj.alive()
