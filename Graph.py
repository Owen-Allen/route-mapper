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

    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def get_all_graph_edges_with_weight(self):
        edges = []
        for node in self.nodes:
            for edge_node in node.outgoing_edges:
                weight = node.get_weight_to_node(edge_node)
                # node_name = node.name + ' (' + str(node.get_passenger_amount()) + ')'
                edge_to_add = [node.name, edge_node.name, weight]
                edges.append(edge_to_add)
        return edges
    
    def get_node_with_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None