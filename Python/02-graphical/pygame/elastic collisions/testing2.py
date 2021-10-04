
import math
from random import randint as ri, uniform as ru
from particle import Particle
from gameboard import Gameboard
from math import pi
import pygame

# Background fill colour
backgroundColour = (128, 81, 9)

# Specifies window properties
width = 800
height = 600
pygame.display.set_caption("Elastic Collision")
screen = pygame.display.set_mode((width, height))

# gameboard is a class for creating objects inside the pygame window.
gameboard = Gameboard(pygame, [0, width], [0, height])

# .physicsProperties defines how objects are affected inside the pygame window
gameboard.physicsProperties([pi, 0.002], 0.01, 0.75)

# .generate specifies how many particle objects to create.
gameboard.addParticles(2)

time = 10 * 1000000

# Game loop
running = True
while running:

    # For-loop that tests for specific inputs
    for event in pygame.event.get():

        # Stops program if pygame window is closed
        if event.type == pygame.QUIT:
            running = False

        # Selects a given object if the mouse is clicked and
        # the objects position matches the cursors position
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            gameboard.selectObject(mouseX, mouseY)

        # Deselects any given object if the mouse is no longer clicked
        if event.type == pygame.MOUSEBUTTONUP:
            gameboard.selectedParticle = None

    # Draws the background
    screen.fill(backgroundColour)

    # Updates and draws all particle objects
    gameboard.update()
    gameboard.display(screen)

    # Updates screen with current content
    pygame.display.flip()

    time -= 1
    if time < 0:
        running = False

total = 0
for i in gameboard.particleList:
    total += i.maxSpeed

print(total)


class Gameboard:

    def __init__(self, pygame, xRange, yRange):

        # Allows pygame to be used for drawing objects
        self.pygame = pygame

        # Gameboard boundaries
        self.xRange = xRange
        self.yRange = yRange

        # Variables for handling objects
        self.objectList = []
        self.selectedObject = None

        # Physics properties
        self.gravityVector = 0
        self.airResistance = 0
        self.elasticity = 0

    #
    def physicsProperties(self, gravityVector=False, airResistance=0, elasticity=0):
        self.gravityVector = gravityVector
        self.airResistance = airResistance
        self.elasticity = elasticity

    # Generates n random objects when method is called.
    def addParticles(self, numObjects, **kwargs):
        edge = 50
        for _ in range(numObjects):

            xP = kwargs.get(
                "xP", ri(self.xRange[0]+edge, self.xRange[1]-edge))  # x-position
            yP = kwargs.get(
                "yP", ri(self.yRange[0]+edge, self.yRange[1]-edge))  # y-position
            # xV = kwargs.get("xV", 1)
            # yV = kwargs.get("yV", 1)
            # speed
            v = kwargs.get("velocity", 1)
            # radius
            r = kwargs.get("radius", 20)
            a = kwargs.get("angle", ru(0, math.pi*2)
                           )                           # angle
            # density
            d = kwargs.get("density", ri(1, 20))
            e = kwargs.get("elasticity", 1)

            particle = Particle(xP, yP, v, r, a, d, e, self)
            self.objectList.append(particle)

    #
    def update(self):
        for i, obj1 in enumerate(self.objectList):

            if self.gravityVector:
                vector = (obj1.angle, obj1.speed)
                (obj1.angle, obj1.speed) = self.addVectors(
                    *vector, *self.gravityVector)

            obj1.move(self.airResistance)
            self.checkBoundary(obj1)

            for obj2 in self.objectList[i+1:]:
                obj1.checkCollision(obj2)

            if self.selectedObject:
                (mouseX, mouseY) = self.pygame.mouse.get_pos()
                self.selectedObject.moveTo(mouseX, mouseY)

    #
    def display(self, screen):
        for obj in self.objectList:
            obj.display(screen)

    #
    def selectObject(self, mouseX, mouseY):
        for obj in self.objectList:
            if math.hypot(obj.xPos-mouseX, obj.yPos-mouseY) <= obj.radius:
                self.selectedObject = obj

    #
    def addVectors(self, angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)

    #
    def checkBoundary(self, obj):

        if obj.xPos + obj.radius > self.xRange[1]:
            obj.xPos = 2*(self.xRange[1] - obj.radius) - obj.xPos
            obj.angle = -obj.angle
            # obj.xVel *= self.elasticity
            obj.speed *= self.elasticity

        elif obj.xPos - obj.radius < self.xRange[0]:
            obj.xPos = 2*obj.radius - obj.xPos
            obj.angle = -obj.angle
            # obj.xVel *= self.elasticity
            obj.speed *= self.elasticity

        if obj.yPos + obj.radius > self.yRange[1]:
            obj.yPos = 2*(self.yRange[1] - obj.radius) - obj.yPos
            obj.angle = math.pi - obj.angle
            # obj.yVel *= self.elasticity
            obj.speed *= self.elasticity

        elif obj.yPos - obj.radius < self.yRange[0]:
            obj.yPos = 2*obj.radius - obj.yPos
            obj.angle = math.pi - obj.angle
            # obj.yVel *= self.elasticity
            obj.speed *= self.elasticity


