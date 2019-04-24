import tkinter
from time import sleep
from math import sqrt, sin, cos, acos, radians

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


class Car:
    possible_states = ("do_nothing", "gas", "brake", "turn_right", "turn_left", "turn_right+gas", "turn_left+gas")

    max_engine_force = 2000 # N
    mass = 1000 # kg
    drag_const = 0.39 # Drag constant.
    rr_const = 11.7 # Rolling resistance constant.
    braking_const = mass * 9.8 * 0.9 # Friction = normal force [AKA m * g] * friction coefficient.


    def __init__(self, canvas):
        self.canvas = canvas

        # Create the car.
        self.car = [
            self.canvas.create_line(490, 480, 490, 520), # Left Vert
            self.canvas.create_line(510, 480, 510, 520), # Right Vert
            self.canvas.create_line(490, 480, 510, 480), # Top Hor
            self.canvas.create_line(490, 520, 510, 520), # Bot Hor
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
        self.orientation = radians(90)
        self.u = [cos(self.orientation), sin(self.orientation)] # Unit vector for the orientation of the car.
        self.engine_force = 0
        self.velocity = [0, 0] # The car is at rest.

        # Forces and physics stuff.
        self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance
        self.f_braking = [0, 0] # direction unit vector * braking force
        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass
        
    
    def update(self): # Check at half-second intervals.
        # Update the values of the forces, acceleration, and velocity.
        if self.state == Car.possible_states[0]: # Car is doing nothing.
            self.f_traction = [0, 0]
            self.f_braking = [0, 0]
        elif self.state == Car.possible_states[1]: # GAS GAS GAS
            self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
            self.f_braking = [0, 0]
        elif self.state == Car.possible_states[2]: # Driver is being a coward (braking)
            self.f_traction = [0, 0]
            # There should be no braking force if the car is not moving.
            if [round([i * magnitude(self.velocity) for i in self.u][i] - self.velocity[i]) for i in range(2)] == [0, 0] and magnitude(self.velocity) > 10:
                # Check if self.velocity's direction is the same as the direction of self.u (orientation) and if the velocity's magnitude is not 0.
                self.f_braking = [-i * Car.braking_const for i in self.u] # direction unit vector * braking force
            else:
                self.f_braking = [0, 0]
                self.velocity = [0, 0]
                self.state = Car.possible_states[0]
                #no_accelerate_flag = True

        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance

        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i] + self.f_braking[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass.

        # Get velocity (v = v + dt * a) in m/s
        for i in range(len(self.velocity)):
            self.velocity[i] += self.acceleration[i]
        
        for line in self.car:
            self.canvas.move(line, self.velocity[0], -(self.velocity[1]))
        
        canvas.update()


root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 1000, height = 1000)
canvas.pack()

ae86 = Car(canvas)
ae86.state = Car.possible_states[1]

for i in range(10):
    ae86.update()
    print()
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")

    ae86.engine_force += 1000 if ae86.engine_force < Car.max_engine_force else 0
    sleep(0.1)

ae86.state = Car.possible_states[2]
print("BRAKE")

while True:
    ae86.update()
    print()
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")

    ae86.engine_force -= 100 if ae86.engine_force > 0 else 0
    sleep(0.1)

root.mainloop()
