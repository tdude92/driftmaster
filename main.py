import tkinter
from time import sleep
from math import sqrt, sin, cos, radians

# Btw assume 1 meter = 10 px

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


class Car:
    possible_states = ("do_nothing", "gas", "brake", "turn_right", "turn_left", "turn_right+gas", "turn_left+gas")

    max_engine_force = 5000 # N
    drag_const = 0.4257
    rr_const = 12.8 # Rolling resistance constant.
    mass = 1000


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
        self.engine_force = 0
        self.velocity = [0, 0] # The car is at rest.

        # Forces and physics stuff.
        self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance
        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass
        
    
    def update(self): # Check at half-second intervals.
        # Update the values of the forces, acceleration, and velocity.
        self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance
        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass
        
        # Get velocity (v = v + dt * a)
        for i in range(len(self.velocity)):
            self.velocity[i] += 0.5 * self.acceleration[i]


root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 600, height = 600)
canvas.pack()

ae86 = Car(canvas)

for _ in range(60):
    ae86.update()
    print()
    print("Traction:" + str(magnitude(ae86.f_traction)))
    print("Drag:" + str(magnitude(ae86.f_drag)))
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)))
    print("Acceleration:" + str(magnitude(ae86.acceleration)))
    print("Velocity:" + str(magnitude(ae86.velocity)))

    ae86.engine_force += 100 if ae86.engine_force < Car.max_engine_force else 0
    sleep(0.1)
while True:
    ae86.update()
    print()
    print("Traction:" + str(magnitude(ae86.f_traction)))
    print("Drag:" + str(magnitude(ae86.f_drag)))
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)))
    print("Acceleration:" + str(magnitude(ae86.acceleration)))
    print("Velocity:" + str(magnitude(ae86.velocity)))

    ae86.engine_force -= 100 if ae86.engine_force > 0 else 0
    sleep(0.1)

root.mainloop()
