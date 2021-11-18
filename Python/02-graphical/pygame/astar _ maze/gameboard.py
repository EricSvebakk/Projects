
from cell import Cell
import math
from random import randint

class Gameboard:
	
	def __init__(self, pygame, size, start, end, wallChance):
		
		self.pygame = pygame
		
		self.size = size
		(self.width, self.height) = pygame.display.get_surface().get_size()

		# 
		self.cWidth = self.width / size
		self.cHeight = self.height / size
		
		# 
		self.wallChance = wallChance
		
		# 
		self.startCell = None
		self.endCell = None
		self.current = None
		
		# 
		self.backgroundCellColour = (50, 50, 50)
		self.wallCellColour = (0, 0, 0)
		
		self.startColour = (255, 0, 255)
		self.endColour = (255, 255, 255)
		self.pathColour = (0, 80, 0)
		
		self.closedSetColour = (255, 0, 0)
		self.openSetColour = (100, 200, 100)

		self.updateFrequency = 100
		self.pauseFrequency = 80
		self.pygame.FPS = self.pauseFrequency
		self.allowUpdate = True
		self._mouseMode = 1

		# 
		self.closedSet = []
		self.openSet = []
		
		# 
		self.path = []
		self.oldPath = []

		# 
		self.grid = []
		self.createGrid()
		self.randomizeCells()
		self.pickPoints(start, end)

	#=============================================================================
	def resetData(self):
		
		if self.startCell:
			self.startCell.wall = False
		
		if self.endCell:
			self.endCell.wall = False
		
		self.current = None
		
		self.openSet = []
		self.closedSet = []
		self.path = []
		self.oldPath = []
		self.openSet.append(self.startCell)
		
	
	def createGrid(self):
		
		# Cell generation code
		for y in range(self.size):
			self.grid.append([])
			for x in range(self.size):
				cell = Cell(int(x), int(y), self.cWidth, self.cHeight)
				self.grid[y].append(cell)

		# Update each cell with their corresponding neighbours
		for y in range(self.size):
			for x in range(self.size):
				
				cell = self.grid[y][x]
				cell.findNeighbours(self.grid, self.size)
				
		self.resetData()


	def randomizeCells(self):
		
		for y in range(self.size):
			for x in range(self.size):
				
				cell = self.grid[y][x]
				
				if randint(0, int(100/self.wallChance)-1) == 0:
					cell.wall = True
				else:
					cell.wall = False
		
		# # Wall generation code
		# for y in range(self.size):
		#     for x in range(self.size):

		#         cell = self.grid[y][x]

		#         if cell.x - 1 > 0 and cell.x < self.size-1:
		#             if cell.y - 1 > 0 and cell.y < self.size-1:

		#                 if self.grid[cell.y-1][cell.x].wall:
		#                     if randint(0, 1) == 0:
		#                         cell.wall = True

		#                 if self.grid[cell.y][cell.x-1].wall or self.grid[cell.y][cell.x+1].wall:
		#                     cell.wall = False
		
		self.resetData()
	
		
	def clearBoard(self):

		for y in range(self.size):
			for x in range(self.size):
				self.grid[y][x].wall = False

		self.resetData()
	
	
	def pickPoints(self, start, end):
				
		# Sets self.start to the corresponding cell for the given grid-coordinates
		self.startCell = self.grid[start[1]][start[0]]

		# # start cell is first cell to be checked in the open-set
		# self.openSet.append(self.startCell)

		# Sets self.end to the corresponding cell for the given grid-coordinates
		self.endCell = self.grid[end[1]][end[0]]

		self.resetData()

	#=============================================================================
	def update(self):

		if self.current is self.endCell:
			return

		if len(self.openSet) > 0:

			index = 0
			for i in range(len(self.openSet)):
				if self.openSet[i].f < self.openSet[index].f:
					index = i

			self.current = self.openSet[index]
			self.openSet.pop(index)
			self.closedSet.append(self.current)

			currentNeighbours = self.current.neighbours

			for i in range(len(currentNeighbours)):
				cell = currentNeighbours[i]
				
				if cell not in self.closedSet and not cell.wall:
					tempG = self.current.g + self.heuristic(cell, self.current)

					newPath = False
					if cell in self.openSet:
						if tempG < cell.g:
							cell.g = tempG
							newPath = True
					else:
						cell.g = tempG
						newPath = True
						self.openSet.append(cell)

					if newPath:
						cell.h = self.heuristic(cell, self.endCell)
						cell.f = cell.g + cell.h
						cell.previous = self.current

		else:
			print("no solution")
			return

		self.path = []
		temp = self.current
		self.path.append(temp)
		if temp != None:
			while temp.previous:
				self.path.append(temp.previous)
				temp = temp.previous


	#=============================================================================
	def drawGrid(self, screen):

		colour = None
		
		for y in range(self.size):
			for x in range(self.size):

				cell = self.grid[y][x]

				if cell.wall:
					colour = self.wallCellColour
				else:
					colour = self.backgroundCellColour
					# continue

				self.grid[y][x].draw(self.pygame, screen, colour)

	#=============================================================================
	def draw(self, screen):

		colour = None

		for y in range(self.size):            
			for x in range(self.size):
				
				cell = self.grid[y][x]

				if cell is self.startCell:
					colour = self.startColour
					
				elif cell is self.endCell:
					colour = self.endColour

				elif cell in self.path:
					colour = self.pathColour

				elif cell in self.oldPath:
					colour = self.closedSetColour

				elif cell in self.openSet:
					colour = self.openSetColour

				# elif cell in self.closedSet:
				#     colour = self.closedSetColour

				else:
					continue

				self.grid[y][x].draw(self.pygame, screen, colour)

		# self.oldColour = colour

		# coordinates = []
		# for i in self.path:
		#     center = (int(i.x*i.width+i.width/2), int(i.y*i.height+i.height/2))
		#     coordinates.append(center)
		
		# if len(coordinates) > 1:
		#     self.pygame.draw.lines(screen, (0,0,0), False, coordinates, 5)

		self.oldPath = self.path

	#=============================================================================
	def heuristic(self, objA, objB):

		# Manhattan distance. x distance + y distance
		# return abs(objA.x - objB.x) + abs(objA.y - objB.y)

		# euclidean distance. pythagoras.
		return math.hypot(objA.x - objB.x, objA.y - objB.y)
	
	def pause(self):
		self.allowUpdate = True
		self.pygame.FPS = self.pauseFrequency

	def unpause(self):
		self.pygame.FPS = self.updateFrequency
		self.allowUpdate = False

	def isPaused(self):
		return self.allowUpdate
		
	def incrementFrequency(self, increment):
		self.updateFrequency += increment
		self.pygame.FPS = self.updateFrequency

	def getFrequency(self):
		return self.updateFrequency
		
	def setMouseMode(self, _mouseMode):
		self._mouseMode = _mouseMode
		
	#
	def selectWithMouse(self, mouseX, mouseY):

		if not self.isPaused():
			return

		obj = None

		cWidth = self.width / self.size
		cHeight = self.height / self.size

		# keyX = 0
		# keyX = 0

		for y in range(self.size):
			for x in range(self.size):

				x1 = x * cWidth
				y1 = y * cHeight
				x2 = x1 + cWidth
				y2 = y1 + cHeight
				obj = self.grid[y][x]

				if mouseX >= x1 and mouseX < x2:
					if mouseY >= y1 and mouseY < y2:
						
						
						if self._mouseMode == 1:
							obj.wall = True
							
							# ADD 'PAUSE WHEN MOUSEDOWN'
							# ADD 'RESETDATA() IF DRAW'
							# FIX COLOURING FOR BETTER PERFORMANCE
							
							
							# obj.f = 0
							# obj.g = 0
							# obj.h = 0
							
							# self.path = []
							# self.closedSet = []
							# self.openSet = []
							# self.openSet.append(self.startCell)
								
								
						elif self._mouseMode == 3:
							print(obj)
							print("wall:      ", obj.wall)
							print("path:      ", obj in self.path)
							print("openSet:   ", obj in self.openSet)
							print("closedSet: ", obj in self.closedSet)
							# obj.wall = False
