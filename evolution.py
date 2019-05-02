from math import e
from random import randint

# Actual nodes stored in class variable. Nodes are then referenced with assigned IDs.

def sigmoid(x):
    return 1 / (1 + e ** -x)


class OutNode:
    id_counter = 0
    nodes = []

    def __init__(self):
        self.ID = OutNode.id_counter
        OutNode.id_counter += 1
        OutNode.nodes.append(self)

        self.connections = []
        self.value = 0
    
    def get_value(self):
        self.value = 0
        for node in self.connections:
            self.value += InNode.nodes[node[0]].value * node[1]
        self.value = sigmoid(self.value)

    def __repr__(self):
        return str(self.ID)


class InNode:
    id_counter = 0
    nodes = []

    def __init__(self, boundto_var):
        self.ID = InNode.id_counter
        InNode.id_counter += 1
        InNode.nodes.append(self)

        self.connections = []
        self.value = 0
        self.bound_to = boundto_var # This is the variable that the node is bound to.
    
    def add_connection(self, node_id, weight):
        if str(node_id) in [node.__repr__() for node in OutNode.nodes]:
            self.connections.append((node_id, weight))
            OutNode.nodes[node_id].connections.append((self.ID, weight))
        else:
            pass
            #raise Exception(str(node_id) + " is an invalid node ID")

    def __repr__(self):
        return str(self.ID)


class Network:
    def __init__(self):
        self.input_nodes = []
        self.output_nodes = []
        self.output = None
    
    def connect(self):
        for node in self.input_nodes:
            for outnode in self.output_nodes:
                InNode.nodes[node].add_connection(OutNode.nodes[outnode].ID, randint(1, 10) / 10)

    def update(self):
        for node in self.input_nodes:
            InNode.nodes[node].value = InNode.nodes[node].bound_to

        for node in self.output_nodes:
            OutNode.nodes[node].get_value()
        
        self.output = max([OutNode.nodes[node].value for node in self.output_nodes])


if __name__ == "__main__":
    test_network = Network()

    x = 0.5
    y = 0.4
    z = 0.6
    
    test_network.input_nodes.append(InNode(x).ID)
    test_network.input_nodes.append(InNode(y).ID)
    test_network.input_nodes.append(InNode(z).ID)

    test_network.output_nodes.append(OutNode().ID)
    test_network.output_nodes.append(OutNode().ID)

    test_network.connect()
    test_network.update()

    print(test_network.output)
