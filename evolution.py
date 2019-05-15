from math import e, tanh
from random import randint

# Actual nodes stored in class variable. Nodes are then referenced with assigned IDs.

def activation(x):
    # Activation function.
    return tanh(x)


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

    def __init__(self, callback = None):
        # Callback: a function reference that will be called when an outnode has the highest value in its network.
        self.ID = OutNode.id_counter
        OutNode.id_counter += 1
        OutNode.nodes.append(self)

        self.connections = []
        self.value = 0

        self.callback = callback
    
    def get_value(self):
        # Calculate the value of the node based on the weighted sum of the input node
        # values multiplied by the weight.

        # Arguments: None
        # Returns: None
        self.value = 0
        for node in self.connections:
            self.value += InNode.nodes[node[0]].value * node[1]
        self.value = activation(self.value)

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
        self.value = activation(self.bound_to[0]) / 600
    
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
    # A class variable stores every network.
    networks = []

    # An instance of the Network class stores the IDs of all associated nodes.
    def __init__(self):
        Network.networks.append(self)
        self.input_nodes = []
        self.output_nodes = []
    
    def create_input_nodes(self, bound_vars, bias = False):
        # Creates input nodes and appends their IDs to self.input_nodes.
        
        # Arguments:
        #     bound_vars (list/tuple): A list/tuple containing BoundVar instances.
        #                              Used in the creation of InNode instances.
        #     bias (boolean): Determines whether the network has a bias.
        # Returns: None
        for var in bound_vars:
            self.input_nodes.append(InNode(var).ID)
        
        if bias:
            self.input_nodes.append(InNode(BoundVar(600)).ID)
    
    def create_output_nodes(self, callbacks):
        # Creates output nodes
        
        # Arguments:
        #     callbacks (list/tuple): A list/tuple containing function references.
        #                             Used in the creation of OutNode instances.
        # Returns: None
        for function in callbacks:
            self.output_nodes.append(OutNode(function).ID)
    
    def connect(self, weights):
        # Adds the required connections between each of the nodes.

        # Arguments: Two-dimensional list of weights. Each weight is grouped into which input node they're connected to.
        # Returns: None
        for node in range(len(self.input_nodes)):
            for outnode in range(len(self.output_nodes)):
                InNode.nodes[self.input_nodes[node]].add_connection(OutNode.nodes[self.output_nodes[outnode]].ID, weights[node][outnode])

    def update(self):
        # Updates the value of each input node and calculates the resulting effects on the network.

        # Arguments: None
        # Returns: None
        for node in self.input_nodes:
            InNode.nodes[node].value = activation(InNode.nodes[node].bound_to[0]) / 600

        for node in self.output_nodes:
            OutNode.nodes[node].get_value()
        
        self.outputs = [OutNode.nodes[node].value for node in self.output_nodes]
        OutNode.nodes[self.output_nodes[self.outputs.index(max(self.outputs))]].callback()


# Tests
if __name__ == "__main__":
    from time import sleep

    test_network = Network()

    def foo():
        print("cool boi")
    
    def bar():
        print("bar won")

    x = BoundVar(0.5)
    y = BoundVar(0.4)
    z = BoundVar(0.6)
    
    test_network.create_input_nodes([x, y, z])
    test_network.create_output_nodes([foo, bar])

    test_network.connect()
    test_network.update()

    for node in test_network.input_nodes:
        print(InNode.nodes[node].connections)

    for node in test_network.output_nodes:
        print(OutNode.nodes[node].connections)

    while True:
        x.update_val(randint(0, 600))
        y.update_val(randint(0, 600))
        z.update_val(randint(0, 600))

        test_network.update()
        sleep(0.5)
