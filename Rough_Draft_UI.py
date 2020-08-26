from tkinter import *
from itertools import chain
import sqlite3 as sq
import time 
import datetime
 
#save onto text file from user input
def f():
    t = X_Coor.get()
    y = Y_Coor.get()
    file1 = open("text.txt", 'w')
    file1.write(t+ "\n"+y )
    file1.close()
    return

#Main GUI window frame 
window = Tk()
window.withdraw()
window.title("WELCOME TO USV BAY-STATION INTERFACE")
window.geometry('1050x550')

#define List box
list1 = Listbox(window, height = 9, width = 45)
list1.grid(row = 9, column = 2, rowspan = 3, columnspan=2)

# Attach scrollbar to the List
sb1 = Scrollbar(window)
sb1.grid(row=9,column=4,rowspan=3)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# Define Buttons
b1 = Button(window, text = "Battery-Level", width = 14)
b1.grid(row = 8, column = 0, pady = 10)

b1 = Button(window, text = "Leak-Detection", width = 14)
b1.grid(row = 9, column = 0, pady = 10)

b3 = Button(window, text = "Pressure-Data", width = 14)
b3.grid(row = 10, column = 0, pady = 10)

b4 = Button(window, text = "Velocity", width = 14)
b4.grid(row = 11, column = 0, pady = 10)

b5 = Button(window, text = "Auto-Dock", width = 14)
b5.grid(row = 2, column = 5, pady = 10)

b6 = Button(window, text = "System-log", width = 14)
b6.grid(row = 3, column = 5, pady = 10)

b7 = Button(window, text = "Check-log", width = 14)
b7.grid(row = 4, column = 5, pady = 10)

b8 = Button(window, text = "Video-Feed", width = 14)
b8.grid(row = 5, column = 5, pady = 10)

b9 = Button(window, text = "X-Coord-input", width = 14)
b9.grid(row = 8, column = 5, pady = 10)

b10 = Button(window, text = "Y-Coord-input", width = 14)
b10.grid(row = 9, column = 5, pady = 10)

b11 = Button(window, text = "Last-Update-Time", width = 14)
b11.grid(row = 0, column = 1, padx = 10, pady = 10)

b12 = Button(window, text = "Run-Time", width = 14)
b12.grid(row = 0, column = 5, padx = 10, pady = 10)

#framewindow for database records
frame = Frame(window)
frame.place(x= 710, y = 50)

Lb = Listbox(frame, height = 8, width = 25,font=("arial", 12)) 

scroll = Scrollbar(frame, orient = VERTICAL) # set scrollbar to list box for when entries exceed size of list box
scroll.config(command = Lb.yview)

scroll1 = Scrollbar(frame, orient = HORIZONTAL)
scroll1.config(command = Lb.xview)

Lb.config(yscrollcommand = scroll.set)
Lb.config(xscrollcommand = scroll1.set) 

scroll1.pack(side = BOTTOM, fill = X)
Lb.pack(side = LEFT, fill = Y)
scroll.pack(side = RIGHT, fill = Y)

Lb.insert(0, 'Time,   Message') #first row in listbox

b13 = Button(window, text = "OPEN DB File", width= 14, command=lambda:Record('counter'))
b13.grid(row = 0, column = 7, padx = 10)

#Define Labels
lbl = Label(window, text=" Position of the USV ", font = ( 'Times New Roman',11, "bold"))
lbl.grid(row = 1, column = 0)

lb2 = Label(window, text="X-Coordinate")
lb2.grid(row = 2, column = 0)

lb3 = Label(window, text="Y-Coordinate")
lb3.grid(row = 3, column = 0, pady = 10)

lb4 = Label(window, text="GPS, Earth Positioning", font = ( 'Times New Roman',11, "bold"))
lb4.grid(row = 4, column = 0)

lb5 = Label(window, text="longitude")
lb5.grid(row = 5, column = 0)

lb6 = Label(window, text="latitude")
lb6.grid(row = 6, column = 0)

lb7 = Label(window, text="System Check", font = ( 'Times New Roman',11, "bold"))
lb7.grid(row = 7,column = 0, pady=10)

lb8 = Label(window, text="User Commands", font = ( 'Times New Roman',11, "bold"))
lb8.grid(row = 1,column = 5, pady=10)

lb10 = Label(window, text="Ping/Go-Here", font = ( 'Times New Roman',11, "bold"))
lb10.grid(row = 7,column = 5, pady=10)

#define Entries
X_Coor = StringVar()
a1 = Entry(window, textvariable = X_Coor)
a1.grid(row = 2, column = 1)

Y_Coor = StringVar()
b1 = Entry(window, textvariable = Y_Coor)
b1.grid(row = 3,column = 1)

b = Button(window, text="save as file", command=lambda: f()) #button command is not activated till it is pushed. 
b.grid(row=1,column=1)

long = StringVar()
a1 = Entry(window, textvariable = long)
a1.grid(row = 5, column = 1)

lati = StringVar()
b1 = Entry(window, textvariable = lati)
b1.grid(row = 6,column = 1)

#loading screen as user first opens UI
class loading_screen:
    def __init__(self):
        self.level = Toplevel()
        self.percentage = 0
        Label(self.level,text="WELCOME TO USV BAY-STATION INTERFACE",font = ( 'Times New Roman',20, "bold") ).pack()
        self.load = Label(self.level,text=f"Loading...{self.percentage}%")
        self.load.pack()
        self.load_bar()

    def load_bar(self):
        self.percentage +=5
        self.load.config(text=f"Loading...{self.percentage}%")
        if self.percentage == 100:

            #finished loading to close loading_screen
            self.level.destroy()

            #window will appear again
            window.deiconify()
            return
        else:
            window.after(100,self.load_bar)

loading_screen()
#window.after(1000, Record)
window.mainloop()
f()
#window.after(20000, Record)
