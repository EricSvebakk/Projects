
class Stone:

    def __init__(self, stoneImage, xPos, yPos):
        self._stoneImage = stoneImage
        self._xPos = xPos
        self._yPos = yPos
        self._radius = 25
        self._immobile = True

    def getPos(self):
        return [self._xPos + self._radius, self._yPos + self._radius]

    def getRadius(self):
        return self._radius

    def immobile(self):
        return self._immobile

    def draw(self, screen):
        screen.blit(self._stoneImage, (self._xPos, self._yPos))
