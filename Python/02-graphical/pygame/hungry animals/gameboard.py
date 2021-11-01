
from sheep import Sheep
from grass import Grass
from stone import Stone
from wolf import Wolf
from math import sqrt

class Gameboard:

    def __init__(self, boardWidth, boardHeight):
        self._sheepList = []
        self._grassList = []
        self._stoneList = []
        self._wolfList = []
        self._width = boardWidth
        self._height = boardHeight

    def createGrass(self, image, xPos, yPos):
        self._grassList.append(Grass(image, xPos, yPos))

    def createStone(self, image, xPos, yPos):
        self._stoneList.append(Stone(image, xPos, yPos))

    def createSheep(self, image, xPos, yPos):
        sheep = Sheep(image, xPos, yPos)
        sheep.border(self._width, self._height)
        self._sheepList.append(sheep)
        return sheep

    def createWolf(self, image, xPos, yPos):
        wolf = Wolf(image, xPos, yPos, self._sheepList)
        wolf.border(self._width, self._height)
        self._wolfList.append(wolf)
        return wolf

    def update(self):
        for sheep in self._sheepList:
            sheep.move()
            for grass in self._grassList:
                if self._checkCollision(sheep, grass):
                    grass.eatenBySheep()
            for stone in self._stoneList:
                if self._checkCollision(sheep, stone):
                    sheep.turnAround()

        for wolf in self._wolfList:
            wolf.move()
            for sheep in self._sheepList:
                if self._checkCollision(wolf, sheep):
                    sheep.eatenByWolf()

    def draw(self, screen):
        #
        for sheep in self._sheepList:
            if sheep.isEaten():
                self._sheepList.remove(sheep)
            else:
                sheep.draw(screen)

        #        
        for grass in self._grassList:
            if grass.isEaten():
                self._grassList.remove(grass)
            else:
                grass.draw(screen)

        #
        for stone in self._stoneList:
            stone.draw(screen)

        #
        for wolf in self._wolfList:
            wolf.draw(screen)

    #
    def _checkCollision(self, obj1, obj2):

        obj1Pos = obj1.getPos()
        obj2Pos = obj2.getPos()
        deltaX = obj1Pos[0] - obj2Pos[0]
        deltaY = obj1Pos[1] - obj2Pos[1]
        dist = sqrt(deltaX**2 + deltaY**2)

        if dist < obj1.getRadius() + obj2.getRadius():
            return True
        return False

    # obj1Pos = {
    #     "x": [obj1.getPos()[0],obj1.getPos()[0] + 50],
    #     "y": [obj1.getPos()[1],obj1.getPos()[1] + 50]
    # }

    # obj2Pos = {
    #     "x": [obj2.getPos()[0],obj2.getPos()[0] + 50],
    #     "y": [obj2.getPos()[1],obj2.getPos()[1] + 50]
    # }

    # for i in range(2):
    #     for j in ["x", "y"]:

    #         exp = eval(f"obj1Pos['{j}'][{i}] > obj2Pos['{j}'][{-i+1}]")
    #         exp1 = f"obj1Pos['{j}'][{i}]"
    #         exp2 = f"obj2Pos['{j}'][{-i+1}]"

    #         o1 = f"s{j}{i+1}"
    #         o2 = f"w{j}{-i+1+1}"

    #         if eval(f"obj1Pos['{j}'][{i}] > obj2Pos['{j}'][{-i+1}]"):
    #             print(o1, o2, f"{eval(exp1):>3}", ">", f"{eval(exp2):>3}", exp)
    #         else:
    #             print(o1, o2, f"{eval(exp1):>3}", "<", f"{eval(exp2):>3}", exp)

