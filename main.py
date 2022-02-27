import math


# to see if bus has an alternate route we need to run a shortest path (dijkstra) algorithm to see if its on the
# shortest path or not (Nash Equilibrium)
class Node:

    def __init__(self, name):
        self.name = name
        # node, weight of edge
        self.outgoing_edges = {}
        self.dist = math.inf
        self.prev = ''

    def add_edge(self, node, weight):
        self.outgoing_edges[node] = weight

    def print_edge_nodes(self):
        print("outgoing edges for node " + self.name)
        for node in self.outgoing_edges:
            print(node.name)

class Graph:

    def __init__(self):
        self.nodes = []

    def print_nodes(self):
        for node in self.nodes:
            print(node.name)

    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

def find_minimum_dist(graph):
    lowest_dist = math.inf
    lowest_dist_node = None
    for node in graph.nodes:
        if node.dist < lowest_dist:
            lowest_dist_node = node
    return lowest_dist_node

def shortest_path(graph, source, target):
    for node in graph.nodes:
        node.dist = math.inf
        node.prev = ''
    source.dist = 0
    Q = graph
    while Q:
        u = find_minimum_dist(Q)
        Q.nodes.remove(u)
        for edge_node_v in u.outgoing_edges:
            if u.dist + u.outgoing_edges[edge_node_v] < edge_node_v.dist:
                edge_node_v.dist = u.dist + u.outgoing_edges[edge_node_v]
                edge_node_v.prev = u.name
            if edge_node_v == target:
                return


# def find_shortest_path(graph, source, target):
#     path = []
#     if target.dist < math.inf:
#         path.append(target.name)
#         current_node_name = target.prev
#         while current_node_name != source.name:
#             path.append(current_node_name)
#             curr_node = graph.find_node_by_name(current_node_name)
#             print(curr_node.name)
#             current_node_name = curr_node.prev
#         path.append(source.name)
#     return path

def construct_graph():
    g = Graph()
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    nodeD = Node('D')
    nodeE = Node('E')

    nodeA.add_edge(nodeB, 10)
    nodeA.add_edge(nodeD, 9)

    nodeD.add_edge(nodeE, 9)

    nodeB.add_edge(nodeC, 10)

    nodeC.add_edge(nodeE, 10)


    g.nodes.append(nodeA)
    g.nodes.append(nodeB)
    g.nodes.append(nodeC)
    g.nodes.append(nodeD)
    g.nodes.append(nodeE)
    shortest_path(g, nodeA, nodeE)
    # print(find_shortest_path(g, nodeA, nodeE))


if __name__ == '__main__':
    construct_graph()
