import tkinter
from time import sleep
from math import sqrt, sin, cos, atan, radians, pi

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


def direction(td_vector):
    # Return the direction of a 2d vector.
    if magnitude(td_vector) > 0:
        return atan(td_vector[1] / td_vector[0])


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

    max_engine_force = 2000 # N
    mass = 1000 # kg
    wheelbase = 2.4 # m
    steering_angle = radians(45) # radian
    drag_const = 0.39 # Drag constant.
    rr_const = 11.7 # Rolling resistance constant.
    braking_const = mass * 9.8 * 0.9 # Friction = normal force [AKA m * g] * friction coefficient.
    cornering_stiffness = 5000


    def __init__(self, canvas):
        self.canvas = canvas

        # Create the car.
        self.car = [
            self.canvas.create_line(299, 498, 299, 502, fill = "green", width = 2), # Left Vert
            self.canvas.create_line(301, 498, 301, 502, fill = "green", width = 2), # Right Vert
            self.canvas.create_line(299, 498, 301, 498, fill = "red", width = 2), # Top Hor
            self.canvas.create_line(299, 502, 301, 502, fill = "green", width = 2), # Bot Hor
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
        if round(magnitude(self.velocity)) > 0:
            self.slip_angle = abs(direction(self.velocity) - self.orientation)
        else:
            self.slip_angle = 0

        if round(self.slip_angle, 2) == 0:
            self.f_lateral = [0, 0]
        else:
            self.mag_lateral = Car.cornering_stiffness * self.slip_angle
            self.f_lateral = [self.mag_lateral * abs(sin(self.slip_angle)) * -i for i in self.velocity]

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

            self.angular_velocity = pi / 32 # per 1/10 seconds
            self.orientation -= self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]

            self.top_left = [
                self.canvas.coords(self.car[0])[0],
                self.canvas.coords(self.car[0])[1]
            ]
            self.top_right = [
                self.canvas.coords(self.car[0])[2],
                self.canvas.coords(self.car[0])[3]
            ]
            self.bot_left = [
                self.canvas.coords(self.car[1])[0],
                self.canvas.coords(self.car[1])[1]
            ]
            self.bot_right = [
                self.canvas.coords(self.car[1])[2],
                self.canvas.coords(self.car[1])[3]
            ]

            self.coords = [self.top_left, self.top_right, self.bot_left, self.bot_right]

            for i in range(len(self.coords)):
                self.temp_x = self.coords[i][0] - self.car_centerX
                self.temp_y = self.coords[i][1] - self.car_centerY

                self.rotated_x = self.temp_x * cos(self.angular_velocity) - self.temp_y * sin(self.angular_velocity)
                self.rotated_y = self.temp_x * sin(self.angular_velocity) + self.temp_y * cos(self.angular_velocity)

                self.coords[i][0] = self.rotated_x + self.car_centerX
                self.coords[i][1] = self.rotated_y + self.car_centerY
            
            for i in self.car:
                self.canvas.delete(i)

            self.car = [
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.bot_left[0], self.bot_left[1], fill = "green", width = 2), # Left Vert
                self.canvas.create_line(self.top_right[0], self.top_right[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Right Vert
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.top_right[0], self.top_right[1], fill = "red", width = 2), # Top Hor
                self.canvas.create_line(self.bot_left[0], self.bot_left[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Bot Hor
            ]
        elif self.state == Car.possible_states[4]: # Cowardly left turn.
            self.f_traction = [0, 0]
            self.f_braking = [0, 0]

            self.angular_velocity = -pi / 32 # per 1/10 seconds
            self.orientation -= self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]

            self.top_left = [
                self.canvas.coords(self.car[0])[0],
                self.canvas.coords(self.car[0])[1]
            ]
            self.top_right = [
                self.canvas.coords(self.car[0])[2],
                self.canvas.coords(self.car[0])[3]
            ]
            self.bot_left = [
                self.canvas.coords(self.car[1])[0],
                self.canvas.coords(self.car[1])[1]
            ]
            self.bot_right = [
                self.canvas.coords(self.car[1])[2],
                self.canvas.coords(self.car[1])[3]
            ]

            self.coords = [self.top_left, self.top_right, self.bot_left, self.bot_right]

            for i in range(len(self.coords)):
                self.temp_x = self.coords[i][0] - self.car_centerX
                self.temp_y = self.coords[i][1] - self.car_centerY

                self.rotated_x = self.temp_x * cos(self.angular_velocity) - self.temp_y * sin(self.angular_velocity)
                self.rotated_y = self.temp_x * sin(self.angular_velocity) + self.temp_y * cos(self.angular_velocity)

                self.coords[i][0] = self.rotated_x + self.car_centerX
                self.coords[i][1] = self.rotated_y + self.car_centerY
            
            for i in self.car:
                self.canvas.delete(i)

            self.car = [
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.bot_left[0], self.bot_left[1], fill = "green", width = 2), # Left Vert
                self.canvas.create_line(self.top_right[0], self.top_right[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Right Vert
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.top_right[0], self.top_right[1], fill = "red", width = 2), # Top Hor
                self.canvas.create_line(self.bot_left[0], self.bot_left[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Bot Hor
            ]
        elif self.state == Car.possible_states[5]: # Right turn.
            self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
            self.f_braking = [0, 0]

            self.angular_velocity = pi / 32 # per 1/10 seconds
            self.orientation -= self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]

            self.top_left = [
                self.canvas.coords(self.car[0])[0],
                self.canvas.coords(self.car[0])[1]
            ]
            self.top_right = [
                self.canvas.coords(self.car[0])[2],
                self.canvas.coords(self.car[0])[3]
            ]
            self.bot_left = [
                self.canvas.coords(self.car[1])[0],
                self.canvas.coords(self.car[1])[1]
            ]
            self.bot_right = [
                self.canvas.coords(self.car[1])[2],
                self.canvas.coords(self.car[1])[3]
            ]

            self.coords = [self.top_left, self.top_right, self.bot_left, self.bot_right]

            for i in range(len(self.coords)):
                self.temp_x = self.coords[i][0] - self.car_centerX
                self.temp_y = self.coords[i][1] - self.car_centerY

                self.rotated_x = self.temp_x * cos(self.angular_velocity) - self.temp_y * sin(self.angular_velocity)
                self.rotated_y = self.temp_x * sin(self.angular_velocity) + self.temp_y * cos(self.angular_velocity)

                self.coords[i][0] = self.rotated_x + self.car_centerX
                self.coords[i][1] = self.rotated_y + self.car_centerY
            
            for i in self.car:
                self.canvas.delete(i)

            self.car = [
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.bot_left[0], self.bot_left[1], fill = "green", width = 2), # Left Vert
                self.canvas.create_line(self.top_right[0], self.top_right[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Right Vert
                self.canvas.create_line(self.top_left[0], self.top_left[1], self.top_right[0], self.top_right[1], fill = "red", width = 2), # Top Hor
                self.canvas.create_line(self.bot_left[0], self.bot_left[1], self.bot_right[0], self.bot_right[1], fill = "green", width = 2), # Bot Hor
            ]
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

canvas = tkinter.Canvas(root, width = 600, height = 600, bg = "black")
canvas.pack()

ae86 = Car(canvas)
ae86.state = Car.possible_states[1]

for i in range(40):
    ae86.update()
    print()
    print(ae86.u, ae86.velocity)
    print(ae86.orientation, direction(ae86.velocity))
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Lateral Force:" + str(magnitude(ae86.f_lateral)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")

    ae86.engine_force += 1000 if ae86.engine_force < Car.max_engine_force else 0
    sleep(0.1)

ae86.state = Car.possible_states[5]
print("DRIFT")
for i in range(20):
    ae86.update()
    print()
    print(ae86.orientation)
    print(ae86.slip_angle)
    print("lateral force: ", ae86.f_lateral, magnitude(ae86.f_lateral))

    ae86.engine_force -= 100 if ae86.engine_force > 0 else 0
    sleep(0.1)

ae86.state = Car.possible_states[1]
for i in range(40):
    ae86.engine_force = 2000
    ae86.update()
    ae86.engine_force = 2000
    print(ae86.u, ae86.velocity)
    print(ae86.orientation, direction(ae86.velocity))
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Lateral Force:" + str(magnitude(ae86.f_lateral)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")
    print()
    sleep(0.1)

ae86.state = Car.possible_states[4]
print("DRIFT")
for i in range(40):
    ae86.update()
    print()
    print(ae86.orientation)
    print(ae86.slip_angle)
    print(ae86.f_lateral, magnitude(ae86.f_lateral))
    sleep(0.1)

ae86.state = Car.possible_states[1]
for i in range(40000):
    ae86.update()
    print(ae86.u, ae86.velocity)
    print(ae86.orientation, direction(ae86.velocity))
    print("Traction:" + str(magnitude(ae86.f_traction)) + " N")
    print("Braking Force:" + str(magnitude(ae86.f_braking)) + " N")
    print("Drag:" + str(magnitude(ae86.f_drag)) + " N")
    print("Rolling Resistance:" + str(magnitude(ae86.f_rr)) + " N")
    print("Lateral Force:" + str(magnitude(ae86.f_lateral)) + " N")
    print("Acceleration:" + str(magnitude(ae86.acceleration)) + " m/s^2")
    print("Velocity:" + str(magnitude(ae86.velocity)) + " m/s")
    print()
    sleep(0.1)

root.mainloop()
