# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:13:46 2021

@author: emilo
"""

from tkinter import *
import time

class car:
    
    def __init__(self,canvas,x,y,diameter,xVelocity,yVelocity,color):
        self.canvas = canvas
        self.image = canvas.create_oval(x,y,diameter,diameter,fill=color)
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        
    def move(self):
        coordinates = self.canvas.coords(self.image)
        print(coordinates)
        self.canvas.move(self.image,self.xVelocity,self.yVelocity)

  
    # def pos(self):
    #     return self.canvas.coords(self.image)


wdw01 = Tk()
WIDTH = 800
HEIGHT = 600
track = Canvas(wdw01, width=WIDTH, height=HEIGHT)
track.pack()

# construct some cars
car01 = car(track,0,0,100,1,1,"green")


while True:
    car01.move()
    wdw01.update()
    time.sleep(0.02)

wdw01.mainloop()

