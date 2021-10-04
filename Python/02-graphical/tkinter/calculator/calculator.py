
from tkinter import *
from tkinter import font as TKFont 

# Adds symbol to entry
def button_click(symbol):
    
    temp = entry.get()
    entry.delete(0,END)
    if temp == "0":
        if symbol == ".":
            entry.insert(0, temp + symbol)
        else:
            entry.insert(0, symbol)
    else:
        entry.insert(0, temp + symbol)

# Calculates value of entry via eval
def button_equals():
    temp = entry.get()
    entry.delete(0, END)
    if eval(temp) % 1 == 0:
        entry.insert(0, int(eval(temp)))
    else:
        entry.insert(0, round(eval(temp),3))

# Clears entry
def button_clear():
    entry.delete(0, END)
    entry.insert(0, "0")

# Window
root = Tk()
root.title("Calculator")
# root.iconbitmap("C:\\Users\\Eric\\Documents\\Projects\\Python\\004 tkinter\\calculator2.ico")
# root.configure(background="white")

btn = {}
padx = 20
pady = 10
font = TKFont.Font(family="Consolas", size="20")

entry = Entry(root, width=22, border=0, font=font, background="#F0F0F0", justify="center")
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=20)
entry.insert(0, "0")


# Button content
font = TKFont.Font(family="Consolas", size="20")

btn["7"] = Button(root, text="7", padx=padx, pady=pady, font=font, command=lambda: button_click("7"))
btn["8"] = Button(root, text="8", padx=padx, pady=pady, font=font, command=lambda: button_click("8"))
btn["9"] = Button(root, text="9", padx=padx, pady=pady, font=font, command=lambda: button_click("9"))
btn["C"] = Button(root, text="C", padx=(padx*2)+18, pady=pady, font=font, command=button_clear)

btn["4"] = Button(root, text="4", padx=padx, pady=pady, font=font, command=lambda: button_click("4"))
btn["5"] = Button(root, text="5", padx=padx, pady=pady, font=font, command=lambda: button_click("5"))
btn["6"] = Button(root, text="6", padx=padx, pady=pady, font=font, command=lambda: button_click("6"))
btn["+"] = Button(root, text="+", padx=padx, pady=pady, font=font, command=lambda: button_click("+"))
btn["*"] = Button(root, text="*", padx=padx, pady=pady, font=font, command=lambda: button_click("*"))

btn["1"] = Button(root, text="1", padx=padx, pady=pady, font=font, command=lambda: button_click("1"))
btn["2"] = Button(root, text="2", padx=padx, pady=pady, font=font, command=lambda: button_click("2"))
btn["3"] = Button(root, text="3", padx=padx, pady=pady, font=font, command=lambda: button_click("3"))
btn["-"] = Button(root, text="-", padx=padx, pady=pady, font=font, command=lambda: button_click("-"))
btn["/"] = Button(root, text="/", padx=padx, pady=pady, font=font, command=lambda: button_click("/"))

btn["."] = Button(root, text=".", padx=padx, pady=pady, font=font, command=lambda: button_click("."))
btn["0"] = Button(root, text="0", padx=padx, pady=pady, font=font, command=lambda: button_click("0"))
btn["="] = Button(root, text="=", padx=(padx*3)+36, pady=pady, font=font, command=button_equals)

# Button positions
btn["7"].grid(row=1, column=0)
btn["8"].grid(row=1, column=1)
btn["9"].grid(row=1, column=2)
btn["C"].grid(row=1, column=3, columnspan=2)

btn["4"].grid(row=2, column=0)
btn["5"].grid(row=2, column=1)
btn["6"].grid(row=2, column=2)
btn["+"].grid(row=2, column=3)
btn["*"].grid(row=2, column=4)

btn["1"].grid(row=3, column=0)
btn["2"].grid(row=3, column=1)
btn["3"].grid(row=3, column=2)
btn["-"].grid(row=3, column=3)
btn["/"].grid(row=3, column=4)

btn["."].grid(row=4, column=0)
btn["0"].grid(row=4, column=1)
btn["="].grid(row=4, column=2, columnspan=3)

# Mainloop
root.mainloop()
