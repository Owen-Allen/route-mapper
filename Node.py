import math


class Node:

    def __init__(self, name):
        self.name = name
        # node, weight of edge
        self.outgoing_edges = {}

        # for shortest path
        self.dist = math.inf
        self.prev = None

    def get_edges(self):
        return self.outgoing_edges

    def add_edge(self, node, weight):
        self.outgoing_edges[node] = weight

    def print_edge_nodes(self):
        print("outgoing edges for node " + self.name)
        for node in self.outgoing_edges:
            print(node.name)

    def get_weight_to_node(self, name):
        for edge_node in self.outgoing_edges:
            if edge_node.name == name:
                weight = self.outgoing_edges[edge_node]
                return weight
