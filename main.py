from random import randrange
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from Passenger import Passenger
from Shortest_path import *
from parse import *


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
    graph_test = Graph()
    busses_test = []
    nodes = []
    # generate nodes
    node_a = Node('A', '1')
    node_b = Node('B', '2')
    node_c = Node('C', '3')
    node_d = Node('D', '4')
    node_z = Node('Z', '5')
    node_e = Node('E', '6')

    nodes.append(node_a)
    nodes.append(node_b)
    nodes.append(node_c)
    nodes.append(node_d)
    nodes.append(node_e)
    nodes.append(node_z)

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
    graph_test.passengers = passengers

    # print passengers
    print("Passenger count: ")
    for node in nodes:
        print(node.name + ': ' + str(node.get_passenger_amount()))

    # generate busses
    bus1 = Bus("Bus 1")
    bus1.set_path([node_a, node_b, node_c, node_e])

    bus2 = Bus("Bus 2")
    bus2.set_path([node_a, node_d, node_e])

    # generate graph
    node_a.add_edge(node_b, [10, 0])
    node_a.add_edge(node_d, [7, 0])
    node_a.add_edge(node_z, [lambda x: x, 0])

    node_d.add_edge(node_e, [7, 0])

    node_b.add_edge(node_c, [10, 0])

    node_c.add_edge(node_e, [lambda x: x / 2, 0])

    node_z.add_edge(node_c, [lambda x: x, 0])
    node_z.add_edge(node_e, [lambda x: x, 0])

    graph_test.set_nodes(nodes)
    busses_test.append(bus1)
    busses_test.append(bus2)

    return graph_test, busses_test


def display_network(graph_to_display):
    graph_display = nx.DiGraph()
    edges = graph_to_display.get_all_graph_edges_with_weight()

    # add edges to graph
    graph_display.add_weighted_edges_from(edges)

    # node layout
    pos = nx.planar_layout(graph_display)

    nx.draw(graph_display, pos, with_labels=True, font_weight='bold', node_size=1000)
    edge_weight = nx.get_edge_attributes(graph_display, 'weight')
    nx.draw_networkx_edge_labels(graph_display, pos, edge_labels=edge_weight)
    plt.show()


def display_shortest_path_travel_cost_graph(graph_shortest_path, busses_shortest_path):
    x = np.arange(len(busses_shortest_path))
    y1 = []
    y2 = []
    names = []
    for bus in busses_shortest_path:
        current_cost = calculate_cost_of_path(bus.path)
        bus.set_total_travel_time(current_cost)
        new_path = find_shortest_path_from_bus(graph_shortest_path, bus)
        new_cost = calculate_cost_of_path(new_path)
        y1.append(current_cost)
        y2.append(new_cost)
        names.append(bus.name)

    plot_graph(x, y1, y2, 'Current path', 'Shortest path', 'Cost', 'Busses', 'Travel Cost for each bus', names)


def update_path_costs(graph_to_update, bus_list_to_update):
    nodes = graph_to_update.get_nodes()
    for node in nodes:
        node.reset_drivers_on_edges()
        for edge_node in node.outgoing_edges:
            for bus in bus_list_to_update:
                if bus.has_edge(node, edge_node):
                    node.add_drivers_on_edge_with_node(edge_node, 1)


def get_original_bus_graph_details(graph_original, bus_list):
    _y1_passengers = []
    _y1_profit = []
    _y1_travel_cost = []
    update_path_costs(graph_original, bus_list)

    # regular bus route
    for _bus_original in bus_list:
        for path_node in _bus_original.path:
            _bus_original.drop_off_passengers_at_node(path_node)
            _bus_original.pickup_passengers_at_node(path_node)
        _bus_original.total_travel_time = calculate_cost_of_path(_bus_original.path)

    for _bus_original in bus_list:
        _y1_passengers.append(_bus_original.total_passengers_picked_up)
        _y1_profit.append(_bus_original.total_profit_made)
        _y1_travel_cost.append(_bus_original.total_travel_time)
        _bus_original.reset()

    graph_original.reset_all_nodes()

    return _y1_passengers, _y1_profit, _y1_travel_cost


