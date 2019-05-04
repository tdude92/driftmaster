import tkinter
from time import sleep
from car import *
from evolution import *


root = tkinter.Tk()
canvas = tkinter.Canvas(root, width = 600, height = 600, bg = "black")
canvas.pack()

walls = [
    canvas.create_line(10, 10, 10, 590, fill = "white", width = 2),
    canvas.create_line(590, 10, 590, 500, fill = "white", width = 2),
    canvas.create_line(10, 10, 190, 110, fill = "white", width = 2),
    canvas.create_line(190, 110, 190, 300, fill = "white", width = 2),
    canvas.create_line(190, 300, 490, 300, fill = "white", width = 2),
    canvas.create_line(490, 300, 490, 10, fill = "white", width = 2),
    canvas.create_line(490, 10, 590, 10, fill = "white", width = 2),
    canvas.create_line(10, 590, 590, 500, fill = "white", width = 2), # Inside Lines Start:
    canvas.create_line(40, 100, 40, 560, fill = "white", width = 2),
    canvas.create_line(560, 40, 560, 470, fill = "white", width = 2),
    canvas.create_line(40, 100, 160, 165, fill = "white", width = 2),
    canvas.create_line(160, 165, 160, 330, fill = "white", width = 2),
    canvas.create_line(160, 330, 520, 330, fill = "white", width = 2),
    canvas.create_line(520, 330, 520, 40, fill = "white", width = 2),
    canvas.create_line(520, 40, 560, 40, fill = "white", width = 2),
    canvas.create_line(40, 560, 560, 470, fill = "white", width = 2),
]

test_car = Car(canvas, walls, 295, 490, 305, 510)

test_car.engine_force = 2000
for i in range(500):
    test_car.state = Car.possible_states[randint(0, 4)]
    print(test_car.state)
    for i in range(10):
        test_car.update()
        sleep(0.1)

root.mainloop()
