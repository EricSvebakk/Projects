
from random import randint

class Sheep:
    def __init__(self, sheepImage, xPos, yPos):
        self._sheepImage = sheepImage
        self._xPos = xPos
        self._yPos = yPos
        self._radius = 25

        self._vel = 2
        self._xVel = self._vel
        self._yVel = self._vel

        self._x1Border = None
        self._y1Border = None
        self._x2Border = None
        self._y2Border = None

        self._eaten = False

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
    def eatenByWolf(self):
        self._eaten = True

    def isEaten(self):
        return self._eaten

    #=============================================================
    def move(self):

        if self._xPos < self._x1Border or self._xPos > self._x2Border:
            self._xVel *= -1
        
        if self._yPos < self._y1Border or self._yPos > self._y2Border:
            self._yVel *= -1

        if randint(1, 100) == 1:
            randX = float(randint(1,100))
            randY = float(randint(1,100))
            
            if randX > randY:
                randY /= randX
                randX /= randX
            else:
                randX /= randY
                randY /= randY

            if randint(0, 1):
                randX *= -1
            else:
                randY *= -1

            self._xVel = randX * self._vel
            self._yVel = randY * self._vel
        
        self._xPos += self._xVel
        self._yPos += self._yVel
    
    def turnAround(self):
        self._xVel *= -1
        self._yVel *= -1

    def draw(self, screen):
        screen.blit(self._sheepImage, (self._xPos, self._yPos))

    #=============================================================
