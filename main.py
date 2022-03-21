from random import randrange
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
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

    # # print passengers
    # print("Passenger count: ")
    # for node in nodes:
    #     print(node.name + ': ' + str(node.get_passenger_amount()))

    # generate busses
    bus1 = Bus("Bus 1")
    bus1.set_path([node_a, node_b, node_c, node_e])

    bus2 = Bus("Bus 2")
    bus2.set_path([node_a, node_d, node_e])

    # generate graph
    node_a.add_edge(node_b, [10, 0])
    node_a.add_edge(node_d, [7, 0])
    node_a.add_edge(node_z, [lambda x: x * 1000, 0])

    node_d.add_edge(node_e, [7, 0])

    node_b.add_edge(node_c, [10, 0])

    node_c.add_edge(node_e, [lambda x: x / 2, 0])

    node_z.add_edge(node_c, [lambda x: x * 100, 0])
    node_z.add_edge(node_e, [lambda x: x * 100, 0])

    graph_test.set_nodes(nodes)
    busses_test.append(bus1)
    busses_test.append(bus2)

    return graph_test, busses_test


def display_network(graph_to_display):
    plt.figure(num=None, dpi=70)
    graph_display = nx.DiGraph()
    edges = graph_to_display.get_all_graph_edges_with_weight()

    # add edges to graph
    graph_display.add_weighted_edges_from(edges)

    # node layout
    # pos = nx.planar_layout(graph_display)
    pos = graph_to_display.get_all_node_locations()
    # pos = nx.get_node_attributes(graph_to_display, 'pos')

    nx.draw(graph_display, pos, with_labels=True, font_weight='bold', node_size=2000)
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
        _bus_original.total_travel_time += calculate_cost_of_path(_bus_original.path)

    for _bus_original in bus_list:
        _y1_passengers.append(_bus_original.total_passengers_picked_up)
        _y1_profit.append(_bus_original.total_profit_made)
        _y1_travel_cost.append(_bus_original.total_travel_time)

    reset_all_values(graph_original, bus_list)

    return _y1_passengers, _y1_profit, _y1_travel_cost


def display_company_priority_travel_cost(graph_travel_cost, bus_list):
    _y2_passengers = []
    _y2_profit = []
    _y2_travel_cost = []

    _y1_passengers, _y1_profit, _y1_travel_cost = get_original_bus_graph_details(graph_travel_cost, bus_list)

    # modified bus route
    for _bus_modified in bus_list:
        _start_node = _bus_modified.path[0]
        _current_node = _start_node
        _next_destination = _start_node
        _final_destination = _bus_modified.path[-1]

        while _current_node.code != _final_destination.code:

            _bus_modified.modified_path.append(_current_node)
            if _current_node.code == _next_destination.code:
                _bus_modified.drop_off_passengers_at_node(_current_node)
                _bus_modified.pickup_passengers_at_node_going_to_farthest_node_in_path(_current_node)

            # get the next stop that the bus must go to drop off its passengers
            _next_destination = _bus_modified.find_next_destination(_current_node)

            # get the shortest path to the next stop
            modified_path = find_shortest_path_from_source_to_target(graph_travel_cost, _current_node,
                                                                     _next_destination)

            _current_node.add_drivers_between_all_nodes_in_path(modified_path)

            # travel to next stop
            path_skipped = modified_path[1:len(modified_path) - 1]
            for path_skipped_node in path_skipped:
                _bus_modified.modified_path.append(path_skipped_node)

            next_node_to_travel_to = modified_path[-1]

            # bus arrived at stop
            _current_node = next_node_to_travel_to

        # drop off passengers at final destination of bus
        _bus_modified.drop_off_passengers_at_node(_current_node)
        _bus_modified.modified_path.append(_final_destination)
        _bus_modified.total_travel_time += calculate_cost_of_path(_bus_modified.modified_path)

    update_path_costs(graph_travel_cost, bus_list)

    for _bus_modified in bus_list:
        _y2_passengers.append(_bus_modified.total_passengers_picked_up)
        _y2_profit.append(_bus_modified.total_profit_made)
        _y2_travel_cost.append(_bus_modified.total_travel_time)

    # graph details
    # print('Passengers picked up: ')
    # print(_y1_passengers)
    # print(_y2_passengers)
    # print('Profit made: ')
    # print(_y1_profit)
    # print(_y2_profit)
    # print('Travel Cost: ')
    # print(_y1_travel_cost)
    # print(_y2_travel_cost)

    return _y1_passengers, _y1_profit, _y1_travel_cost, _y2_passengers, _y2_profit, _y2_travel_cost


