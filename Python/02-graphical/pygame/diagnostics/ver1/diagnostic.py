
import pygame as pygame_DIAG
import os as os_DIAG

dir_DIAG = []
for item_DIAG in os_DIAG.listdir():

    if ".py" not in item_DIAG or "diagnostic" in item_DIAG:
        continue

    dir_DIAG.append(dir_DIAG)

    item_DIAG = item_DIAG.strip(".py")
    
    command_DIAG = f"from {item_DIAG} import *"
    exec(command_DIAG, globals())


# Diagnostic Class
class Diagnostic:

    #===================================================================
    def __init__(self):
        
        self._rawGlobalVariables = list(globals())
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

