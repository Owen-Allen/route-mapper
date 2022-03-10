import math


class Node:

    def __init__(self, name='', id=''):
        self.name = name
        self.id = id
        # node, [weight of edge, amount of drivers on edge]
        self.outgoing_edges = {}

        self.original_passengers = []
        self.passengers_waiting = []

        # for shortest path
        self.dist = math.inf
        self.prev = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def set_drivers_on_edge_with_node(self, edge_node, x):
        if edge_node in self.outgoing_edges.keys():
            self.outgoing_edges[edge_node][1] = x

    def add_drivers_on_edge_with_node(self, edge_node, x):
        """Add a driver to the edge between this node and edge_node
            :param edge_node: the node that has the edge between this node and edge_node
            :param x: the amount of drivers we will increase the edge by
        """
        if edge_node in self.outgoing_edges.keys():
            self.outgoing_edges[edge_node][1] += x

    def reset_drivers_on_edges(self):
        for edge_node in self.outgoing_edges:
            self.outgoing_edges[edge_node][1] = 0

    def get_edges(self):
        return self.outgoing_edges

    def add_edge(self, node, weight_and_driver):
        self.outgoing_edges[node] = weight_and_driver

    def print_edge_nodes(self):
        print("outgoing edges for node " + self.name)
        for node in self.outgoing_edges:
            print(node.name)

    def add_passenger(self, passenger):
        self.passengers_waiting.append(passenger)
        self.original_passengers.append(passenger)

    def get_passenger_amount(self):
        return len(self.passengers_waiting)

    def reset_passengers(self):
        self.passengers_waiting = self.original_passengers

    def get_weight_to_node(self, node):
        for edge_node in self.outgoing_edges:
            if edge_node.name == node.name:
                weight = self.outgoing_edges[edge_node][0]
                if isinstance(weight, int):
                    return weight
                else:
                    drivers_on_path = self.outgoing_edges[edge_node][1]
                    return weight(drivers_on_path)

    def remove_passenger_by_id(self, passenger_id):
        for passenger in self.passengers_waiting:
            if passenger.passenger_id == passenger_id:
                self.passengers_waiting.remove(passenger)

    def remove_passenger(self, passenger_to_remove):
        self.passengers_waiting.remove(passenger_to_remove)
