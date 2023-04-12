

class Cell:

    def __init__(self, pygame):
        self._draw = pygame.draw.rect
        
        self._alive = False
        self._unlocked = True

    #================================================
    def alive(self):
        if self._unlocked:
            self._alive = True

    def dead(self):
        if self._unlocked:
            self._alive = False

    #================================================
    def lock(self):
        self._unlocked = False

    def unlock(self):
        self._unlocked = True

    #================================================
    def isAlive(self):
        return self._alive

    def isUnlocked(self):
        return self._unlocked

    #================================================
    def draw(self, x, y, w, h, colour, screen, border=False):

        if border:
            self._draw(screen, colour, (x, y, w, h))
        else:
            if self.isUnlocked():
                    if self.isAlive():
                        fill = (255, 255, 255)
                    else:
                        fill = (50, 50, 50)
            else:
                fill = (0, 0, 0)

            self._draw(screen, fill, (x, y, w, h))
            self._draw(screen, colour, (x, y, w, h), 1)
