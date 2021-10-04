
from os import system as sys
from random import randint
from cell import Cell

class Gameboard:

    # The Gameboard class-object requires
    # a number for rows and columns to initialize
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = []

        # A variable for tracking the statistics
        # for the current Gameboard
        self._stats = {
            "generation": 0,
            "numUpdated": 0,
            "numTotal": 0,
            "numAlive": 0
        }

        # The board is automatically generated and drawn
        # after the class is called in the main python file
        self.generate()
        #self.drawBoard()

    # A method for creating the board with the specified
    # dimensions and filling it with cells.
    def generate(self):

        # Statistics tracking
        self._stats["generation"] = 0
        self._stats["numTotal"] = 0

        # Loop for creating each row
        for y in range(self._cols):
            self._grid.append([])

            # Loop for adding cells to each row
            for x in range(self._rows):
                cell = Cell()

                # Each cell has a 1/3 chance to start
                # generation 0 being alive
                if randint(0, 2) == 1:
                    cell.alive()

                self._grid[y].append(cell)

                # Statistics tracking
                self._stats["numTotal"] += 1
                

    # A method for drawing the current state of the board
    def drawBoard(self):

        # The os-module has been imported to allow clearing
        # of the terminal before the board is drawn
        sys("cls")

        # String containing the top and bottom border for board
        prStr = "-" * self._rows *2 + "---"
        print(prStr)

        # Nested for-loop for creating the board
        for y in range(self._cols):
            r = "| "
            for x in range(self._rows):

                r += f"{self._grid[y][x]} "

            r += f"|"
            print(r)

        # Bottom border
        print(prStr)

        # After the board has been drawn, statistics are printed as well
        print(f"{'Generation:':<12} {self._stats['generation']}")
        print(f"{'Updates:':<12} {self._stats['numUpdated']} cells")
        print(f"{'Alive:':<12} {self._stats['numAlive']} / {self._stats['numTotal']}")

    # A method which returns all neighbouring cells to a specified cell-position
    def findNeighbours(self, xC:int, yC:int) -> list:

        neighbours = []

        # iterates over the cells "above" and
        # "below" of a specified cell-position
        for yi in range(-1, 2):
            yi += yC

            # y-positions which are too small
            # or too large are skipped
            if yi < 0 or yi > self._cols-1:
                continue
            
            # iterates over the cells "left" and
            # "right" of a specified cell-position
            for xi in range(-1, 2):
                xi += xC

                # x-positions which are too small
                # or too large are skipped
                if xi < 0 or xi > self._rows-1:
                    continue

                # The cell specified for findNeighbours() is 
                # not included among the list of neighbours
                if yi == yC and xi == xC:
                    continue
                
                # The remainder of positions (which are all valid positions)
                # are added to the list of neighbours
                else:
                    neighbours.append(self._grid[yi][xi])

        return neighbours

    # A method which follows the rules of "The Game Of Life" and
    # updates every cell on the gameboard and increases the current generation
    def update(self):

        # Statistics tracking
        self._stats["generation"] += 1
        self._stats["numUpdated"] = 0
        self._stats["numAlive"] = 0

        changeToAlive = []
        changeToDead = []

        # Nested for-loop for iterating over every cell
        for y in range(self._cols):
            for x in range(self._rows):
                
                # Gets the surrounding neighbour cells for
                # the cell with position (x,y)
                neighbours = self.findNeighbours(x, y)
                aliveNeighbours = 0

                for neighbour in neighbours:
                    if neighbour.status():
                        aliveNeighbours += 1

                # An if-statement which determines if a cell
                # updates from alive to dead in the next generation
                if self._grid[y][x].status():
                    if aliveNeighbours > 3 or aliveNeighbours < 2:
                        changeToDead.append(self._grid[y][x])

                        # Statistics tracking
                        self._stats["numUpdated"] += 1
                        self._stats["numAlive"] += 1

                # An if-statement which determines if a cell
                # updates from dead to alive in the next generation
                else:
                    if aliveNeighbours == 3:
                        changeToAlive.append(self._grid[y][x])
                        self._stats["numUpdated"] += 1

        # Two for-loops for flipping the state of certain cells
        for cell in changeToAlive:
            cell.alive()
        for cell in changeToDead:
            cell.dead()

    # A method for accessing gameboard statistics
    def getStats(self):
        return self._stats

    # An extra method that requires an x and y-position which
    # will be marked on the gameboard for tracking specific cells.
    # A smaller 3x3 is also drawn for specified cell 
    # ***NB: The 3x3 board does not work for cells around the edge
    def checkCell(self, xC, yC):

        # The os-module has been imported to allow clearing
        # of the terminal before the board is drawn
        sys("cls")

        # String containing the top and bottom border for board
        prStr = "-" * self._rows * 2 + "---"
        print(prStr)

        # Nested for-loop for creating the board
        for yi in range(self._cols):
            r = "| "
            for xi in range(self._rows):
                
                # If a cell matches the coordinated given
                # by the method, the cell is highlighted
                if yi == yC and xi == xC:
                    
                    # Living are highlighted with "Ø"
                    if self._grid[yi][xi].status():
                        r += "Ø "

                    # Dead cells are highlighted with "*"
                    else:
                        r += "* "

                # All other cells are drawn normally
                else:
                    r += f"{self._grid[yi][xi]} "

            r += f"|"
            print(r)

        # Bottom border
        print(prStr)

        # Gets the surrounding neighbour cells for
        # the cell with position (x,y)
        neighbours = self.findNeighbours(xC, yC)
        r = "| "

        # The 3x3 board is drawn with one loop
        for i in range(len(neighbours)):
            
            r += f"{neighbours[i]} "

            # For the 4th iteration, the loop will
            # add the cell specific for the method
            # since the loop iterates over the neighbours
            if i == 3:
                if self._grid[yC][xC].status():
                    r += "Ø "
                else:
                    r += "* "
            
            # A linebreak is added for the end
            # of the first and second line
            if i in [2,4]:
                r += "|\n| "

        # Prints the 3x3 board
        print(f"---------")
        print(f"{r}|")
        print(f"---------")
