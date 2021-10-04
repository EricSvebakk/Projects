
import pygame as pygame_DIAG
import os as os_DIAG


class Container:
    
    def __init__(self, pygame, xPos, yPos, colour1, colour2=(0,0,0)):
        self.pygame = pygame
        self.xPos = xPos
        self.yPos = yPos
        self.colour1 = colour1
        self.colour2 = colour2
        self.boxes = []
        self.pText = None
        self.cText = None

    #===================================================================
    def addBox(self, width, height, borderWidth=0):
        inner = self.pygame.Surface([width, height])
        outer = inner.get_rect()
        outer.center = (self.xPos, self.yPos)
        if borderWidth:
            self.boxes.append([self.colour2, outer, borderWidth])
        else:
            self.boxes.append([self.colour1, outer])

    #===================================================================
    def addText(self, text, fontType="consolas", fontSize=16):
        font = self.pygame.font.SysFont(fontType, fontSize)
        inner = font.render(text, True, self.colour2)
        outer = inner.get_rect()
        outer.center = (self.xPos, self.yPos)
        self.pText = text
        self.cText = (inner, outer)
            
#===================================================================
class Diagnostic:
    
    def __init__(self, pygame, width=600, height=600, bgColour = (255,255,255)):
        
        self.pygame = pygame

        self.width = width
        self.height = height
        self.bgColour = bgColour

        self.pygame.init()
        self.screen = self.pygame.display.set_mode((self.width, self.height))
        self.pygame.display.set_caption("Diagnostic")
        
        self.dirImport = None
        self.directory = None


        self.drawList = []
        self.getDirectory()
        #self.updateContainer(["Show Directory"], self.directory, 120, 50)
        # self.update(["test1", "test2"], self.drawList, 50, 50)
        # self.gameloop()

    #===================================================================
    def getDirectory(self):

        self.dirImport = []
        dirList = []

        for item in os_DIAG.listdir():
            if __file__ not in item and ".py" in item:
                dirList.append(item)

        for fileName in dirList:
            fileName = fileName.strip(".py")
            fileContent = __import__(fileName)
            self.dirImport.append((fileName, fileContent))

        self.directory = {}

        for (fileName, fileContent) in self.dirImport:

            self.directory[fileName] = {}

            for (refName, refContent) in vars(fileContent).items():

                if "__" not in refName:

                    self.directory[fileName][refName] = {}
                    self.directory[fileName][refName]["type"] = type(refContent)
                    self.directory[fileName][refName]["value"] = refContent

                    if type(refContent) == type:

                        self.directory[fileName][refName]["methods"] = []

                        for methodName in dir(refContent):

                            if "__" not in methodName:
                                self.directory[fileName][refName]["methods"].append(
                                    methodName)

        # def nestedTruth(dict1):

        #     def recursion(dict2):

        #         for (key, val) in dict2.items():

        #             if type(val) == dict:
        #                 recursion(val)

        #             else:
                        

        #     recursion(dict1)

        # nestedTruth(self.directory)


        def nestedDict(dict1):

            def recursion(dict2):
                
                pad = 12
                for (key, val) in dict2.items():

                    if type(val) == dict:
                        print()
                        print(f"{'Variable:':<{pad}}{key}")
                        recursion(val)

                    elif type(val) == list:
                        for index in val:
                            print(f"{'':<{pad}}{index}()")

                    else:
                        print(f"{(key+':'):<{pad}}{val}")

            recursion(dict1)

        nestedDict(self.directory)


        # print("\n\n")

        # for file in self.directory:
        #     print(file, ".py", sep="")

        #     for variable in self.directory[file]:
        #         print("*", variable)

        #         for attribute in self.directory[file][variable]:
        #             if attribute != "methods":
        #                 print("**", attribute, ":",
        #                       self.directory[file][variable][attribute])
        #             else:

        #                 print("**", attribute)
        #                 for method in self.directory[file][variable][attribute]:
        #                     print("*** ", method, "()", sep="")

        #         print()

        #     print()

    #===================================================================
    def draw(self):

        self.screen.fill(self.bgColour)

        for key in self.drawList:
            for objectList in key:
                for obj in objectList.boxes:

                    self.pygame.draw.rect(self.screen, *obj)

                self.screen.blit(*objectList.cText)

        self.pygame.display.update()

    #===================================================================
    def update(self, objects, objList, xPos, yPos):
        
        mColour = (0, 100, 100)
        bgColour = (0, 0, 0)
        step = 50

        for item in objects:
            
            container = Container(self.pygame, xPos, yPos, mColour, bgColour)

            container.addBox(120, step-1)
            container.addBox(120, step-1, 1)
            container.addText(item)

            objList.append(container)

        # if selected:
        #     newDir = dir(self.dirImport["value"][selected])

        #     self.updateContainer(self.importName, self.directory["outerContent"], 80, 50)

        #     self.updateContainer(newDir, self.directory["innerContent"], 250, 50)

    #===================================================================
    def updateContainer(self, objects, containerList, xPos, yPos):

        for _ in range(len(containerList)):
            del containerList[0]

        mColour = (0, 100, 100)
        bgColour = (0, 0, 0)
        step = 50

        for item in objects:

            if "__" in item:
                continue

            container = Container(self.pygame, xPos, yPos, mColour, bgColour)

            container.addBox(120, step-1)
            container.addBox(120, step-1, 1)
            container.addText(item)

            containerList.append(container)

            yPos += step

    #===================================================================
    def selectWithMouse(self, xPos:int, yPos):

        print(xPos)

        print(self)

        for key in self.directory:
            for (index, objects) in enumerate(self.directory[key]):
    
                if objects.boxes[0][1].collidepoint(xPos, yPos):
                    
                    print(xPos, yPos)
                    return index

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
                    self.update(self.selectWithMouse(xPos, yPos))

                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_q:
                        running = False
                    
                    elif event.key == self.pygame.K_i:
                        for key in self.directory:
                            print(f"{key}: {self.directory[key]}")

                    elif event.key == self.pygame.K_o:
                        for key in self.dirImport:
                            print(f"{key}: {self.dirImport[key]}")

                    elif event.key == self.pygame.K_c:
                        os_DIAG.system("cls")

            self.draw()


    
Diagnostic(pygame_DIAG)


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
#         os_DIAG.system("cls")

#     elif command_DIAG == "dir":
#         print()

#     else:
#         exec(command_DIAG)

