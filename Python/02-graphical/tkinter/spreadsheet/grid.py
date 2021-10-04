
import tkinter as tk
from cell import Cell
from os import system as sys

class Grid:

    def __init__(self, master, rows, cols):

        self.master = master
        self.numRows = rows
        self.numCols = cols

        self.padx = 0
        self.pady = 0

        self.container = tk.Frame(self.master, bd=2, bg="red")
        self.container.grid(row=0, column=0)
        self.grid = []

        for row in range(self.numRows):
            tempList = []

            for column in range(self.numCols):

                tempList.append(Cell(self.container, row, column, self.padx, self.pady))

            self.grid.append(tempList)

        self.lastRow = len(self.grid)
        self.lastCol = len(self.grid[0])

    def _info(self):
        # sys("cls")
        # for row in self.grid:
        #     print(row)
        pass

    def getContent(self):
        return self.container

    #==========================================================================#
    # Adds a new row to the spreadsheet                                        #
    #==========================================================================#
    def _addRow(self):

        row = self.lastRow

        tempList = []
        for col in range(self.lastCol):
            tempList.append(Cell(self.container, row, col, self.padx, self.pady))

        self.grid.append(tempList)
        self.lastRow += 1
        self._info()

    #==========================================================================#
    # Adds a new row to the spreadsheet                                        #
    #==========================================================================#
    def _subRow(self, row=None):

        if not row:
            row = self.lastRow-1

        temp = self.grid.pop(row)

        for cell in temp:
            cell.destroy()

        self.lastRow -= 1
        self._info()

    #==========================================================================#
    # Adds a new column to the spreadsheet                                     #
    #==========================================================================#
    def _addCol(self):

        col = self.lastCol

        for row in range(self.lastRow):
            self.grid[row].append(Cell(self.container, row, col, self.padx, self.pady))

        self.lastCol += 1
        self._info()

    #==========================================================================#
    # Adds a new column to the spreadsheet                                     #
    #==========================================================================#
    def _subCol(self, col=None):
        
        if not col:
            col = self.lastCol-1

        for row in range(self.lastRow):
            cell = self.grid[row].pop(col)
            cell.destroy()

        self.lastCol -= 1
        self._info()
