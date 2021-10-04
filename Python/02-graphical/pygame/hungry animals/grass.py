
class Grass:

    def __init__(self, grassImage, xPos, yPos):
        self._grassImage = grassImage
        self._xPos = xPos
        self._yPos = yPos
        self._radius = 25

        self._eaten = False

    def getPos(self):
        return [self._xPos + self._radius, self._yPos + self._radius]

    def getRadius(self):
        return self._radius

    def eatenBySheep(self):
        self._eaten = True

    def isEaten(self):
        return self._eaten

    def draw(self, screen):
        screen.blit(self._grassImage, (self._xPos, self._yPos))
