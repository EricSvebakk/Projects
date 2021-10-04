
from gameboard import checkCollision
from sheep import Sheep
from wolf import Wolf

def checkCollision_test():

    sheep = Sheep("sheep", 100, 100)
    wolf = Wolf("wolf", 150, 150, [sheep])

    checkCollision(sheep, wolf)



checkCollision_test()