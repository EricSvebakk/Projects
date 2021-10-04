
from particle import Particle
from random import randint as ri, uniform as ru
import math

class Gameboard:

    def __init__(self, pygame, xRange, yRange):
        
        # Allows pygame to be used for drawing objects
        self.pygame = pygame

        # Gameboard boundaries
        self.xRange = xRange
        self.yRange = yRange

        # Variables for handling objects
        self.particleList = []
        self.selectedParticle = None

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

            xP = kwargs.get("xP", ri(self.xRange[0]+edge, self.xRange[1]-edge)) # x-position
            yP = kwargs.get("yP", ri(self.yRange[0]+edge, self.yRange[1]-edge)) # y-position
            # xV = kwargs.get("xV", 1)
            # yV = kwargs.get("yV", 1)
            v = kwargs.get("velocity", 0)                                       # speed
            r = kwargs.get("radius", 20)                                        # radius
            a = kwargs.get("angle", ru(0, math.pi*2))                           # angle
            d = kwargs.get("density", 10)                                       # density
            e = kwargs.get("elasticity", 1)

            particle = Particle(xP, yP, v, r, a, d, e, self)
            self.particleList.append(particle)

    #
    def update(self):
        
        preParticleVelocityTotal = 0
        postParticleVelocityTotal = 0
        
        for i, obj1 in enumerate(self.particleList):
            
            preParticleVelocityTotal += obj1.speed
            
            if self.gravityVector:
                vector = (obj1.angle, obj1.speed)
                (obj1.angle, obj1.speed) = self.addVectors(*vector, *self.gravityVector)

            obj1.move(self.airResistance)
            self.checkBoundary(obj1)

            for obj2 in self.particleList[i+1:]:
                obj1.checkCollision(obj2)

            if self.selectedParticle:
                (mouseX, mouseY) = self.pygame.mouse.get_pos()
                self.selectedParticle.moveTo(mouseX, mouseY)
                
            postParticleVelocityTotal += obj1.speed
        
        print(round(preParticleVelocityTotal, 2), round(postParticleVelocityTotal, 2))

    #
    def display(self, screen):
        for obj in self.particleList:
            obj.display(screen)

    #
    def selectObject(self, mouseX, mouseY):
        for obj in self.particleList:
            if math.hypot(obj.xPos-mouseX, obj.yPos-mouseY) <= obj.radius:
                self.selectedParticle = obj

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

