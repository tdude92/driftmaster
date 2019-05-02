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

    def __repr__(self):
        return str(self.ID)


class InNode:
    id_counter = 0
    nodes = []

    def __init__(self, value):
        self.ID = InNode.id_counter
        InNode.id_counter += 1
        InNode.nodes.append(self)

        self.connections = []
        self.value = value
    
    def add_connection(self, node_id, weight):
        if str(node_id) in [node.__repr__() for node in OutNode.nodes]:
            self.connections.append((node_id, weight))
            OutNode.nodes[node_id].connections.append((self.ID, weight))
        else:
            raise Exception(str(node_id) + " is an invalid node ID")

    def __repr__(self):
        return str(self.ID)


if __name__ == "__main__":
    from random import randint
    
    out_nodes = [OutNode() for _ in range(2)]
    in_nodes = [InNode(randint(1, 5)) for _ in range(3)]

    for node in in_nodes:
        for outnode in out_nodes:
            node.add_connection(outnode.ID, 2)
    
    for i in in_nodes:
        print(i.value)
    
    for i in out_nodes:
        i.get_value()
        print(i.value)
