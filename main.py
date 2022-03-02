import math
import networkx as nx
from matplotlib import pyplot as plt
from Bus import Bus
from Node import Node
from Graph import Graph
from Shortest_path import *


def calculate_cost_of_path(path):
    total_travel_time = 0
    if len(path) > 0:
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            weight_to_add = current_node.get_weight_to_node(next_node.name)
            total_travel_time += weight_to_add
    return total_travel_time


def print_path(path):
    path_to_print = []
    for node in path:
        path_to_print.append(node.name)
    print(path_to_print)


def construct_graph():
    graph = Graph()
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    nodeD = Node('D')
    nodeE = Node('E')

    bus1 = Bus("first")
    bus1.set_path([nodeA, nodeB, nodeC, nodeE])
    # bus1.set_path([nodeA, nodeD, nodeE])

    nodeA.add_edge(nodeB, 10)
    nodeA.add_edge(nodeD, 7)

    nodeD.add_edge(nodeE, 7)

    nodeB.add_edge(nodeC, 10)

    nodeC.add_edge(nodeE, 10)

    graph.add_node(nodeA)
    graph.add_node(nodeB)
    graph.add_node(nodeC)
    graph.add_node(nodeD)
    graph.add_node(nodeE)
    new_path = find_shortest_path(graph, bus1)

    bus1.set_total_travel_time(calculate_cost_of_path(bus1.path))

    if new_path == bus1.path:
        print("bus1 is on shortest path thus this bus satisfies Nash Equilibrium")
    else:
        print("bus1 is not on shortest path thus this bus does not satisfy Nash Equilibrium")
        print("Alternate route is: ")
        print_path(new_path)
        new_cost = calculate_cost_of_path(new_path)
        print("The new cost is " + str(new_cost) + " which is smaller than the original " + str(
            bus1.get_total_travel_time()))
    return graph


def display_graph():
    graph_display = nx.DiGraph()
    graph = construct_graph()
    edges = graph.get_all_graph_edges_with_weight()

    # add edges to graph
    graph_display.add_weighted_edges_from(edges)

    pos = nx.spring_layout(graph_display)
    nx.draw(graph_display, pos, with_labels=True, font_weight='bold')
    edge_weight = nx.get_edge_attributes(graph_display, 'weight')
    nx.draw_networkx_edge_labels(graph_display, pos, edge_labels=edge_weight)
    plt.show()


if __name__ == '__main__':
    display_graph()
