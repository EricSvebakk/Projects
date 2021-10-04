
import pygame as pygame_DIAGNOSTIC
import os as os_DIAGNOSTIC


class Container:
    
    def __init__(self, pygame, xPos, yPos, colour=(0,100,100)):
        self.pygame = pygame
        self.xPos = int(xPos)
        self.yPos = int(yPos)
        self.colour1 = colour
        self.colour2 = (0, 0, 0)
        self.border = None
        self.text = None
        self.rect = None

    #===================================================================
    def __repr__(self):
        return f"{self.xPos}:{self.yPos}"

    #===================================================================
    def draw(self, screen):

        if self.rect:
            self.pygame.draw.rect(screen, self.colour1, self.rect)
            
            if self.border:
                self.pygame.draw.rect(screen, self.colour2, self.rect, self.border)

        if self.text:
            screen.blit(*self.text)

    #===================================================================
    def addBox(self, width, height, border=1):
        surface = self.pygame.Surface([int(width), int(height)])
        self.border = border
        self.rect = surface.get_rect()
        self.rect.center = (self.xPos, self.yPos)

    #===================================================================
    def addText(self, text, fontType="consolas", fontSize=16):
        font = self.pygame.font.SysFont(fontType, fontSize)
        surface = font.render(text, True, self.colour2)
        rect = surface.get_rect()
        rect.center = (self.xPos, self.yPos)
        self.text = (surface, rect)
            
#===================================================================
class Diagnostic:
    
    def __init__(self, width=600, height=600, bgColour=(255,255,255)):

        self.width = width
        self.height = height
        self.bgColour = bgColour

        self.pygame = pygame_DIAGNOSTIC
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((self.width, self.height),self.pygame.RESIZABLE)
        self.pygame.display.set_caption("Diagnostic")
        
        self.directory = None
        self.tree = []

        self.previousRect = None
        self.previousColour = None

        self.drawList = []
        self.getDirectory()
        self.setContainers()
        self.gameloop()

    #===================================================================
    def getDirectory(self):

        self.directory = {}
        imports = []

        for item in os_DIAGNOSTIC.listdir():
            if __file__ not in item and ".py" in item:
                
                fileContent = __import__(item.strip(".py"))
                imports.append((item, fileContent))

        fi = 0
        for (fileName, fileContent) in imports:
            fi += 1

            self.directory[f"{fi}000"] = [fileName, True, None]

            ri = 0
            for (refName, refContent) in vars(fileContent).items():
                if "__" not in refName:
                    ri += 1

                    self.directory[f"{fi}{ri}00"] = [refName, False, None]
                    self.directory[f"{fi}{ri}10"] = ["Type", False, None]
                    self.directory[f"{fi}{ri}11"] = [type(refContent), False, None]
                    self.directory[f"{fi}{ri}20"] = ["Value", False, None]
                    self.directory[f"{fi}{ri}21"] = [refContent, False, None]

                    if type(refContent) == type:
                        self.directory[f"{fi}{ri}30"] = ["Methods", False, None]
                        
                        mi = 0
                        for methodName in dir(refContent):
                            if "__" not in methodName:
                                mi += 1

                                self.directory[f"{fi}{ri}3{mi}"] = [f"{methodName}()", False, None]

    #===================================================================
    def setContainers(self):

        ratio = [1,1,1,2]
        
        smallest = min(ratio)

        for i in range(len(ratio)):
            ratio[i] = int(ratio[i]/smallest)
        
        uw = self.width/sum(ratio)
        uh = self.height/12

        (x, w, h) = ([], [], [])

        for i in range(4):
            x.append(uw * sum(ratio[:i]) + (uw * ratio[i])/2)
            w.append((uw * ratio[i]) - 10)
            h.append(0)

        xPos = 0
        yPos = 0
        width = None
        height = uh

        for (key, val) in self.directory.items():

            index = 3 - key.count("0")
            
            h[index] += uh
            yPos = h[index]
            xPos = x[index]
            width = w[index]
            
            for i in range(4):
                if i > index:
                    h[i] = 0

            colour = (0, 150, 50 + index * 50)
            container = Container(self.pygame, xPos, yPos, colour)
            container.addBox(width, height, 1)
            container.addText(str(val[0]), "consolas", 12)
            val[2] = container
            
    #===================================================================
    def draw(self):

        self.screen.fill(self.bgColour)

        for obj in self.directory.values():
            if obj[1]:
                obj[2].draw(self.screen)


        # for i in range(24):
        #     i *= (600/24)
        #     i = int(i)
        #     self.pygame.draw.line(self.screen, (0,0,0), (i, 0), (i, self.height))
        #     self.pygame.draw.line(self.screen, (0,0,0), (0, i), (self.width, i))

        self.pygame.display.update()

    #===================================================================
    def selectWithMouse(self, xPos:int, yPos):

        if self.previousRect:
            self.previousRect.colour2 = self.previousColour

        for (key, val) in self.directory.items():

            if val[2].rect.collidepoint(xPos, yPos) and val[1]:
                    
                self.showTree(key)

                self.previousRect = val[2]
                self.previousColour = val[2].colour2
                val[2].colour2 = (255, 255, 255)

    #===================================================================
    def showTree(self, keyA):
        
        nz = 4 - keyA.count("0")
        nzA = keyA.count("0") - 1

        for (keyB, valB) in self.directory.items():
            
            nzB = keyB.count("0")

            if valB[1]:
                if (nzA >= nzB):
                    valB[1] = False

            else:
                if (keyA[:nz] == keyB[:nz] and nzA == nzB):
                    valB[1] = True

    #===================================================================
    def gameloop(self):

        self.screen.fill(self.bgColour)
        self.pygame.display.update()

        xPos = 0
        yPos = 0

        running = True
        while running:

            for event in self.pygame.event.get():

                if event.type == self.pygame.QUIT:
                    running = False

                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    (xPos, yPos) = self.pygame.mouse.get_pos()
                    self.selectWithMouse(xPos, yPos)

                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_q:
                        running = False
                    
                    elif event.key == self.pygame.K_i:
                        for i, j in self.directory.items():
                            print(f"{i}: {{ {str(j[0]):<20} {j[1]} {j[2]} }}")

                    elif event.key == self.pygame.K_c:
                        os_DIAGNOSTIC.system("cls")

            self.draw()


Diagnostic(600, 600)


# screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
# background = pygame.image.load(background_image_filename).convert()

# while True:

#     event = pygame.event.wait()

#     if event.type == VIDEORESIZE:
#         SCREEN_SIZE = event.size
#         screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
#         pygame.display.set_caption("Window resized to "+str(event.size))

#     screen_width, screen_height = SCREEN_SIZE

#     for y in range(0, screen_height, background.get_height()):
#         for x in range(0, screen_width, background.get_width()):
#             screen.blit(background, (x, y))

#     pygame.display.update()


# def check(var):

#     print(vars(var), "\n")

#     for i in vars(var):
#         print(i, vars(var)[i])

#     print("\n")

#     for i in dir(var):
#         if "__" not in i:
#             print(i)


# while (command_DIAG := input("\n> ")) != "exit":
    
#     if command_DIAG == "clear":
#         os_DIAGNOSTIC.system("cls")

#     elif command_DIAG == "dir":
#         print()

#     else:
#         exec(command_DIAG)

