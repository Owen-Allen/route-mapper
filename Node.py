import copy
import math

from Passenger import Passenger


class Node:

    def __init__(self, name='', code=''):
        self.name = name
        self.code = code
        self.pos = (1,1)
        # node, [weight of edge, amount of drivers on edge]
        self.outgoing_edges = {}

        self.original_passengers = []
        self.passengers_list = []

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


    def add_drivers_between_all_nodes_in_path(self, path):
        for i in range(len(path)):
            if path[i] == path[-1]:
                return
            path[i].add_drivers_on_edge_with_node(path[i+1], 1)
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
        self.passengers_list.append(passenger)
        self.original_passengers.append(passenger)

    def get_passenger_amount(self):
        return len(self.passengers_list)

    def reset_passengers(self):
        self.passengers_list = self.original_passengers.copy()

    def get_weight_to_node(self, node):
        for edge_node in self.outgoing_edges:
            if edge_node.code == node.code:
                weight = self.outgoing_edges[edge_node][0]
                if isinstance(weight, int):
                    return weight
                else:
                    drivers_on_path = self.outgoing_edges[edge_node][1] + 1  # include yourself on the path
                    weight_on_path = weight(drivers_on_path)
                    return weight_on_path
        return None


    def get_weight_to_node_without_driver_increase(self, node):
        for edge_node in self.outgoing_edges:
            if edge_node.code == node.code:
                weight = self.outgoing_edges[edge_node][0]
                if isinstance(weight, int):
                    return weight
                else:
                    drivers_on_path = self.outgoing_edges[edge_node][1]
                    weight_on_path = weight(drivers_on_path)
                    return weight_on_path
        return None

    def remove_passenger_by_id(self, passenger_id):
        for passenger in self.passengers_list:
            if passenger.passenger_id == passenger_id:
                self.passengers_list.remove(passenger)

    def remove_passenger(self, passenger_to_remove):
        self.passengers_list.remove(passenger_to_remove)
