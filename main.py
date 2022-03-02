import math
import networkx as nx
from matplotlib import pyplot as plt

class Bus:
    def __init__(self, name):
        self.name = name
        self.path = []
        self.total_travel_time = 0

    def set_path(self, path):
        self.path = path

    def set_total_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time

    # def calculate_cost_of_path(self):
    #     self.total_travel_time = self.path[0].outgoing_edges



class Node:

    def __init__(self, name):
        self.name = name
        # node, weight of edge
        self.outgoing_edges = {}

        # for shortest path
        self.dist = math.inf
        self.prev = None

    def add_edge(self, node, weight):
        self.outgoing_edges[node] = weight

    def print_edge_nodes(self):
        print("outgoing edges for node " + self.name)
        for node in self.outgoing_edges:
            print(node.name)


class Graph:

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def print_nodes(self):
        for node in self.nodes:
            print(node.name)

    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node


def find_minimum_dist(nodes):
    lowest_dist = math.inf
    lowest_dist_node = None
    for node in nodes:
        if node.dist < lowest_dist:
            lowest_dist_node = node
    return lowest_dist_node


# to see if bus has an alternate route we need to run a shortest path (dijkstra) algorithm to see if its on the
# shortest path or not (Nash Equilibrium)
def shortest_path(graph, source, target):
    for node in graph.nodes:
        node.dist = math.inf
        node.prev = None
    source.dist = 0
    Q = list(graph.get_nodes())
    while Q:
        u = find_minimum_dist(Q)
        Q.remove(u)
        for edge_node_v in u.outgoing_edges:
            if u.dist + u.outgoing_edges[edge_node_v] < edge_node_v.dist:
                edge_node_v.dist = u.dist + u.outgoing_edges[edge_node_v]
                edge_node_v.prev = u
            if edge_node_v == target:
                return


def shortest_path(graph, bus):
    source = bus.path[0]
    target = bus.path[-1]
    for node in graph.nodes:
        node.dist = math.inf
        node.prev = None
    source.dist = 0
    Q = list(graph.get_nodes())
    while Q:
        u = find_minimum_dist(Q)
        Q.remove(u)
        for edge_node_v in u.outgoing_edges:
            if u.dist + u.outgoing_edges[edge_node_v] < edge_node_v.dist:
                edge_node_v.dist = u.dist + u.outgoing_edges[edge_node_v]
                edge_node_v.prev = u
            if edge_node_v == target:
                return


def find_shortest_path(source, target):
    path = []
    if target.dist < math.inf:
        current_node = target
        while current_node.name != source.name:
            path.append(current_node.name)
            current_node = current_node.prev
        path.append(current_node.name)
    return path[::-1]


def find_shortest_path(graph, bus):
    source = bus.path[0]
    target = bus.path[-1]
    path = []
    if target.dist < math.inf:
        current_node = target
        while current_node.name != source.name:
            path.append(current_node.name)
            current_node = current_node.prev
        path.append(current_node.name)
    return path[::-1]


def construct_graph():
    graph = Graph()
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    nodeD = Node('D')
    nodeE = Node('E')

    bus1 = Bus("first")
    bus1.set_path([nodeA, nodeB, nodeC, nodeE])

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
    graph.print_nodes()
    g = graph
    shortest_path(g, bus1)
    new_path = find_shortest_path(graph, bus1)

    if new_path == bus1.path:
        print("bus1 is on shortest path thus this bus satisfies Nash Equilibrium")
    else:
        print("bus1 is not on shortest path thus this bus does not satisfy Nash Equilibrium")
        print("Alternate route is: ")
        print(new_path)
    return graph


def display_graph():
    graph_display = nx.DiGraph()
    edges = []
    graph = construct_graph()
    for node in graph.get_nodes():
        for edge_node in node.outgoing_edges:
            edge_to_add = [node.name, edge_node.name, node.outgoing_edges[edge_node]]
            edges.append(edge_to_add)
    graph_display.add_weighted_edges_from(edges)
    # nx.draw_networkx(graph_display)
    pos = nx.spring_layout(graph_display)
    nx.draw(graph_display, pos, with_labels=True, font_weight='bold')
    edge_weight = nx.get_edge_attributes(graph_display, 'weight')
    nx.draw_networkx_edge_labels(graph_display, pos, edge_labels=edge_weight)
    plt.show()




if __name__ == '__main__':
    display_graph()
