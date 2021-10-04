
from sheep import Sheep

def sheep_test():

    sheep = Sheep("sheep", 50, 50)

    sheep.setPos(0, 0)
    sheep.setVel(10, 20)
    sheep.move()
    sheep.move()
    print(sheep.getPos())
    sheep.turnAround()
    sheep.move()
    print(sheep.getPos())

sheep_test()