def display_company_priority_profit(graph_for_profit, bus_list):
    # print("Passenger count: ")
    # for node in graph_travel_cost.nodes:
    #     print(node.name + ': ' + str(node.get_passenger_amount()))

    _y2_passengers = []
    _y2_profit = []
    _y2_travel_cost = []

    _y1_passengers, _y1_profit, _y1_travel_cost = get_original_bus_graph_details(graph_for_profit, bus_list)

    # modified bus route
    for _bus_modified in bus_list:
        _start_node = _bus_modified.path[0]
        _current_node = _start_node
        _next_destination = _start_node
        _final_destination = _bus_modified.path[-1]

        while _current_node.code != _final_destination.code:

            _bus_modified.modified_path.append(_current_node)
            if _current_node.code == _next_destination.code:
                _bus_modified.drop_off_passengers_at_node(_current_node)
                _bus_modified.pickup_passengers_at_node_going_to_closest_node_in_path(_current_node)

            # get the next stop that the bus must go to drop off its passengers
            _next_destination = _bus_modified.find_next_destination(_current_node)

            # get the shortest path to the next stop
            modified_path = find_shortest_path_from_source_to_target(graph_for_profit, _current_node,
                                                                     _next_destination)

            _current_node.add_drivers_between_all_nodes_in_path(modified_path)

            if len(modified_path) < 2:
                print("NO PATH TO NODE " + _next_destination.name + " FROM NODE " + _current_node.name)
            # travel to next stop
            path_skipped = modified_path[1:len(modified_path) - 1]
            for path_skipped_node in path_skipped:
                _bus_modified.modified_path.append(path_skipped_node)

            next_node_to_travel_to = modified_path[-1]

            # bus arrived at stop
            _current_node = next_node_to_travel_to

        # drop off passengers at final destination of bus
        _bus_modified.drop_off_passengers_at_node(_current_node)
        _bus_modified.modified_path.append(_final_destination)
        _bus_modified.total_travel_time += calculate_cost_of_path(_bus_modified.modified_path)

    update_path_costs(graph_for_profit, bus_list)

    for _bus_modified in bus_list:
        _y2_passengers.append(_bus_modified.total_passengers_picked_up)
        _y2_profit.append(_bus_modified.total_profit_made)
        _y2_travel_cost.append(_bus_modified.total_travel_time)

    # graph details
    # print('Passengers picked up: ')
    # print(_y1_passengers)
    # print(_y2_passengers)
    # print('Profit made: ')
    # print(_y1_profit)
    # print(_y2_profit)
    # print('Travel Cost: ')
    # print(_y1_travel_cost)
    # print(_y2_travel_cost)

    return _y1_passengers, _y1_profit, _y1_travel_cost, _y2_passengers, _y2_profit, _y2_travel_cost


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

    figure.tight_layout()
    plt.show()


def reset_all_values(graph_to_reset, bus_list):
    graph_to_reset.reset_all_nodes()
    for bus in bus_list:
        bus.reset()


def display_company_graphs(g, b, y1_p, y2_p, y1_pr, y2_pr, y1_t, y2_t, names):
    # display graphs
    display_network(g)
    x = np.arange(len(b))
    plot_graph(x, y1_p, y2_p, 'Original', 'Modified', 'Passengers picked up', 'Busses',
               'Passengers picked up by busses', names)
    plot_graph(x, y1_pr, y2_pr, 'Original', 'Modified', 'Profit made', 'Busses',
               'Profit made by each bus', names)
    plot_graph(x, y1_t, y2_t, 'Original', 'Modified', 'Cost', 'Busses',
               'Travel Cost by busses', names)


def reset_passengers(graph):
    # reset passengers
    graph.passengers.clear()
    for node in graph.nodes:
        node.passengers_list.clear()
        node.original_passengers.clear()