class Particle:

    #
    def __init__(self, xP, yP, s, r, a, d, e, gameboard):

        self.gameboard = gameboard
        self.drawCircle = self.gameboard.pygame.draw.circle

        self.xPos = xP
        self.yPos = yP
        # self.xVel = xV
        # self.yVel = yV
        self.speed = s

        self.radius = r
        self.angle = a
        self.mass = d * self.radius ** 2
        self.elasticity = e

        self.colour = (200-d*10, 200-d*10, 255)
        self.borderThickness = 1

        #self.maxSpeed = abs(xV + yV)

    #
    def display(self, screen):
        x = int(self.xPos)
        y = int(self.yPos)
        self.drawCircle(screen, self.colour, (x, y), self.radius-1)
        self.drawCircle(screen, (0, 0, 0), (x, y),
                        self.radius, self.borderThickness)

    # Calculated the particles position
    def move(self, airResistance):

        drag = (self.mass/(self.mass + airResistance)) ** self.radius
        # self.xVel *= drag
        # self.yVel *= drag
        # self.xPos += math.sin(self.angle) * self.xVel
        # self.yPos -= math.cos(self.angle) * self.yVel

        self.speed *= drag
        self.xPos += math.sin(self.angle) * self.speed
        self.yPos -= math.cos(self.angle) * self.speed

        # totVel = abs(self.xVel + self.yVel)
        # if totVel > self.maxSpeed:
        #     self.maxSpeed = totVel

    def moveTo(self, xPos, yPos):
        dx = xPos - self.xPos
        dy = yPos - self.yPos
        self.angle = math.atan2(dy, dx) + (math.pi/2)
        self.speed = math.hypot(dx, dy) * 0.05
        # self.xVel = dx * 0.9
        # self.yVel = dy * 0.9

    #
    def checkCollision(self, obj):

        # Calculates the distance between obj1 and obj2
        dx = self.xPos - obj.xPos
        dy = self.yPos - obj.yPos
        dist = math.hypot(dx, dy)

        # If obj1 and obj have collided then...
        if dist < self.radius + obj.radius:

            obj1test1 = self.speed
            obj2test1 = obj.speed

            angle = math.atan2(dy, dx) + 0.5 * math.pi
            massTotal = self.mass + obj.mass

            # a vector (tuple containing angle and speed) perpendiular to
            # obj1's vector is added, whose magnitude is based on it's momentum
            # (mass * velocity)
            vector1 = (self.angle, self.speed*(self.mass-obj.mass)/massTotal)
            vector2 = (angle, 2*obj.speed*obj.mass/massTotal)
            (self.angle, self.speed) = self.gameboard.addVectors(*vector1, *vector2)

            # Same as above but for obj2's vector
            vector1 = (obj.angle, obj.speed*(obj.mass-self.mass)/massTotal)
            vector2 = (angle+math.pi, 2*self.speed*self.mass/massTotal)
            (obj.angle, obj.speed) = self.gameboard.addVectors(*vector1, *vector2)

            # Each collision between obj1 and obj1 contributes to slow down
            # both objects based on their elasticity
            elasticity = self.elasticity * obj.elasticity
            self.speed *= elasticity
            obj.speed *= elasticity

            # Calculates how much obj1 and obj2 are overlapping
            # to adjust their position accordingly
            overlap = 0.1 * (self.radius + obj.radius - dist + 1)

            # Each position is recalculated to account for overlap
            self.xPos += math.sin(angle) * overlap
            self.yPos -= math.cos(angle) * overlap
            obj.xPos -= math.sin(angle) * overlap
            obj.yPos += math.cos(angle) * overlap

            obj1test3 = self.speed
            obj2test3 = obj.speed

            print(
                round(obj1test1+obj2test1, 2),
                round(obj1test3+obj2test3, 2)
            )