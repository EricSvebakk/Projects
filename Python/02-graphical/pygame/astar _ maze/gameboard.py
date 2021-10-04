
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
        self.backgroundCellColour = (255, 255, 255)
        self.pathCellColour = (0, 0, 0)
        self.startCellColour = (0, 255, 0)
        self.closedCellColour = (255, 0, 0)
        self.openCellColour = (100, 200, 100)
        self.wallCellColour = (100, 100, 100)

        # 
        self.closedSet = []
        self.openSet = []
        
        # 
        self.path = []
        self.oldPath = []

        # 
        self.grid = []
        self.generate(start, end)

    #=============================================================================
    def generate(self, start, end):
        
        self.startPos = start
        self.endPos = end

        self.openSet = []
        self.closedSet = []
        self.path = []
        self.oldPath = []
        self.grid = []

        # Cell generation code
        for y in range(self.size):
            self.grid.append([])
            for x in range(self.size):
                            
                cell = Cell(int(x), int(y), self.cWidth, self.cHeight)

                if randint(0, int(100/self.wallChance)-1) == 0:
                    cell.wall = True
                else:
                    cell.wall = False

                self.grid[y].append(cell)

        # Update each cell with their corresponding neighbours
        for y in range(self.size):
            for x in range(self.size):
                
                cell = self.grid[y][x]
                cell.findNeighbours(self.grid, self.size)

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

        # Sets self.start to the corresponding cell for the given grid-coordinates
        self.startCell = self.grid[start[1]][start[0]]
        self.startCell.wall = False
        
        # start cell is first cell to be checked in the open-set
        self.openSet.append(self.startCell)

        # Sets self.end to the corresponding cell for the given grid-coordinates
        self.endCell = self.grid[end[1]][end[0]]
        self.endCell.wall = False

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
    def drawAll(self, screen):

        colour = None

        for y in range(self.size):
            for x in range(self.size):

                cell = self.grid[y][x]

                if cell.wall:
                    colour = self.wallCellColour
                else:
                    colour = self.backgroundCellColour

                self.grid[y][x].draw(self.pygame, screen, colour)

    #=============================================================================
    def draw(self, screen):

        colour = None

        for y in range(self.size):            
            for x in range(self.size):
                
                cell = self.grid[y][x]

                if cell is self.startCell or cell is self.endCell:
                    colour = self.startCellColour

                elif cell in self.path:
                    colour = self.pathCellColour

                elif cell in self.oldPath:
                    colour = self.closedCellColour

                # elif cell in self.closedSet:
                #     colour = (255, 0, 0)

                elif cell in self.openSet:
                    colour = self.openCellColour

                else:
                    continue

                self.grid[y][x].draw(self.pygame, screen, colour)

        self.oldColour = colour

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