def print_line_graphs(original_array_for_line_graph, modified_array_for_line_graph, company_priority):
    for i in range(len(busses)):
        y1 = []
        y2 = []
        for j in range(len(original_array_for_line_graph)):
            # reset the arrays
            y1.clear()
            y2.clear()
            for bus_values in original_array_for_line_graph[j]:
                y1.append(bus_values[i])
            for bus_values in modified_array_for_line_graph[j]:
                y2.append(bus_values[i])

            # annotate the points with their values
            for index in range(len(passenger_amounts)):
                plt.annotate(y1[index], (passenger_amounts[index], y1[index]), textcoords="offset points",
                             xytext=(0, 5), ha='center', wrap=True)
                plt.annotate(y2[index], (passenger_amounts[index], y2[index]), textcoords="offset points",
                             xytext=(0, 5), ha='center', wrap=True)

            plt.plot(passenger_amounts, y1, label="Original path", marker='o')
            plt.plot(passenger_amounts, y2, label="Alternate path", marker='o')

            plt.xlabel("Passenger count")

            plt.title(busses[i].name + " for company priority of " + company_priority)
            # giving a y-axis name to my graph
            if j == 0:
                plt.ylabel("Passengers picked up")
            elif j == 1:
                plt.ylabel("Profit made")
            else:
                plt.ylabel("Travel cost")

            plt.legend()
            # plt.grid(True)
            plt.show()


if __name__ == '__main__':
    # graph, busses = construct_test_graph()

    # currently, issues with double values
    # graph, busses = construct_graph_and_buses()
    graph, busses = construct_g_b()

    names = []
    for bus in busses:
        names.append(bus.name)

    # for bus in busses:
    #     if bus.name == "7 St-Laurent":
    #         print_path(bus.path)

    y_original_travel = []
    y_modified_travel = []

    y_original_profit = []
    y_modified_profit = []

    y_original_passenger = []
    y_modified_passenger = []

    y_original_passenger = []
    y_modified_passenger = []

    y_original_travel_for_company_profit = []
    y_modified_travel_for_company_profit = []

    y_original_profit_for_company_profit = []
    y_modified_profit_for_company_profit = []

    y_original_passenger_for_company_profit = []
    y_modified_passenger_for_company_profit = []

    y_original_passenger_for_company_profit = []
    y_modified_passenger_for_company_profit = []

    passenger_amounts = [1000, 10000, 100000]

    for amount in passenger_amounts:
        reset_passengers(graph)

        # generate passengers
        passengers = []
        for i in range(amount):
            p = Passenger()
            # random destination for each passenger
            destination_number = randrange(start=0, stop=len(graph.nodes))
            p.destination = graph.nodes[destination_number]
            if destination_number == 0:
                node_to_wait_at = graph.nodes[1]
            else:
                node_index = destination_number
                while node_index == destination_number:
                    node_index = randrange(start=0, stop=len(graph.nodes))
                node_to_wait_at = graph.nodes[node_index]

            node_to_wait_at.add_passenger(p)
            passengers.append(p)

        graph.passengers = passengers

        _y1_passengers, _y1_profit, _y1_travel_cost, _y2_passengers, _y2_profit, _y2_travel_cost = display_company_priority_travel_cost(
            graph, busses)

        y_original_travel.append(_y1_travel_cost)
        y_modified_travel.append(_y2_travel_cost)

        y_original_profit.append(_y1_profit)
        y_modified_profit.append(_y2_profit)

        y_original_passenger.append(_y1_passengers)
        y_modified_passenger.append(_y2_passengers)

        original_array_for_company_travel = [y_original_passenger, y_original_profit,
                                             y_original_travel]
        modified_array_for_company_travel = [y_modified_passenger, y_modified_profit,
                                             y_modified_travel]
        reset_all_values(graph, busses)

        y1_passengers_company_profit, y1_profit_company_profit, y1_travel_cost_company_profit, y2_passengers_company_profit, \
        y2_profit_company_profit, y2_travel_cost_company_profit = display_company_priority_profit(
            graph, busses)

        y_original_travel_for_company_profit.append(y1_travel_cost_company_profit)
        y_modified_travel_for_company_profit.append(y2_travel_cost_company_profit)

        y_original_profit_for_company_profit.append(y1_profit_company_profit)
        y_modified_profit_for_company_profit.append(y2_profit_company_profit)

        y_original_passenger_for_company_profit.append(y1_passengers_company_profit)
        y_modified_passenger_for_company_profit.append(y2_passengers_company_profit)

        original_array_for_company_profit = [y_original_passenger_for_company_profit,
                                             y_original_profit_for_company_profit, y_original_travel_for_company_profit]
        modified_array_for_company_profit = [y_modified_passenger_for_company_profit,
                                             y_modified_profit_for_company_profit, y_modified_travel_for_company_profit]

        reset_all_values(graph, busses)

    update_path_costs(graph, busses)
    # display_network(graph)
    print_line_graphs(original_array_for_company_travel, modified_array_for_company_travel, "Travel Cost")
    print_line_graphs(original_array_for_company_profit, modified_array_for_company_profit, "Profit")
