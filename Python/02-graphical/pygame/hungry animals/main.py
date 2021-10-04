
from gameboard import Gameboard
from random import randint

#
WIDTH = 800
HEIGHT = 600
gameboard = Gameboard(WIDTH, HEIGHT)

#
border = 50

#
objects = {
    "sheep": 2,
    "grass": 15,
    "stone": 5,
    "wolf": 1
}

#
for myObj in objects:
    for _ in range(objects[myObj]):
        randW = randint(border, WIDTH-border-50)
        randH = randint(border, HEIGHT-border-50)
        eval(f"gameboard.create{myObj.capitalize()}('{myObj}',{randW},{randH})")


def draw():
    screen.fill((128, 81, 9))    
    gameboard.draw(screen)

#
def update():
    gameboard.update()
