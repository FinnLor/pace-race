# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: em fl fs
"""


import matplotlib.pyplot as plt
#import numpy as np
#import random as rn
import tkinter as tk



def disp_coord(event):
    #my_lbl['text']=str(event.x)
    my_lbl['text'] = f'x={event.x} y={event.y}'

def set_points(event):
    #my_canvas.create_oval(event.x,event.y,10,10,fill="blue")    
    #my_canvas.create_rectangle(event.x-1,event.y-1,event.x+1,event.y+1)   
    #my_canvas.create_rectangle(event.x,event.y,event.x,event.y)

    points_x = []
    points_y = []
    points_x.append(event.x)
    points_y.append(event.y)
    #my_canvas.create_line(points_x[len(points_x)-2], points_y[len(points_y)-2], points_x[len(points_x)-1], points_y[len(points_y)-1]
    #my_canvas.create_polygon(points,fill = "blue")
    #my_canvas.create_line(event.x,event.y,event.x,event.y)
    my_canvas.create_line(event.x-5,event.y+5,event.x+5,event.y-5)
    my_canvas.create_line(event.x-5,event.y-5,event.x+5,event.y+5)
    
    return points_x
    
    #plt(points_x, points_y)
    #plt.show()



my_wdw = tk.Tk()
my_wdw.title('PunkteSetzTest')
my_canvas = tk.Canvas(my_wdw, width=800, height=600, background = 'white')
my_lbl = tk.Label(bd=4, relief="solid", font="Times 22 bold", bg="white", fg="black")

my_canvas.bind('<Button-1>',set_points)
my_canvas.bind('<Button-3>',disp_coord)
my_canvas.grid(row=0, column=0)
my_lbl.grid(row=1, column=0)
# tk.Button(my_wdw, text='enough', command = lambda:my_wdw.destroy()).pack(expand=True)
# generates a button wich enbales to exit the mainloop
my_wdw.mainloop()



