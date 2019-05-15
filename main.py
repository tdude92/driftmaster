import tkinter
import json
from time import sleep
from random import choice
from car import *

n_cars = 20

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
            new_weights1 = [[i + randint(1, 10) / 10 for i in row] for row in network.car.weights]
            new_weights2 = [[i - randint(1, 10) / 10 for i in row] for row in network.car.weights]
            network_children.append(Car(canvas, walls, Network(), new_weights1, 24, 498, 26, 502))
            network_children.append(Car(canvas, walls, Network(), new_weights2, 24, 498, 26, 502))
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
            new_weights1 = [[i + randint(1, 10) / 10 for i in row] for row in network.car.weights]
            new_weights2 = [[i - randint(1, 10) / 10 for i in row] for row in network.car.weights]
            network_children.append(Car(canvas, walls, Network(), new_weights1, 24, 498, 26, 502))
            network_children.append(Car(canvas, walls, Network(), new_weights2, 24, 498, 26, 502))
    return network_children


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

cars = []

for _ in range(n_cars):
    weights = [[8.100000000000003, 7.999999999999996, 9.4, 5.999999999999998, 6.4999999999999964], [0.5000000000000002, 11.899999999999997, 4.499999999999999, 8.500000000000005, 10.000000000000002], [10.7, 11.400000000000002, 4.999999999999999, 2.2, 5.299999999999999], [2.0999999999999996, 1.8, 0.7999999999999997, 2.899999999999999, 5.6000000000000005], [8.299999999999997, 16.50000000000001, 2.4999999999999996, 8.399999999999999, -2.6], [1.1999999999999997, 7.100000000000001, 11.900000000000002, 13.0, 6.100000000000004], [-1.5999999999999996, 3.1000000000000005, 5.600000000000002, 3.1000000000000005, 1.9]]
    cars.append(Car(canvas, walls, Network(), weights, 24, 498, 26, 502))

generation_counter = 1
while True:
    for _ in range(600):
        if not (False in [car.is_dead for car in cars]):
            break
        else:
            for car in cars:
                car.update()
        sleep(0.1)

    for car in cars:
        if not car.is_dead:
            car.is_dead = True
            car.update()

    cars = update_population(cars)
    car_distances = sorted(cars, key = lambda car: car.distance_travelled)
    with open("optimal.json", "w") as write_file:
        json.dump(car_distances[len(car_distances) - 1].weights, write_file)
    print("Generation:", generation_counter)
    print(car_distances[len(car_distances) - 1].weights)
    generation_counter += 1

root.mainloop()
