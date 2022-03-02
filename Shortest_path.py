import math


def find_minimum_dist(nodes):
    lowest_dist = math.inf
    lowest_dist_node = None
    for node in nodes:
        if node.dist < lowest_dist:
            lowest_dist_node = node
    return lowest_dist_node


# to see if bus has an alternate route we need to run a shortest path (dijkstra) algorithm to see if its on the
# shortest path or not (Nash Equilibrium)
def dijkstra_shortest_path_from_source_to_target(graph, source, target):
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


def dijkstra_shortest_path_from_bus(graph, bus):
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


def find_shortest_path_from_bus(graph, bus):
    dijkstra_shortest_path_from_bus(graph, bus)
    source = bus.path[0]
    target = bus.path[-1]
    shortest_path = []
    if target.dist < math.inf:
        current_node = target
        while current_node.name != source.name:
            shortest_path.append(current_node)
            current_node = current_node.prev
        shortest_path.append(current_node)
    return shortest_path[::-1]

def find_shortest_path_from_source_to_target(graph, source, target):
    dijkstra_shortest_path_from_source_to_target(graph, source, target)
    shortest_path = []
    if target.dist < math.inf:
        current_node = target
        while current_node.name != source.name:
            shortest_path.append(current_node)
            current_node = current_node.prev
        shortest_path.append(current_node)
    return shortest_path[::-1]



def find_shortest_path_from_source_to_middle_to_target(graph, source, middle, target):
    shortest_path = find_shortest_path_from_source_to_target(graph, source, middle) + find_shortest_path_from_source_to_target(graph, middle, target)
    # remove duplicate nodes from path
    shortest_path = list(dict.fromkeys(shortest_path))
    return shortest_path
