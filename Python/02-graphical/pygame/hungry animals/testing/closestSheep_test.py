
from gameboard import Gameboard
from random import randint


def closesSheep_test():
    gameboard = Gameboard(800, 800)
    gameboard.createSheep("sheep", 0, 0)
    gameboard.createSheep("sheep", 179, 160)
    wolf = gameboard.createWolf("wolf", 90, 80)

    closestSheep = wolf.getClosestSheep()

    print(closestSheep.getPos())

closesSheep_test()
