
# import tkinter as tk
# from tkinter import font as TKFont

# #==========================================================================#
# #==========================================================================#
# class Spreadsheet:

#     def __init__(self, title):
        
#         self.root = tk.Tk()
#         self.root.title(title)
#         self.root.grid_rowconfigure(0, weight=1)
#         self.root.grid_columnconfigure(0, weight=1)
#         # self.root.attributes("-fullscreen", 1)

#         # 
#         self.frame_main = tk.Frame(self.root, bg="red")
#         self.frame_main.grid(sticky="news")

#         self.frame_canv = tk.Frame(self.frame_main)
#         self.frame_canv.grid(row=0, column=0, sticky="nw")
#         self.frame_canv.grid_rowconfigure(0, weight=1)
#         self.frame_canv.grid_columnconfigure(0, weight=1)

#         self.canv = tk.Canvas(self.frame_canv, bg="purple")
#           # scrollregion=(0, 0, 1000, 1000), yscrollcommand=self.scroll.set
#         self.canv.grid(row=0, column=0, sticky="news")

#         self.vsb = tk.Scrollbar(self.frame_canv, orient="vertical", command=self.canv.yview)
#         self.vsb.grid(row=0, column=1, sticky="ns")
#         self.canv.config(yscrollcommand=self.vsb.set)

#         self.hsb = tk.Scrollbar(self.frame_canv, orient="horizontal", command=self.canv.yview)
#         self.hsb.grid(row=1, column=0, sticky="ew")
#         self.canv.config(xscrollcommand=self.hsb.set)
    

#         numRows = 5
#         numCols = 6

#         self.frame_grid = tk.Frame(self.canv, bg="blue", bd=2)

#         self.grid = Grid(self.frame_grid, numRows, numCols, 0, 0)

#         self.canv.create_window((0,0), window=self.frame_grid, anchor="nw")
#         # self.canv.config(scrollregion=(0, 0, 100, 100), width=50, height=50)
        

#         self.container = None
#         self.grid = None
#         self.btn = {}
        
#         self.font = TKFont.Font(family="Consolas", size="20")
#         self.padx = 30
#         self.pady = 20

#     #==========================================================================#
#     #==========================================================================#
#     def create(self, numRows, numCols):

#         # font = self.font
#         # padx = self.padx
#         # pady = self.pady

#         # self.container = tk.Frame(self.fra)
#         # self.container.grid(columnspan=100, row=0, column=0, sticky="w")

#         self.btn["X"] = tk.Button(self.frame_main, text="X", command=self.root.destroy)
#         # self.btn["r+"] = tk.Button(self.frame_main, text="r+", command=self.grid._addRow)
#         # self.btn["r-"] = tk.Button(self.frame_main, text="r-", command=self.grid._subRow)
#         # self.btn["c+"] = tk.Button(self.frame_main, text="c+", command=self.grid._addCol)
#         # self.btn["c-"] = tk.Button(self.frame_main, text="c-", command=self.grid._subCol)

#         self.btn["X"].grid(row=0, column=1)
#         # self.btn["r+"].grid(row=0, column=2)
#         # self.btn["r-"].grid(row=0, column=3)
#         # self.btn["c+"].grid(row=0, column=4)
#         # self.btn["c-"].grid(row=0, column=5)

#         # for btn in self.btn.values():
#         #     btn.config(font=font)
#         #     btn.config(padx=padx)
#         #     btn.config(pady=pady)

#         self.root.mainloop()

#     #==========================================================================#
#     #==========================================================================#
#     def addIcon(self, path):
#         self.root.iconbitmap(path)


import tkinter as tk
from grid import Grid

class MyApp(tk.Tk):
    def __init__(self, title="Sample App"):

        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(background="gray")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.geometry("500x500")

        frame_root = tk.Frame(self.root, bg="Light Blue", bd=3, relief="ridge")
        frame_root.grid(sticky="NEWS")
        frame_root.columnconfigure(0, weight=1)
        frame_root.rowconfigure(0, weight=1)

        # Frame for canvas and scrollbars
        frame_canvas = tk.Frame(frame_root, bg="pink")
        frame_canvas.grid(row=1, column=0, sticky="NEWS") # Add sticky="NEWS" to fill window width
        frame_canvas.columnconfigure(0, weight=1)

        # Add a canvas in that frame.
        self.canvas = tk.Canvas(frame_canvas, bg="Yellow")
        self.canvas.grid(row=0, column=0, sticky="NEWS")

        # Fills canvas with cells
        self.grid = Grid(self.canvas, 10, 10)
        self.frame_grid = self.grid.getContent()

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        vsbar.grid(row=0, column=1, sticky="NS")
        self.canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame_canvas, orient="horizontal", command=self.canvas.xview)
        hsbar.grid(row=1, column=0, sticky="EW")
        self.canvas.configure(xscrollcommand=hsbar.set)

        # Navbar (frame 1)
        frame_navbar = tk.Frame(frame_root, bg="light green", padx=10, pady=10)
        frame_navbar.grid(row=0, column=0, sticky="NEWS")

        # Buttons for editing number of cells in grid
        btn = {}
        btn["r+"] = tk.Button(frame_navbar, text="r+", command=self.addRow)
        btn["r-"] = tk.Button(frame_navbar, text="r-", command=self.subRow)
        btn["c+"] = tk.Button(frame_navbar, text="c+", command=self.addCol)
        btn["c-"] = tk.Button(frame_navbar, text="c-", command=self.subCol)
        
        for i, b in enumerate(btn.values()):
            b.grid(row=0, column=i)

        # Create canvas window to hold the buttons_frame.
        self.canvas.create_window((0, 0), window=self.frame_grid, anchor="nw")

        self.update()
        self.root.mainloop()

    def update(self):
        self.frame_grid.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
        self.canvas.configure(scrollregion=bbox)

    def addRow(self):
        self.grid._addRow()
        self.update()

    def subRow(self):
        self.grid._subRow()
        self.update()

    def addCol(self):
        self.grid._addCol()
        self.update()

    def subCol(self):
        self.grid._subCol()
        self.update()
