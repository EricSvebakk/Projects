
import math

class Particle:

    #
    def __init__(self, xPos, yPos, speed, radius, angle, density, elasticity, gameboard):
        
        self.gameboard = gameboard
        self.drawCircle = self.gameboard.pygame.draw.circle
        
        self.xPos = xPos
        self.yPos = yPos
        # self.xVel = xV
        # self.yVel = yV
        self.speed = speed

        self.radius = radius
        self.angle = angle
        self.mass = density * self.radius ** 2
        self.elasticity = elasticity

        self.colour = (200-density*10, 200-density*10, 255)
        self.borderThickness = 1

        #self.maxSpeed = abs(xV + yV)

    #
    def display(self, screen):
        x = int(self.xPos)
        y = int(self.yPos)
        self.drawCircle(screen, self.colour, (x, y), self.radius-1)
        self.drawCircle(screen, (0, 0, 0), (x, y), self.radius, self.borderThickness)

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

            # print(
            #     round(obj1test1+obj2test1, 2),
            #     round(obj1test3+obj2test3, 2)
            #     )
        

    # def _translate(self, angle, a, b):
    #     sin = math.sin(angle)
    #     cos = math.cos(angle)
    #     x = a * cos + b * sin
    #     y = b * cos - a * sin
    #     return {"x": x, "y": y}

    # def checkCollision(self, obj2):

    #     dx = self.xPos - obj2.xPos
    #     dy = self.yPos - obj2.yPos
    #     dist = math.hypot(dx, dy)

    #     if dist < self.radius + obj2.radius:

    #         angle = math.atan2(dy, dx)

    #         aPos = {"x": 0, "y": 0}
    #         bPos = self._translate(angle, dx, dy)
    #         aVel = self._translate(angle, obj2.xVel, obj2.yVel)
    #         bVel = self._translate(angle, self.xVel, self.yVel)

    #         xVelTotal = aVel["x"] - bVel["x"]

    #         x1Vel = (self.xVel * (self.mass - obj2.mass) + (2 * obj2.mass * obj2.xVel)) / (self.mass + obj2.mass)
    #         y1Vel = (self.yVel * (self.mass - obj2.mass) + (2 * obj2.mass * obj2.yVel)) / (self.mass + obj2.mass)
    #         x2Vel = (obj2.xVel * (obj2.mass - self.mass) + (2 * self.mass * self.xVel)) / (self.mass + obj2.mass)
    #         y2Vel = (obj2.yVel * (obj2.mass - self.mass) + (2 * self.mass * self.yVel)) / (self.mass + obj2.mass)

    #         aVel["x"] = (aVel["x"] * (self.mass - obj2.mass) + (2 * obj2.mass * bVel["x"])) / (self.mass + obj2.mass)
    #         bVel["x"] = xVelTotal + aVel["x"]

    #         aPos["x"] += aVel["x"]
    #         bPos["x"] += bVel["x"]

    #         posAf = self._translate(angle, *aPos)
    #         posBf = self._translate(angle, *bPos)
    #         velAf = self._translate(angle, *aVel)
    #         velBf = self._translate(angle, *bVel)

    #         self.xPos += x1Vel
    #         self.yPos += y1Vel
    #         obj2.xPos += x2Vel
    #         obj2.yPos += y2Vel

    #         self.xVel = velBf["x"]
    #         self.yVel = velBf["y"]
    #         obj2.xVel = velAf["x"]
    #         obj2.yVel = velAf["y"]

    #         # print(
    #         #     round(obj1test1+obj2test1,2),
    #         #     round(obj1test2+obj2test2,2),
    #         #     round(obj1test3+obj2test3,2)
    #         #     )
