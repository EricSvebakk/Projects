
from math import sqrt

class Wolf:

    def __init__(self, wolfImage, xPos, yPos, sheepList):
        self._wolfImage = wolfImage
        self._xPos = xPos
        self._yPos = yPos
        self._radius = 25

        self._vel = 0.5
        self._xVel = self._vel
        self._yVel = self._vel

        self._sheepList = sheepList

        self._x1Border = None
        self._y1Border = None
        self._x2Border = None
        self._y2Border = None

    def border(self, width, height):
        self._x1Border = 0
        self._y1Border = 0
        self._x2Border = width - 50
        self._y2Border = height - 50

    #=============================================================

    def setPos(self, xPos, yPos):
        self._xPos = xPos
        self._yPos = yPos

    def getPos(self):
        return [self._xPos + self._radius, self._yPos + self._radius]

    def getRadius(self):
        return self._radius

    #=============================================================
    def setVel(self, xVel, yVel):
        self._xVel = xVel
        self._yVel = yVel

    def getxVel(self):
        return self._xVel

    def getyVel(self):
        return self._yVel

    #=============================================================
    def getClosestSheep(self):

        closestSheep = None
        closest = 999

        # if self._sheepList:
        for sheep in self._sheepList:
            sheepPos = sheep.getPos()

            deltaX = self._xPos - sheepPos[0]
            deltaY = self._yPos - sheepPos[1]
            dist = sqrt(deltaX**2 + deltaY**2)

            if dist < closest:
                closest = dist
                closestSheep = sheep

        return closestSheep
    
    def move(self):

        if self.getClosestSheep():

            sheepPos = self.getClosestSheep().getPos()
            if sheepPos[0] < self._xPos:
                self._xVel = -self._vel
            else:
                self._xVel = self._vel

            if sheepPos[1] < self._yPos:
                self._yVel = -self._vel
            else:
                self._yVel = self._vel
        else:
            if self._xPos < self._x1Border or self._xPos > self._x2Border:
                self._xVel *= -1

            if self._yPos < self._y1Border or self._yPos > self._y2Border:
                self._yVel *= -1

        self._xPos += self._xVel
        self._yPos += self._yVel
            
    def turnAround(self):
        self._xVel *= -1
        self._yVel *= -1

    def draw(self, screen):
        screen.blit(self._wolfImage, (self._xPos, self._yPos))
