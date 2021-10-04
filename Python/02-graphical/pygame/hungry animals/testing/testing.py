
from random import randint
from os import system as sys

sys("cls")

randX = 0
randY = 0

while randX == 0 and randY == 0:
    randX = randint(-10, 10)
    randY = randint(-10, 10)

print(f"x: {randX:.1f}", f"y: {randY:.1f}")

if randX > randY:
    randY /= randX
    randX /= randX
else:
    randX /= randY
    randY /= randY

print(f"x: {randX:.1f}", f"y: {randY:.1f}")
