import tkinter
from time import sleep
from math import sqrt, sin, cos, acos, radians

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


class Car:
    possible_states = (
        "do_nothing",
        "gas",
        "brake",
        "turn_right",
        "turn_left",
        "turn_right+gas",
        "turn_left+gas",
        "turn_right+brake",
        "turn_left+brake",
    )

    max_engine_force = 4000 # N
    mass = 1000 # kg
    wheelbase = 2.4 # m
    steering_angle = radians(45) # radian
    sharp_steering_angle = radians(75) # radians
    drag_const = 0.39 # Drag constant.
    rr_const = 11.7 # Rolling resistance constant.
    braking_const = mass * 9.8 * 0.9 # Friction = normal force [AKA m * g] * friction coefficient.
    cornering_stiffness = 50 # N


    def __init__(self, canvas):
        self.canvas = canvas

        # Create the car.
        self.car = [
            self.canvas.create_line(490, 880, 490, 920, fill = "green", width = 2), # Left Vert
            self.canvas.create_line(510, 880, 510, 920, fill = "green", width = 2), # Right Vert
            self.canvas.create_line(490, 880, 510, 880, fill = "green", width = 2), # Top Hor
            self.canvas.create_line(490, 920, 510, 920, fill = "green", width = 2), # Bot Hor
        ]

        # Calculate car center coordinates
        self.car_centerX = (canvas.coords(self.car[2])[0] + canvas.coords(self.car[2])[2]) / 2
        self.car_centerY = (canvas.coords(self.car[0])[1] + canvas.coords(self.car[0])[3]) / 2

        # Set default state after creation.
        self.state = Car.possible_states[0]
        self.orientation = radians(90)
        self.u = [cos(self.orientation), sin(self.orientation)] # Unit vector for the orientation of the car.
        self.engine_force = 0
        self.velocity = [0, 0] # The car is at rest.
        self.angular_velocity = 0 # radians/s

        # Forces and physics stuff.
        self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance
        self.f_braking = [0, 0] # direction unit vector * braking force
        self.f_lateral = [0, 0]
        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i] + self.f_lateral[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass
        
    
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
        elif self.state == Car.possible_states[3]: # Cowardly right turn.
            self.f_traction = [0, 0]
            self.f_braking = [0, 0]

            self.turning_radius = Car.wheelbase / sin(Car.steering_angle) # R = L / sin(steering_angle)
            self.angular_velocity = (magnitude(self.velocity) / self.turning_radius) / 10 # av = |v| / R
            self.orientation += self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]

            # TODO: MAKE THIS WORK
            self.slip_angle = abs(acos(self.velocity[0]) / magnitude(self.velocity) - acos(self.u[0]))
            self.mag_lateral = Car.cornering_stiffness * self.slip_angle
            self.f_lateral = [sin(self.slip_angle) * -i for i in self.velocity]

            # Recreate the turned car with some trig.
            self.front_center = [
                self.car_centerX + 20 * cos(self.orientation),
                self.car_centerY - 20 * sin(self.orientation)
            ]
            self.back_center = [
                self.car_centerX - 20 * cos(self.orientation),
                self.car_centerY + 20 * sin(self.orientation)
            ]

            self.top_right = [
                self.front_center[0] + 10 * cos(self.orientation - radians(90)),
                self.front_center[1] - 10 * sin(self.orientation - radians(90)),
            ]
            self.top_left = [
                self.front_center[0] + 10 * cos(self.orientation + radians(90)),
                self.front_center[1] - 10 * sin(self.orientation + radians(90)),
            ]
            self.bot_right = [
                self.back_center[0] + 10 * cos(self.orientation - radians(90)),
                self.back_center[1] - 10 * sin(self.orientation - radians(90)),
            ]
            self.bot_left = [
                self.back_center[0] + 10 * cos(self.orientation + radians(90)),
                self.back_center[1] - 10 * sin(self.orientation + radians(90)),
            ]

            
            for i in self.car:
                self.canvas.delete(i)

            self.car = [
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.bot_left[0], self.bot_left[1], fill = "green", width = 2), # Left Vert
                self.canvas.create_line(self.top_right[0], self.top_right[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Right Vert
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.top_right[0], self.top_right[1], fill = "green", width = 2), # Top Hor
                self.canvas.create_line(self.bot_left[0], self.bot_left[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Bot Hor
            ]
            print(self.angular_velocity)
            
        elif self.state == Car.possible_states[4]: # Cowardly left turn.
            pass
        elif self.state == Car.possible_states[5]: # Right turn.
            pass
        elif self.state == Car.possible_states[6]: # Left turn.
            pass
        elif self.state == Car.possible_states[7]: # Right turn + brake.
            pass
        elif self.state == Car.possible_states[8]: # Left turn + brake.
            pass

        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance

        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i] + self.f_braking[i] + self.f_lateral[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass.

        self.acceleration = [i / 10 for i in self.acceleration]

        # Get velocity (v = v + dt * a) in m/s
        for i in range(len(self.velocity)):
            self.velocity[i] += self.acceleration[i]
        
        # Actually move the car.
        for line in self.car:
            self.canvas.move(line, self.velocity[0], -(self.velocity[1]))
        
        # Recalculate the car center coords.
        self.car_centerX = (canvas.coords(self.car[2])[0] + canvas.coords(self.car[2])[2]) / 2
        self.car_centerY = (canvas.coords(self.car[0])[1] + canvas.coords(self.car[0])[3]) / 2
        
        canvas.update()


root = tkinter.Tk()

canvas = tkinter.Canvas(root, width = 1000, height = 1000, bg = "black")
canvas.pack()

ae86 = Car(canvas)
ae86.state = Car.possible_states[1]

for i in range(20):
    ae86.update()
    print()
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Lateral Force:" + str(magnitude(ae86.f_lateral)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")

    ae86.engine_force += 1000 if ae86.engine_force < Car.max_engine_force else 0
    sleep(0.1)

ae86.state = Car.possible_states[3]
print("DRIFT")

for i in range(10):
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

ae86.state = Car.possible_states[1]
while True:
    ae86.update()
    ae86.engine_force += 1000 if ae86.engine_force < Car.max_engine_force else 0
    sleep(0.1)

root.mainloop()
