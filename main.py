from random import randrange
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from Bus import Bus
from Node import Node
from Graph import Graph
from Passenger import Passenger
from Shortest_path import *


def calculate_cost_of_path(path):
    total_travel_time = 0
    if len(path) > 0:
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            weight_to_add = current_node.get_weight_to_node(next_node)
            total_travel_time += weight_to_add
    return total_travel_time


def print_path(path):
    path_to_print = []
    for node in path:
        path_to_print.append(node.name)
    print(path_to_print)


def construct_test_graph():
    graph = Graph()
    busses = []
    nodes = []

    # generate nodes
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    nodeD = Node('D')
    nodeE = Node('E')
    nodeZ = Node('Z')

    nodes.append(nodeA)
    nodes.append(nodeB)
    nodes.append(nodeC)
    nodes.append(nodeD)
    nodes.append(nodeE)
    nodes.append(nodeZ)

    # generate passengers
    passengers = []
    for i in range(1000):
        p = Passenger()
        # random destination for each passenger
        destination_number = randrange(start=0, stop=6)
        p.destination = nodes[destination_number]
        if destination_number == 0:
            node_to_wait_at = nodes[1]
        else:
            node_to_wait_at = nodes[randrange(start=0, stop=destination_number)]

        node_to_wait_at.add_passenger(p)
        passengers.append(p)
    graph.passengers = passengers

    # print passengers
    print("Passenger count: ")
    for node in nodes:
        print(node.name + ': ' + str(node.get_passenger_amount()))

    # generate busses
    bus1 = Bus("Bus 1")
    bus1.set_path([nodeA, nodeB, nodeC, nodeE])

    bus2 = Bus("Bus 2")
    bus2.set_path([nodeA, nodeD, nodeE])

    # generate graph
    nodeA.add_edge(nodeB, [10, 0])
    nodeA.add_edge(nodeD, [7, 0])
    nodeA.add_edge(nodeZ,  [lambda x: x, 0])

    nodeD.add_edge(nodeE, [7, 0])

    nodeB.add_edge(nodeC, [10, 0])

    nodeC.add_edge(nodeE, [lambda x: x / 2, 0])

    nodeZ.add_edge(nodeC, [lambda x: x, 0])
    nodeZ.add_edge(nodeE, [lambda x: x, 0])

    graph.set_nodes(nodes)
    busses.append(bus1)
    busses.append(bus2)

    return graph, busses


def display_network(graph):
    graph_display = nx.DiGraph()
    edges = graph.get_all_graph_edges_with_weight()

    # add edges to graph
    graph_display.add_weighted_edges_from(edges)

    # node layout
    pos = nx.planar_layout(graph_display)

    nx.draw(graph_display, pos, with_labels=True, font_weight='bold', node_size=1000)
    edge_weight = nx.get_edge_attributes(graph_display, 'weight')
    nx.draw_networkx_edge_labels(graph_display, pos, edge_labels=edge_weight)
    plt.show()


def display_new_travel_cost_graph(graph, busses):
    x = np.arange(len(busses))
    y1 = []
    y2 = []
    names = []
    for bus in busses:
        current_cost = calculate_cost_of_path(bus.path)
        bus.set_total_travel_time(current_cost)
        new_path = find_shortest_path_from_bus(graph, bus)
        new_cost = calculate_cost_of_path(new_path)
        y1.append(current_cost)
        y2.append(new_cost)
        names.append(bus.name)

    plot_graph(x,y1,y2,'Current path','Shortest path','Cost','Busses','Travel Cost for each bus',names)


def update_path_costs(graph, busses):
    nodes = graph.get_nodes()
    for node in nodes:
        node.reset_drivers_on_edges()
        for edge_node in node.outgoing_edges:
            for bus in busses:
                if bus.has_edge(node, edge_node):
                    node.add_drivers_on_edge_with_node(edge_node, 1)


def display_company_priority_travel_cost(graph, bus_list):
    names = []
    for bus in bus_list:
        names.append(bus.name)
        bus.reset()
    y1_passengers = []
    y2_passengers = []
    y1_profit = []
    y2_profit = []
    y1_travel_cost = []
    y2_travel_cost = []

    update_path_costs(graph, bus_list)

    # regular bus route
    for bus in bus_list:
        for path_node in bus.path:
            bus.drop_off_passengers_at_node(path_node)
            bus.pickup_passengers_at_node(path_node)
        bus.total_travel_time = calculate_cost_of_path(bus.path)

    for bus in bus_list:
        y1_passengers.append(bus.total_passengers_picked_up)
        y1_profit.append(bus.total_profit_made)
        y1_travel_cost.append(bus.total_travel_time)
        bus.reset()

    for node in graph.nodes:
        node.reset_passengers()
        node.reset_drivers_on_edges()

    # modified bus route
    for bus in bus_list:
        start_node = bus.path[0]
        current_node = start_node
        next_destination = start_node
        final_destination = bus.path[-1]
        while current_node.name != final_destination.name:
            bus.modified_path.append(current_node)
            if current_node.name == next_destination.name:
                bus.drop_off_passengers_at_node(current_node)
                bus.pickup_passengers_at_node_going_to_farthest_node_in_path(current_node)

            # get the next stop that the bus must make
            next_destination = bus.find_next_destination()

            # get the shortest path to the next stop
            modified_path = find_shortest_path_from_source_to_target(graph, current_node, next_destination)
            # travel to next stop
            next_node_to_travel_to = modified_path[1]
            current_node.add_drivers_on_edge_with_node(next_node_to_travel_to, 1)
            # bus arrived at stop
            current_node = next_node_to_travel_to

        # drop off passengers at final destination of bus
        bus.drop_off_passengers_at_node(current_node)
        bus.modified_path.append(final_destination)
        bus.total_travel_time = calculate_cost_of_path(bus.modified_path)

    for bus in bus_list:
        y2_passengers.append(bus.total_passengers_picked_up)
        y2_profit.append(bus.total_profit_made)
        y2_travel_cost.append(bus.total_travel_time)
        bus.reset()



    # display graphs
    update_path_costs(graph, bus_list)
    display_network(graph)
    x = np.arange(len(busses))
    plot_graph(x, y1_passengers, y2_passengers, 'Original', 'Modified', 'Passengers picked up', 'Busses',
               'Passengers picked up by busses', names)
    plot_graph(x, y1_profit, y2_profit, 'Original', 'Modified', 'Profit made', 'Busses',
               'Profit made by each bus', names)
    plot_graph(x, y1_travel_cost, y2_travel_cost, 'Original', 'Modified', 'Cost', 'Busses',
               'Travel Cost by busses', names)



def plot_graph(x, y1,y2, label1, label2, y_title, x_title, graph_title, x_names):
    figure, plot = plt.subplots()
    width = 0.40
    # plot data in grouped manner of bar type
    original_plot = plot.bar(x - width / 2, y1, width, label=label1)
    modified_plot = plot.bar(x + width / 2, y2, width, label=label2)

    plot.set_ylabel(y_title)
    plot.set_xlabel(x_title)
    plot.set_title(graph_title)
    plot.set_xticks(x, x_names)
    plot.legend()

    plot.bar_label(original_plot)
    plot.bar_label(modified_plot)

    plt.show()


if __name__ == '__main__':
    graph, busses = construct_test_graph()
    # company priority 1
    display_company_priority_travel_cost(graph, busses)
