
import tkinter as tk

class Cell:

    def __init__(self, root, row, col, padx=0, pady=0):

        self.root = root
        self.row = row
        self.col = col

        self.obj = tk.Entry(self.root, width=10, border=1)
        self.obj.grid(row=self.row, column=self.col, padx=padx, pady=pady, sticky="news",)

        self.text(f"{self.row+1}:{self.col+1}")

    #==========================================================================#
    # Adds a new column to the spreadsheet                                     #
    #==========================================================================#
    def __repr__(self):
        return f"({self.row+1}:{self.col+1})"

    #==========================================================================#
    # Adds a new column to the spreadsheet                                     #
    #==========================================================================#
    def text(self, text):
        self.obj.delete(0, 0)
        self.obj.insert(0, text)
    
    #==========================================================================#
    # Adds a new column to the spreadsheet                                     #
    #==========================================================================#
    def destroy(self):
        self.obj.destroy()
