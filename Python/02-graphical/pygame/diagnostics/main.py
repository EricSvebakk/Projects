
from gameboard import Gameboard
from cell import Cell

# Defines the size of the board
rows = 16
cols = 16
#rows, cols = int(input("rows: ")), int(input("cols: "))

# The board will be automatically
# generated and drawn when initalized
gb = Gameboard(rows, cols)

# diagnostic.Diagnostic()

# The loop will update the gameboard depending
# on the command written into the terminal
# "exit" can be inputted to end the program
# while (command := input("\ncommand: ")) != "exit":
    
#     # Writing nothing iterates the board 1 generation
#     if command == "":
#         gb.update()
#         gb.drawBoard()

#     # Writing "stable" runs the Game of Life
#     # until the board reaches a stable state
#     elif command == "stable":
#         stability = 0
#         currentNum = 0
#         lastNum = 0
        
#         # If number of updates does not change
#         # for 8 generations, then the board is stable
#         while stability < 8:
#             stats = gb.getStats()
#             currentNum = stats["numUpdated"]
            
#             # Checks if the number of updates has changed
#             if currentNum == lastNum:
#                 stability += 1
#             else:
#                 stability = 0

#             gb.update()
#             lastNum = currentNum
#         gb.drawBoard()

#     # Adds x generations to the current board
#     elif command == "add":
#         num = int(input("Add x generations: "))
#         for _ in range(num):
#             gb.update()
#         gb.drawBoard()

#     # A command for testing an extra method is created :))
#     elif command == "check":
        
#         print(f"\nRange for x: (1-{rows})")
#         x = int(input("x: ")) - 1
#         print(f"\nRange for y: (1-{cols})")
#         y = int(input("y: ")) - 1

#         # Only valid positions are inputted
#         if x <= rows and x > 0 and y <= cols and y > 0:
#             gb.checkCell(x, y)
#         else:
#             print("Invalid position!")
    
#     # If an unrecognized command is entered, an
#     # Error message is written to the terminal
#     else:
#         print(f"'{command}' not recognized. Valid commands:")
#         print('"stable", "add", "check", "exit"')


# eval('type(' + val + ')')

# print("\n==========================================")

# allVariables = list(globals())
# iterable = iter(allVariables)

# for i in range(len(allVariables)):
    
#     val = next(iterable)
#     evalval = eval(val)
#     myList = []

#     if "__" not in val:

#         if type(evalval) != int:
            
#             for item in list(dir(evalval)):
#                 if "__" not in item:
#                     myList.append(item)

#         pad = 12
#         print(f"{'variable:':<{pad}} {val}")
#         #print(f"{'type:':<{pad}} {type(val)}")
#         print(f"{'eval:':<{pad}} {evalval}")
#         print(f"{'type:':<{pad}} {type(evalval)}")
#         print(f"{'methods:':<{pad}} {myList}\n")


# while (command := input("> ")) != "exit":
#     eval(command)
