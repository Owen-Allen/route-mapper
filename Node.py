import math


class Node:

    def __init__(self, name):
        self.name = name
        # node, [weight of edge, amount of drivers on edge]
        self.outgoing_edges = {}

        # for shortest path
        self.dist = math.inf
        self.prev = None

    def set_drivers_on_edge_with_node(self, name, x):
        for edge_node in self.outgoing_edges:
            if edge_node.name == name:
                self.outgoing_edges[edge_node][1] = x

    def get_edges(self):
        return self.outgoing_edges

    def add_edge_with_constant_weight(self, node, weight):
        self.outgoing_edges[node] = weight

    def add_edge_with_congestion_weight(self, node, func):
        self.outgoing_edges[node] = func

    def print_edge_nodes(self):
        print("outgoing edges for node " + self.name)
        for node in self.outgoing_edges:
            print(node.name)

    def get_weight_to_node(self, name):
        for edge_node in self.outgoing_edges:
            if edge_node.name == name:
                weight = self.outgoing_edges[edge_node][0]
                if isinstance(weight, int):
                    return weight
                else:
                    drivers_on_path = self.outgoing_edges[edge_node][1]
                    return weight(drivers_on_path)
