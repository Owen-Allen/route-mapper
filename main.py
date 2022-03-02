import networkx as nx
import numpy as np
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
    busses = []
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    nodeD = Node('D')
    nodeE = Node('E')

    bus1 = Bus("Bus 1")
    bus1.set_path([nodeA, nodeB, nodeC, nodeE])

    bus2 = Bus("Bus 2")
    bus2.set_path([nodeA, nodeD, nodeE])

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
    busses.append(bus1)
    busses.append(bus2)
    return graph, busses


def display_graph(graph):
    graph_display = nx.DiGraph()
    edges = graph.get_all_graph_edges_with_weight()

    # add edges to graph
    graph_display.add_weighted_edges_from(edges)

    # node layout
    # pos = nx.spring_layout(graph_display)
    pos = nx.planar_layout(graph_display)

    nx.draw(graph_display, pos, with_labels=True, font_weight='bold')
    edge_weight = nx.get_edge_attributes(graph_display, 'weight')
    nx.draw_networkx_edge_labels(graph_display, pos, edge_labels=edge_weight)
    plt.show()


def display_new_cost_graph(graph, busses):
    x = np.arange(len(busses))
    y1 = []
    y2 = []
    names = []
    for bus in busses:
        current_cost = calculate_cost_of_path(bus.path)
        bus.set_total_travel_time(current_cost)
        new_path = find_shortest_path(graph, bus)
        new_cost = calculate_cost_of_path(new_path)
        y1.append(current_cost)
        y2.append(new_cost)
        names.append(bus.name)

    width = 0.40

    figure, plot = plt.subplots()

    # plot data in grouped manner of bar type
    current_plot = plot.bar(x - width / 2, y1, width, label='Current path')
    shortest_plot = plot.bar(x + width / 2, y2, width, label='Shortest path')

    plot.set_ylabel('Cost')
    plot.set_xlabel('Busses')
    plot.set_title('Travel Cost for each bus')
    plot.set_xticks(x, names)
    plot.legend()

    plot.bar_label(current_plot)
    plot.bar_label(shortest_plot)

    plt.show()


if __name__ == '__main__':
    graph, busses = construct_graph()
    display_graph(graph)
    display_new_cost_graph(graph, busses)
