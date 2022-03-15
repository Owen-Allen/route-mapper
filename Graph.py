class Graph:

    def __init__(self):
        self.nodes = []
        self.passengers = []

    def add_node(self, node):
        self.nodes.append(node)

    def set_nodes(self, nodes):
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes

    def print_nodes(self):
        for node in self.nodes:
            print(node.name)

    def reset_all_nodes(self):
        for node in self.nodes:
            node.reset_passengers()
            node.reset_drivers_on_edges()

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node


    def get_node_with_code(self, code):
        for node in self.nodes:
            if node.code == code:
                return node
        return None

    def get_node(self, name, code):
        for node in self.nodes:
            if node.name == name:
                return node
            elif node.code == code:
                return node
        return None

    def get_all_graph_edges_with_weight(self):
        edges = []
        for node in self.nodes:
            for edge_node in node.outgoing_edges:
                weight = node.get_weight_to_node(edge_node)
                edge_to_add = [node.code, edge_node.code, weight]
                edges.append(edge_to_add)
        return edges

    def get_all_node_locations(self):
        locations = dict()
        for node in self.nodes:
            locations[node.code] = node.pos
        return locations


