import tkinter
from time import sleep
from math import sqrt, sin, cos, radians

# Btw assume 1 meter = 10 px

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


class Car:
    possible_states = ("do_nothing", "gas", "brake", "turn_right", "turn_left", "turn_right+gas", "turn_left+gas")

    engine_force = 89484 # Watts
    drag_const = 0
    rr_const = 0 # Rolling resistance constant.


    def __init__(self, canvas):
        self.canvas = canvas

        # Create the car.
        self.car = [
            self.canvas.create_line(290, 280, 290, 320), # Left Vert
            self.canvas.create_line(310, 280, 310, 320), # Right Vert
            self.canvas.create_line(290, 280, 310, 280), # Top Hor
            self.canvas.create_line(290, 320, 310, 320), # Bot Hor
        ]
        # Calculate car center coordinates (where the car's "vision" lines originate from)
        self.car_centerX = (canvas.coords(self.car[2])[0] + canvas.coords(self.car[2])[2]) / 2
        self.car_centerY = (canvas.coords(self.car[0])[1] + canvas.coords(self.car[0])[3]) / 2
        self.turning_axis = [
            (canvas.coords(self.car[3])[0] + canvas.coords(self.car[3])[2]) / 2,
            (canvas.coords(self.car[3])[1] + canvas.coords(self.car[3])[3]) / 2
        ]

        # Set default state after creation.
        self.state = Car.possible_states[0]
        self.orientation = 90
        self.u = [cos(self.orientation), sin(self.orientation)] # Unit vector for the orientation of the car.
        self.velocity = [0, 0] # The car is at rest.

        # Forces and physics stuff.
        self.f_traction = [i * Car.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = Car.drag_const * self.velocity * magnitude(self.velocity)
        self.f_rr = [i * -Car.rr_const for i in self.velocity]


root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 600, height = 600)
canvas.pack()

"""
car_vision = []
for angle in (0, 45, 90, 135, 180, 225, 270, 315):
    x_displacement = 600*cos(radians(angle))
    y_displacement = 600*sin(radians(angle))
    car_vision.append(canvas.create_line(car_centerX, car_centerY, car_centerX + x_displacement, car_centerY + y_displacement))
    print(x_displacement, y_displacement)
"""
root.mainloop()
