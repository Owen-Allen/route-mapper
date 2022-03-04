class Bus:
    def __init__(self, name='', capacity=50):
        self.name = name
        self.path = []
        self.total_travel_time = 0

        # dict of destinations and amount of passengers for that destination that the bus must travel to
        self.destinations = {}
        # passenger capacity in bus
        self.capacity = capacity
        self.passengers_in_bus = []
        self.total_passengers_picked_up = 0
        self.total_profit_made = 0

    def set_path(self, path):
        self.path = path

    def add_passengers_to_destination(self, node, passenger_amount):
        self.destinations[node] += passenger_amount

    def add_destination(self, node):
        if node not in self.destinations:
            self.destinations[node] = 0

    def is_destination_is_in_path(self, destination):
        return destination in self.path

    def set_total_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time

    def get_total_travel_time(self):
        return self.total_travel_time

    def has_edge(self, first_node, second_node):
        for i in range(len(self.path)):
            if self.path[i].name == self.path[-1].name:
                return False
            if self.path[i].name == first_node.name:
                if self.path[i + 1].name == second_node.name:
                    return True
        return False

    def pickup_passengers_at_node(self, node):
        for passenger in node.passengers_waiting:
            if self.capacity > 0:
                if passenger.destination in self.path:
                    node.remove_passenger(passenger)
                    self.passengers_in_bus.append(passenger)
                    if passenger.destination not in self.destinations.keys():
                        self.add_destination(passenger.destination)
                    self.add_passengers_to_destination(passenger.destination, 1)
                    self.capacity -= 1
                    self.total_passengers_picked_up += 1
                    self.total_profit_made += passenger.profit

    def pickup_passengers_at_node_going_to_farthest_node_in_path(self, node):
        # TODO: get the passengers that want to go farthest (picking up any passengers currently)
        for passenger in node.passengers_waiting:
            if self.capacity > 0:
                if passenger.destination in self.path:
                    node.remove_passenger(passenger)
                    self.passengers_in_bus.append(passenger)
                    self.capacity -= 1
                    self.total_passengers_picked_up += 1
                    self.total_profit_made += passenger.profit

    def drop_off_passengers_at_node(self, node):
        if len(self.passengers_in_bus) > 0:
            for passenger in self.passengers_in_bus:
                if passenger.destination == node:
                    self.passengers_in_bus.remove(passenger)
