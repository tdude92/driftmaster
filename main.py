from tkinter import *
from time import sleep
from math import sin, cos, radians

class InputNode:
    def __init__(self, line, walls):
        self.line = line

    def get_value(self, canvas):
        for i in canvas.find_overlapping(self.line):
            
            

root = Tk()

canvas = Canvas(root, width = 600, height = 600)
canvas.pack()
"""
canvas.create_line(20, 20, 20, 590)
canvas.create_line(20, 20, 590, 20)
canvas.create_line(590, 20, 590, 590)
canvas.create_line(590, 590, 20, 590)
"""

car = [
    canvas.create_line(290, 280, 290, 320), # Left Vert
    canvas.create_line(310, 280, 310, 320), # Right Vert
    canvas.create_line(290, 280, 310, 280), # Top Hor
    canvas.create_line(290, 320, 310, 320), # Bot Hor
]
car_centerX = (canvas.coords(car[2])[0] + canvas.coords(car[2])[2]) / 2
car_centerY = (canvas.coords(car[0])[1] + canvas.coords(car[0])[3]) / 2

car_vision = []
for angle in (0, 45, 90, 135, 180, 225, 270, 315):
    x_displacement = 600*cos(radians(angle))
    y_displacement = 600*sin(radians(angle))
    car_vision.append(canvas.create_line(car_centerX, car_centerY, car_centerX + x_displacement, car_centerY + y_displacement))
    print(x_displacement, y_displacement)

root.mainloop()
