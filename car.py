import tkinter
from math import sqrt, sin, cos, atan, radians, pi

def magnitude(vector):
    # Take a list/tuple that represents a vector and return its magnitude.
    return sqrt(sum([i ** 2 for i in vector]))


def direction(td_vector):
    # Take a 2d vector (list with two elements) and return the angle of the vector.
    if magnitude(td_vector) > 0:
        return atan(td_vector[1] / td_vector[0])

# These functions are used to check if line segments intersect.
def orientation(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
def intersect(a, b, c, d):
        return orientation(a,c,d) != orientation(b,c,d) and orientation(a,b,c) != orientation(a,b,d)

class Car:
    possible_states = (
        "do_nothing",
        "gas",
        "brake",
        "turn_right",
        "turn_left",
    )

    max_engine_force = 2000 # N
    mass = 1000 # kg
    wheelbase = 2.4 # m
    steering_angle = radians(45) # radian
    drag_const = 0.39 # Drag constant.
    rr_const = 11.7 # Rolling resistance constant.
    braking_const = mass * 9.8 * 0.9 # Friction = normal force [AKA m * g] * friction coefficient.


    def __init__(self, canvas, track_walls, x0, y0, x1, y1):
        self.canvas = canvas
        self.walls = track_walls

        # Create the car.
        self.car = [
            self.canvas.create_line(x0, y0, x0, y1, fill = "green", width = 2), # Left Vert
            self.canvas.create_line(x1, y0, x1, y1, fill = "green", width = 2), # Right Vert
            self.canvas.create_line(x0, y0, x1, y0, fill = "red", width = 2), # Top Hor
            self.canvas.create_line(x0, y1, x1, y1, fill = "green", width = 2), # Bot Hor
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
        self.calculate_vision()


        # Forces and physics stuff.
        self.f_traction = [i * self.engine_force for i in self.u] # self.u * Car.engine_force
        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance
        self.f_braking = [0, 0] # direction unit vector * braking force
        self.f_centripetal = [0, 0]
        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i] + self.f_centripetal[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass
        

    def calculate_vision(self):
        # Vision.
        self.vision = [
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation),
                self.car_centerY - 600*sin(self.orientation),
                fill = "red",
                width = 2
            )], # Front
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation - radians(25)),
                self.car_centerY - 600*sin(self.orientation - radians(25)),
                fill = "red",
                width = 2
            )], # Front Right 25 degrees
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation + radians(25)),
                self.car_centerY - 600*sin(self.orientation + radians(25)),
                fill = "red",
                width = 2
            )], # Front Left 25 Degrees
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation - pi/2),
                self.car_centerY - 600*sin(self.orientation - pi/2),
                fill = "red",
                width = 2
            )], # Right
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation + pi/2),
                self.car_centerY - 600*sin(self.orientation + pi/2),
                fill = "red",
                width = 2
            )], # Left
            [self.canvas.create_line(
                self.car_centerX,
                self.car_centerY,
                self.car_centerX + 600*cos(self.orientation + pi),
                self.car_centerY - 600*sin(self.orientation + pi),
                fill = "red",
                width = 2
            )] # Back
        ]

        for line in range(len(self.vision)):
            self.vision_line = self.canvas.coords(self.vision[line][0])
            for wall in self.walls:
                self.wall_coords = self.canvas.coords(wall)

                self.v1 = [
                    (self.vision_line[0], self.vision_line[1]),
                    (self.vision_line[2], self.vision_line[3])
                ]
                self.w1 = [
                    (self.wall_coords[0], self.wall_coords[1]),
                    (self.wall_coords[2], self.wall_coords[3])
                ]

                if intersect(self.v1[0], self.v1[1], self.w1[0], self.w1[1]):
                    if self.car_centerX - self.vision_line[2] == 0 and self.wall_coords[0] - self.wall_coords[2] == 0:
                        continue
                    elif self.car_centerX - self.vision_line[2] == 0: # m1 is 1/0
                        self.x = self.vision_line[0]

                        self.m2 = (self.wall_coords[1] - self.wall_coords[3]) / (self.wall_coords[0] - self.wall_coords[2])
                        self.b2 = self.wall_coords[1] - self.m2 * self.wall_coords[0]

                        self.y = self.m2 * self.x + self.b2
                    elif self.wall_coords[0] - self.wall_coords[2] == 0: # m2 is 1/0
                        self.x = self.wall_coords[0]

                        self.m1 = (self.car_centerY - self.vision_line[3]) / (self.car_centerX - self.vision_line[2])
                        self.b1 = self.vision_line[1] - self.m1 * self.vision_line[0]

                        self.y = self.m1 * self.x + self.b1
                    else:
                        self.m1 = (self.car_centerY - self.vision_line[3]) / (self.car_centerX - self.vision_line[2])
                        self.m2 = (self.wall_coords[1] - self.wall_coords[3]) / (self.wall_coords[0] - self.wall_coords[2])

                        self.b1 = self.vision_line[1] - self.m1 * self.vision_line[0]
                        self.b2 = self.wall_coords[1] - self.m2 * self.wall_coords[0]

                        try:
                            self.x = (self.b2 - self.b1) / (self.m1 - self.m2)
                        except ZeroDivisionError:
                            continue
                        self.y = self.m1 * self.x + self.b1

                    self.vision[line].append(
                        self.canvas.create_line(self.car_centerX, self.car_centerY, self.x, self.y, fill = "red", width = 2)
                    )
        
        for line_list in self.vision:
            for _ in range(len(line_list) - 1):
                self.temp_line_coords = [self.canvas.coords(line) for line in line_list]
                self.line_lengths = [sqrt((line[3] - line[1]) ** 2 + (line[2] - line[0]) ** 2) for line in self.temp_line_coords]
                self.canvas.delete(line_list[self.line_lengths.index(max(self.line_lengths))])
                line_list.pop(self.line_lengths.index(max(self.line_lengths)))
                self.line_lengths.pop(self.line_lengths.index(max(self.line_lengths)))
        
        self.vision = [i[0] for i in self.vision]
    
    
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
        elif self.state == Car.possible_states[3]: # Right turn.
            self.f_traction = [i * self.engine_force for i in self.u]
            self.f_braking = [0, 0]

            self.turning_radius = Car.wheelbase / sin(Car.steering_angle)
            self.angular_velocity = magnitude(self.velocity) / self.turning_radius / 10 # radians/ms
            self.orientation -= self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]
            self.velocity = [
                magnitude(self.velocity) * cos(self.orientation),
                magnitude(self.velocity) * sin(self.orientation)
            ]

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
        elif self.state == Car.possible_states[4]: # Left turn.
            self.f_traction = [i * self.engine_force for i in self.u]
            self.f_braking = [0, 0]

            self.turning_radius = Car.wheelbase / sin(Car.steering_angle)
            self.angular_velocity = -magnitude(self.velocity) / self.turning_radius / 10 # radians/ms
            self.orientation -= self.angular_velocity
            self.u = [cos(self.orientation), sin(self.orientation)]
            self.velocity = [
                magnitude(self.velocity) * cos(self.orientation),
                magnitude(self.velocity) * sin(self.orientation)
            ]

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

        self.f_drag = [i * -Car.drag_const * magnitude(self.velocity) for i in self.velocity] # drag_const * acceleration * |acceleration|
        self.f_rr = [i * -Car.rr_const for i in self.velocity] # velocity * -rolling resistance

        self.acceleration = [(self.f_traction[i] + self.f_drag[i] + self.f_rr[i] + self.f_braking[i] + self.f_centripetal[i]) / Car.mass for i in range(2)] # Vector sum of f_traction, f_drag, f_rr divided by mass.

        self.acceleration = [i / 10 for i in self.acceleration]

        # Get velocity (v = v + dt * a) in m/s
        for i in range(len(self.velocity)):
            self.velocity[i] += self.acceleration[i]
        
        # Actually move the car.
        for line in self.car:
            self.canvas.move(line, self.velocity[0], -(self.velocity[1]))
        
        # Recalculate the car center coords.
        self.car_centerX = (self.canvas.coords(self.car[2])[0] + self.canvas.coords(self.car[2])[2]) / 2
        self.car_centerY = (self.canvas.coords(self.car[0])[1] + self.canvas.coords(self.car[0])[3]) / 2

        for line in self.vision:
            self.canvas.delete(line)
        self.calculate_vision()
        
        self.canvas.update()


# Tests
if __name__ == "__main__":
    from time import sleep
    from random import randint

    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width = 600, height = 600, bg = "black")
    canvas.pack()

    test_car = Car(canvas)

    test_car.engine_force = 2000
    for i in range(500):
        test_car.state = Car.possible_states[randint(0, 4)]
        print(test_car.state)
        for i in range(10):
            test_car.update()
            sleep(0.1)
    
    root.mainloop()
