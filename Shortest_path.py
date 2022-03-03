import math


def find_minimum_dist(nodes):
    """Find the node with the lowest distance in the graph
                    :param nodes: nodes in the graph
                    :returns: the node with the lowest distance
    """
    lowest_dist = math.inf
    lowest_dist_node = None
    for node in nodes:
        if node.dist < lowest_dist:
            lowest_dist_node = node
    return lowest_dist_node


# to see if bus has an alternate route we need to run a shortest path (dijkstra) algorithm to see if its on the
# shortest path or not (Nash Equilibrium)
def dijkstra_shortest_path_from_source_to_target(graph, source, target):
    """Find the dijkstra shortest path distances from the source node to the target node
                :param graph: graph of the road network
                :param source: starting node
                :param target: destination node
                :returns: shortest path from the source to the target
    """
    for node in graph.nodes:
        node.dist = math.inf
        node.prev = None
    source.dist = 0
    Q = list(graph.get_nodes())
    while Q:
        u = find_minimum_dist(Q)
        if u is None:
            return
        Q.remove(u)
        for edge_node_v in u.outgoing_edges:
            weight = u.get_weight_to_node(edge_node_v.name)
            if u.dist + weight < edge_node_v.dist:
                edge_node_v.dist = u.dist + weight
                edge_node_v.prev = u
            if edge_node_v == target:
                return


def dijkstra_shortest_path_from_bus(graph, bus):
    """Find the dijkstra shortest path distances from the source node to the target node
            :param graph: graph of the road network
            :param bus: the bus that we will be going from the first node in the path to the klast node in the path
            :returns: shortest path for the bus to reach its last node in its path if it exists or do nothing otherwise
    """
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
            weight = u.get_weight_to_node(edge_node_v.name)
            if u.dist + weight < edge_node_v.dist:
                edge_node_v.dist = u.dist + weight
                edge_node_v.prev = u
            if edge_node_v == target:
                return


def find_shortest_path_from_bus(graph, bus):
    """Find the shortest path from the source node by going through all the middle nodes and reaching the target
        :param graph: graph of the road network
        :param bus: the bus that we will be going from the first node in the path to the klast node in the path
        :returns: shortest path for the bus to reach its last node in its path if it exists or empty array otherwise
    """
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
    """Find the shortest path from the source node to the target node
        :param graph: graph of the road network
        :param source: starting node
        :param target: destination node
        :returns: shortest path if it exists or empty array otherwise
    """
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
    """Find the shortest path from the source node by going through the middle node and reaching the target node
        :param graph: graph of the road network
        :param source: starting node
        :param middle: node that the bus must pass through
        :param target: destination node
        :returns: shortest path if it exists or empty array otherwise
    """
    path_to_middle = find_shortest_path_from_source_to_target(graph, source, middle)
    if len(path_to_middle) == 0:
        return []
    path_to_target = find_shortest_path_from_source_to_target(graph, middle, target)
    if len(path_to_target) == 0:
        return []
    shortest_path = path_to_middle + path_to_target[1:]

    return shortest_path


def find_shortest_path_from_source_to_middle_nodes_to_target(graph, source, middle_nodes, target):
    """Find the shortest path from the source node by going through all the middle nodes and reaching the target node
        :param graph: graph of the road network
        :param source: starting node
        :param middle_nodes: array of nodes that the bus must pass through
        :param target: destination node
        :returns: shortest path if it exists or empty array otherwise
    """
    if len(middle_nodes) > 0:
        path_to_first = find_shortest_path_from_source_to_target(graph, source, middle_nodes[0])
        if len(path_to_first) == 0:
            return []
        shortest_path = path_to_first
        for i in range(len(middle_nodes)):
            current_node = middle_nodes[i]
            if current_node == middle_nodes[-1]:
                path_to_target = find_shortest_path_from_source_to_target(graph, current_node, target)
                if len(path_to_target) == 0:
                    return []
                shortest_path = shortest_path + path_to_target[1:]
                break
            next_node = middle_nodes[i + 1]
            path_to_next_node = find_shortest_path_from_source_to_target(graph, current_node, next_node)
            if len(path_to_next_node) == 0:
                return []
            shortest_path = shortest_path + path_to_next_node[1:]

    return shortest_path
