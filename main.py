import tkinter
from time import sleep
from math import sin, cos, radians

# Btw assume 1 meter = 10 px

class Car:
    possible_states = ("do_nothing", "gas", "brake", "turn_right", "turn_left", "turn_right+gas", "turn_left+gas")
    weight = 1000 #kilograms
    tire_friction_coefficient_side = 1
    tire_friction_coefficient_rolling = 0.2
    acceleration = 1500 # N/s

    def __init__(self, canvas):
        # Create the car.
        self.car = [
            canvas.create_line(290, 280, 290, 320), # Left Vert
            canvas.create_line(310, 280, 310, 320), # Right Vert
            canvas.create_line(290, 280, 310, 280), # Top Hor
            canvas.create_line(290, 320, 310, 320), # Bot Hor
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
        self.orientation = 90 # degrees
        
        # Force vectors
        self.forward_force = [0, 0]
        self.frictional_force_f = [0, 0]
        self.inertial_force = [0, 0]
        self.frictional_force_i = [0, 0]
        self.net_force = [0, 0]
    

    def update(self):
        if self.state == Car.possible_states[0]:
            pass
        elif self.state == Car.possible_states[1]:
            self.forward_force
        elif self.state == Car.possible_states[2]:
            pass
        elif self.state == Car.possible_states[3]:
            pass
        elif self.state == Car.possible_states[4]:
            pass
        elif self.state == Car.possible_states[5]:
            pass
        elif self.state == Car.possible_states[6]:
            pass
        
        self.net_force = [
            self.forward_force[0] + self.frictional_force_f[0] + self.frictional_force_i[0] + self.inertial_force[0],
            self.forward_force[1] + self.frictional_force_f[1] + self.frictional_force_i[1] + self.inertial_force[1]
        ]


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
