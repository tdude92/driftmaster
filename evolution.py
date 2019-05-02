from math import e
from random import randint

# Actual nodes stored in class variable. Nodes are then referenced with assigned IDs.

def sigmoid(x):
    # Activation function.
    return 1 / (1 + e ** -x)


class BoundVar:
    # Creates an object that links to the value of an input node.
    def __init__(self, var):
        # List references are stored in variables.
        # If another variable is given the value of self.var,
        # changes to self.var will change the other variable.
        self.var = [var]
    
    def update_val(self, val):
        # Updates the value of self.var
        # Cannot reassign self.var because that would create a new list that
        # is not linked to the value of the input node.

        # Arguments: New value for the variable.
        # Returns: None.
        self.var.pop(0)
        self.var.append(val)

    def __repr__(self):
        return str(self.var[0])


class OutNode:
    # All instances are stored in a class variable.
    # The node's ID is equal to its index in the class variable.
    # The id_counter variable contains the ID of the next instance that will be created
    id_counter = 0
    nodes = []

    def __init__(self):
        self.ID = OutNode.id_counter
        OutNode.id_counter += 1
        OutNode.nodes.append(self)

        self.connections = []
        self.value = 0
    
    def get_value(self):
        # Calculate the value of the node based on the weighted sum of the input node
        # values multiplied by the weight.

        # Arguments: None
        # Returns: None
        self.value = 0
        for node in self.connections:
            self.value += InNode.nodes[node[0]].value * node[1]
        self.value = sigmoid(self.value)

    def __repr__(self):
        return str(self.ID)


class InNode:
    # All instances are stored in a class variable.
    # The node's ID is equal to its index in the class variable.
    # The id_counter variable contains the ID of the next instance that will be created
    id_counter = 0
    nodes = []

    def __init__(self, boundto_var):
        self.ID = InNode.id_counter
        InNode.id_counter += 1
        InNode.nodes.append(self)

        self.connections = []
        self.bound_to = boundto_var.var # This is the variable that the node is bound to.
        self.value = self.bound_to[0]
    
    def add_connection(self, node_id, weight):
        # Appends a tuple in the form (node_id, weight) to the connections instance variable of the
        # input node and the connected node.

        # Arguments: None
        # Returns: None
        if str(node_id) in [node.__repr__() for node in OutNode.nodes]:
            self.connections.append((node_id, weight))
            OutNode.nodes[node_id].connections.append((self.ID, weight))
        else:
            # The connection cannot exist if the connected node does not exist.
            raise Exception(str(node_id) + " is an invalid node ID")

    def __repr__(self):
        return str(self.ID)


class Network:
    # An instance of the Network class stores the IDs of all associated nodes.
    def __init__(self):
        self.input_nodes = []
        self.output_nodes = []
        self.output = None
    
    def connect(self):
        # Adds the required connections between each of the nodes.

        # Arguments: None
        # Returns: None
        for node in self.input_nodes:
            for outnode in self.output_nodes:
                InNode.nodes[node].add_connection(OutNode.nodes[outnode].ID, randint(1, 10) / 10)

    def update(self):
        # Updates the value of each input node and calculates the resulting effects on the network.

        # Arguments: None
        # Returns: None
        for node in self.input_nodes:
            InNode.nodes[node].value = InNode.nodes[node].bound_to[0]

        for node in self.output_nodes:
            OutNode.nodes[node].get_value()
        
        self.output = max([OutNode.nodes[node].value for node in self.output_nodes])


if __name__ == "__main__":
    test_network = Network()

    x = BoundVar(0.5)
    y = BoundVar(0.4)
    z = BoundVar(0.6)
    
    test_network.input_nodes.append(InNode(x).ID)
    test_network.input_nodes.append(InNode(y).ID)
    test_network.input_nodes.append(InNode(z).ID)

    test_network.output_nodes.append(OutNode().ID)
    test_network.output_nodes.append(OutNode().ID)

    test_network.connect()
    test_network.update()

    print(test_network.output)

    x.update_val(0.6)
    y.update_val(0.5)
    z.update_val(4)

    test_network.update()

    print(test_network.output)
