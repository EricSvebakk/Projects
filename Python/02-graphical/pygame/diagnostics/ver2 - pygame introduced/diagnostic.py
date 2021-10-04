
from os import error
import pygame as pygame_DIAG
import os as os_DIAG

#===================================================================
class Diagnostic:

    def __init__(self):
        
        self._rawGlobalVariables = list(dir())
        self._iterable = iter(self._rawGlobalVariables)
        self._variableDict = {}

        self._updateVariableDict()

    #===================================================================
    def __str__(self):

        output = "\nDiagnostic methods are:\n"

        for method in dir(self):
            if "_" not in method:
                output += f"* {method}\n"

        return output

    #===================================================================
    def _updateVariableDict(self):

        for _ in range(len(self._rawGlobalVariables)):

            var = next(self._iterable)
            evalvar = eval(var)
            varMethods = []

            if ("__" in var) or ("DIAG".lower() in var.lower()):
                continue

            for item in list(dir(evalvar)):
                if "__" not in item:
                    varMethods.append(item)

            self._variableDict[var] = {}
            self._variableDict[var]["name"] = var
            self._variableDict[var]["type"] = type(evalvar)
            self._variableDict[var]["value"] = evalvar
            self._variableDict[var]["methods"] = varMethods

    #===================================================================
    def getVariables(self):
        
        output = "\nAll variables in directory:\n"
        
        for variable in self._variableDict.keys():
            
            if variable in output:
                print(f"DUPLICATE: {variable}")

            output += f"* {variable}\n"

        return output

    #===================================================================
    def getAttributes(self):

        pad = 12
        seperator = "=" * 55 + "\n"
        output = ""

        for variable in self._variableDict:

            if "lib" in str(self._variableDict[variable]["name"]):
                continue
            
            output += seperator
            
            for attribute in self._variableDict[variable]:
                
                if attribute == "methods":

                    spacing = f"{attribute}:"
                    for method in self._variableDict[variable][attribute]:
                        output += f"{spacing:<{pad}}"    
                        output += f"{method}\n"
                        spacing = ""
                        
                else:
                    output += f"{attribute+':':<{pad}}{self._variableDict[variable][attribute]}\n"

        output += seperator

        return output

#===================================================================

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
class Gameboard_DIAG:
    
    def __init__(self, pygame, diagnostic, width=600, height=600, bgColour = (255,255,255)):
        
        self.pygame = pygame
        self.diagnostic = diagnostic

        self.width = width
        self.height = height
        self.bgColour = bgColour

        self.pygame.init()
        self.screen = self.pygame.display.set_mode((self.width, self.height))
        self.pygame.display.set_caption("Diagnostic")
        
        self.dirImport = None

        self.containers = {
            "menu": [],
            "file": [],
            "outerContent": [],
            "innerContent": [],
            "attributes": []
        }
        
        self.getDir()
        #self.updateContainer(["Show Directory"], self.containers["menu"], 120, 50)
        #self.gameloop()

    #===================================================================
    def draw(self):

        self.screen.fill(self.bgColour)

        for key in self.containers:
            for objectList in self.containers[key]:
                for obj in objectList.boxes:

                    self.pygame.draw.rect(self.screen, *obj)

                self.screen.blit(*objectList.cText)

        self.pygame.display.update()

    #===================================================================
    def update(self, selected):
        
        if selected:
            newDir = dir(self.dirImport["value"][selected])

            self.updateContainer(self.importName, self.containers["outerContent"], 80, 50)

            self.updateContainer(newDir, self.containers["innerContent"], 250, 50)

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
    def attributes(self):
        pass
        #print(self.imports)

        #self.updateContainer(self.imports)

        #print(myList[1].randint(0,4))

        #del cols

        # print(self.diagnostic.getVariables())

        # for _ in range(len(self._rawGlobalVariables)):

        #     var = next(self._iterable)
        #     evalvar = eval(var)
        #     varMethods = []

        #     if ("__" in var) or ("DIAG".lower() in var.lower()):
        #         continue

        #     for item in list(dir(evalvar)):
        #         if "__" not in item:
        #             varMethods.append(item)

        #     self._variableDict[var] = {}
        #     self._variableDict[var]["name"] = var
        #     self._variableDict[var]["type"] = type(evalvar)
        #     self._variableDict[var]["value"] = evalvar
        #     self._variableDict[var]["methods"] = varMethods

    #===================================================================
    def selectWithMouse(self, xPos:int, yPos):

        print(xPos)

        print(self)

        for key in self.containers:
            for (index, objects) in enumerate(self.containers[key]):
    
                if objects.boxes[0][1].collidepoint(xPos, yPos):
                    
                    print(xPos, yPos)
                    return index

    #===================================================================
    def getDir(self):

        self.dirImport = []
        dirList = []

        for item in os_DIAG.listdir():
            if __file__ not in item and ".py" in item:
                dirList.append(item)


        for fileName in dirList:
            fileName = fileName.strip(".py")
            fileContent = __import__(fileName)
            self.dirImport.append((fileName, fileContent))


        self.containers = {}

        for (fileName, fileContent) in self.dirImport:

            self.containers[fileName] = {}

            for (refName, refContent) in vars(fileContent).items():

                if "__" not in refName:

                    self.containers[fileName][refName] = {}
                    self.containers[fileName][refName]["type"] = type(refContent)
                    self.containers[fileName][refName]["value"] = refContent

                    if type(refContent) == type:

                        self.containers[fileName][refName]["methods"] = []

                        for methodName in dir(refContent):

                            if "__" not in methodName:
                                self.containers[fileName][refName]["methods"].append(methodName)

        print("\n\n")

        for file in self.containers:
            print(file, ".py", sep="")
            
            for variable in self.containers[file]:
                print("*", variable)

                for attribute in self.containers[file][variable]:
                    if attribute != "methods":
                        print("**", attribute, ":", self.containers[file][variable][attribute])
                    else:

                        print("**", attribute)
                        for method in self.containers[file][variable][attribute]:
                            print("*** ", method, "()", sep="")

                print()

            print()

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
                        for key in self.containers:
                            print(f"{key}: {self.containers[key]}")

                    elif event.key == self.pygame.K_o:
                        for key in self.dirImport:
                            print(f"{key}: {self.dirImport[key]}")

                    elif event.key == self.pygame.K_c:
                        os_DIAG.system("cls")

            self.draw()


    
Gameboard_DIAG(pygame_DIAG, Diagnostic())


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

