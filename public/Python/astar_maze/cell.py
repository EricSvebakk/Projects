
from random import randint

class Cell:

    def __init__(self,x,y,width,height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.f = 0
        self.g = 0
        self.h = 0
        
        self.wall = False

        self.neighbours = None
        self.previous = None
        

    def __repr__(self):
        return f"({self.x}:{self.y})"

    #=============================================================================
    def draw(self, pygame, screen, colour1, colour2 = (0,0,0)):

        rect = (self.x*self.width, self.y*self.height, self.width, self.height)
        pygame.draw.rect(screen, colour1, rect)
        # pygame.draw.rect(screen, colour2, rect, 1)

        # center = (int(self.x*self.width+self.width/2), int(self.y*self.height+self.height/2))
        # pygame.draw.circle(screen, colour1, center, 4)

    #=============================================================================
    def findNeighbours(self, board: list, size: int) -> list:

        neighbours = []

        for i in range(-1, 2):

            yi = i + self.y

            if yi < 0 or yi > size-1:
                continue

            for j in range(-1, 2):

                xj = j + self.x

                if xj < 0 or xj > size-1:
                    continue

                if yi == self.y and xj == self.x:
                    continue

                else:
                    neighbours.append(board[int(yi)][int(xj)])

        self.neighbours = neighbours

