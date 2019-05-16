import tkinter
import json
from time import sleep
from random import choice
from car import *

n_cars = 10

def update_chances(cars):
    cars = sorted(cars, key = lambda car: car.distance_travelled)
    increment = 100 / n_cars
    chance = increment
    for car in cars:
        car.network.reproduction_chance = chance
        chance += increment


def update_population(cars):
    update_chances(cars)
    sorted_networks = [[], []]

    for network in Network.networks: # Network reproduces.
        if randint(1, 100) <= network.reproduction_chance:
            sorted_networks[0].append(network)
        else: # Network does not reproduce.
            sorted_networks[1].append(network)
    
    if len(sorted_networks[1]) > len(sorted_networks[0]):
        keep = len(sorted_networks[1]) - len(sorted_networks[0])
        keep = [choice(sorted_networks[1]) for _ in range(keep)]
        sorted_networks[1] = keep[:]
    
        network_children = []
        for network in sorted_networks[0]:
            new_weights1 = [[i + randint(1, 5) / 10 for i in row] for row in network.car.weights]
            new_weights2 = [[i - randint(1, 5) / 10 for i in row] for row in network.car.weights]
            network_children.append(Car(canvas, walls, Network(), new_weights1, 26, 198, 31, 208))
            network_children.append(Car(canvas, walls, Network(), new_weights2, 26, 198, 28, 208))
        for network in sorted_networks[1]:
            network_children.append(network.car)
    else:
        sorted_networks[1] = []
        keep = []
        Network.networks = []
        network_children = []

        if len(sorted_networks[0]) > n_cars / 2:
            for _ in range(n_cars // 2):
                keep.append(choice(sorted_networks[0]))
            sorted_networks[0] = keep[:]
        
        for network in sorted_networks[0]:
            new_weights1 = [[i + randint(1, 5) / 10 for i in row] for row in network.car.weights]
            new_weights2 = [[i - randint(1, 5) / 10 for i in row] for row in network.car.weights]
            network_children.append(Car(canvas, walls, Network(), new_weights1, 26, 198, 28, 208))
            network_children.append(Car(canvas, walls, Network(), new_weights2, 26, 198, 28, 208))

    return network_children


root = tkinter.Tk()
canvas = tkinter.Canvas(root, width = 600, height = 600, bg = "black")
canvas.pack()

walls = [
    canvas.create_line(10, 10, 10, 590, fill = "white", width = 2),
    canvas.create_line(590, 10, 590, 500, fill = "white", width = 2),
    canvas.create_line(10, 110, 190, 110, fill = "white", width = 2),
    canvas.create_line(190, 110, 190, 300, fill = "white", width = 2),
    canvas.create_line(190, 300, 490, 300, fill = "white", width = 2),
    canvas.create_line(490, 300, 490, 10, fill = "white", width = 2),
    canvas.create_line(490, 10, 590, 10, fill = "white", width = 2),
    canvas.create_line(10, 590, 590, 500, fill = "white", width = 2), # Inside Lines Start:
    canvas.create_line(40, 250, 40, 560, fill = "white", width = 2),
    canvas.create_line(560, 40, 560, 470, fill = "white", width = 2),
    canvas.create_line(40, 250, 160, 165, fill = "white", width = 2),
    canvas.create_line(160, 165, 160, 330, fill = "white", width = 2),
    canvas.create_line(160, 330, 520, 330, fill = "white", width = 2),
    canvas.create_line(520, 330, 520, 40, fill = "white", width = 2),
    canvas.create_line(520, 40, 560, 40, fill = "white", width = 2),
    canvas.create_line(40, 560, 560, 470, fill = "white", width = 2),
]

cars = []

for _ in range(n_cars):
    weights = [[randint(1, 10) / 10 for i in range(5)] for j in range(7)]
    cars.append(Car(canvas, walls, Network(), weights, 26, 198, 28, 208))

generation_counter = 1
while True:
    for _ in range(600):
        if not (False in [car.is_dead for car in cars]):
            break
        else:
            for car in cars:
                car.update()

    for car in cars:
        if not car.is_dead:
            car.is_dead = True
    
    for car in cars:
        car.update()

    cars = update_population(cars)

    car_distances = sorted(cars, key = lambda car: car.distance_travelled)
    with open("optimal.json", "w") as write_file:
        json.dump(car_distances[len(car_distances) - 1].weights, write_file, indent = 4)
    print("generation:", generation_counter)
    print()
    generation_counter += 1

root.mainloop()