def display_company_priority_travel_cost(graph_travel_cost, bus_list):
    names = []
    for bus in bus_list:
        names.append(bus.name)

    _y2_passengers = []
    _y2_profit = []
    _y2_travel_cost = []

    _y1_passengers, _y1_profit, _y1_travel_cost = get_original_bus_graph_details(graph_travel_cost, bus_list)

    print("Passenger count: ")
    for node in graph_travel_cost.nodes:
        print(node.name + ': ' + str(node.get_passenger_amount()))

    # modified bus route
    for _bus_modified in bus_list:
        _start_node = _bus_modified.path[0]
        _current_node = _start_node
        _next_destination = _start_node
        _final_destination = _bus_modified.path[-1]
        while _current_node.id != _final_destination.id:
            _bus_modified.modified_path.append(_current_node)
            if _current_node.id == _next_destination.id:
                _bus_modified.drop_off_passengers_at_node(_current_node)
                _bus_modified.pickup_passengers_at_node_going_to_farthest_node_in_path(_current_node)

            # get the next stop that the bus must make
            _next_destination = _bus_modified.find_next_destination(_current_node)

            # get the shortest path to the next stop
            modified_path = find_shortest_path_from_source_to_target(graph_travel_cost, _current_node,
                                                                     _next_destination)
            # travel to next stop
            next_node_to_travel_to = modified_path[1]
            _current_node.add_drivers_on_edge_with_node(next_node_to_travel_to, 1)
            # bus arrived at stop
            _current_node = next_node_to_travel_to

        # drop off passengers at final destination of bus
        _bus_modified.drop_off_passengers_at_node(_current_node)
        _bus_modified.modified_path.append(_final_destination)
        _bus_modified.total_travel_time = calculate_cost_of_path(_bus_modified.modified_path)

    update_path_costs(graph_travel_cost, bus_list)

    for _bus_modified in bus_list:
        _y2_passengers.append(_bus_modified.total_passengers_picked_up)
        _y2_profit.append(_bus_modified.total_profit_made)
        _y2_travel_cost.append(_bus_modified.total_travel_time)

    print('Passengers picked up: ')
    print(_y1_passengers)
    print(_y2_passengers)
    print('Profit made: ')
    print(_y1_profit)
    print(_y2_profit)
    print('Travel Cost: ')
    print(_y1_travel_cost)
    print(_y2_travel_cost)

    # display graphs
    display_network(graph_travel_cost)
    x = np.arange(len(bus_list))
    plot_graph(x, _y1_passengers, _y2_passengers, 'Original', 'Modified', 'Passengers picked up', 'Busses',
               'Passengers picked up by busses', names)
    plot_graph(x, _y1_profit, _y2_profit, 'Original', 'Modified', 'Profit made', 'Busses',
               'Profit made by each bus', names)
    plot_graph(x, _y1_travel_cost, _y2_travel_cost, 'Original', 'Modified', 'Cost', 'Busses',
               'Travel Cost by busses', names)


def display_company_priority_profit(graph_for_profit, bus_list):
    names = []
    for bus in bus_list:
        names.append(bus.name)

    y2_passengers = []
    y2_profit = []
    y2_travel_cost = []

    y1_passengers, y1_profit, y1_travel_cost = get_original_bus_graph_details(graph_for_profit, bus_list)

    # modified bus route
    for bus in bus_list:
        start_node = bus.path[0]
        current_node = start_node
        next_destination = start_node
        final_destination = bus.path[-1]
        while current_node.id != final_destination.id:
            bus.modified_path.append(current_node)
            if current_node.id == next_destination.id:
                bus.drop_off_passengers_at_node(current_node)
                bus.pickup_passengers_at_node_going_to_closest_node_in_path(current_node)

            # get the next stop that the bus must make
            next_destination = bus.find_next_destination(current_node)

            # get the shortest path to the next stop
            modified_path = find_shortest_path_from_source_to_target(graph_for_profit, current_node, next_destination)
            # travel to next stop
            next_node_to_travel_to = modified_path[1]
            current_node.add_drivers_on_edge_with_node(next_node_to_travel_to, 1)
            # bus arrived at stop
            current_node = next_node_to_travel_to

        # drop off passengers at final destination of bus
        bus.drop_off_passengers_at_node(current_node)
        bus.modified_path.append(final_destination)
        bus.total_travel_time = calculate_cost_of_path(bus.modified_path)

    update_path_costs(graph_for_profit, bus_list)
    for bus in bus_list:
        y2_passengers.append(bus.total_passengers_picked_up)
        y2_profit.append(bus.total_profit_made)
        y2_travel_cost.append(bus.total_travel_time)

    # display graphs
    display_network(graph_for_profit)

    x = np.arange(len(bus_list))
    plot_graph(x, y1_passengers, y2_passengers, 'Original', 'Modified', 'Passengers picked up', 'Busses',
               'Passengers picked up by busses', names)
    plot_graph(x, y1_profit, y2_profit, 'Original', 'Modified', 'Profit made', 'Busses',
               'Profit made by each bus', names)
    plot_graph(x, y1_travel_cost, y2_travel_cost, 'Original', 'Modified', 'Cost', 'Busses',
               'Travel Cost by busses', names)


def plot_graph(x, y1, y2, label1, label2, y_title, x_title, graph_title, x_names):
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


def reset_all_values(graph_to_reset, bus_list):
    graph_to_reset.reset_all_nodes()
    for bus in busses:
        bus.reset()


if __name__ == '__main__':
    graph, busses = construct_test_graph()

    # currently, issues with double values
    # graph, busses = construct_graph_and_buses()
    display_company_priority_travel_cost(graph, busses)

    reset_all_values(graph, busses)

    display_company_priority_profit(graph, busses)
    # display_company_priority_travel_cost(graph, busses)
    # display_company_priority_travel_cost(graph, busses)
    # _graph_travel_cost, _busses_travel_cost = construct_graph_and_buses()
    # _graph_profit, _busses_profit = construct_graph_and_buses()

    # _graph, _busses = construct_graph_and_buses()
    # display_network(_graph)

    # company priority travel cost
    # display_company_priority_travel_cost(_graph_travel_cost, _busses_travel_cost)

    # company priority profit
    # display_company_priority_profit(_graph_profit, _busses_profit)
    # graph, busses = construct_test_graph()
    # graph, buses = construct_graph_and_buses()

    # for node in graph.get_nodes():
    #     print(f"this is the node: {node} {node.id} and its edges, {node.get_edges()}")

    # display_network(graph)
    # display_company_priority_travel_cost(graph, buses)
    # for node in graph.get_nodes():
    #     print(f"this {node.outgoing_edges}")
    # company priority 1
    # display_company_priority_travel_cost(graph, busses)
