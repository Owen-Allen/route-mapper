class Bus:
    def __init__(self, name='', capacity=50, color="blue"):
        self.name = name
        self.path = []
        self.total_travel_time = 0
        self.modified_path = []
        # dict of destinations and amount of passengers for that destination that the bus must travel to
        self.destinations = {}
        # passenger capacity in bus
        self.original_capacity = capacity
        self.capacity = capacity
        self.total_passengers_picked_up = 0
        self.total_profit_made = 0
        self.average_stop_time = 10
        self.color = color

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def print_bus(self):
        print(self.name + ": ")
        print("Destinations: ", end="")
        print(self.destinations)
        print("total_passengers: " + str(self.total_passengers_picked_up))
        print("total_profit: " + str(self.total_profit_made))
        print("total_travel: " + str(self.total_travel_time))
        print("path: ", end="")
        print(self.path)

    def set_path(self, path):
        self.path = path

    def add_node_to_path(self, node):
        self.path.append(node)

    def add_passengers_to_destination(self, node, passenger):
        self.destinations[node].append(passenger)

    def add_destination(self, node):
        if node not in self.destinations:
            self.destinations[node] = []

    def is_destination_is_in_path(self, destination):
        return destination in self.path

    def set_total_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time

    def get_total_travel_time(self):
        return self.total_travel_time

    def has_edge(self, first_node, second_node):
        path_to_use = self.path
        if len(self.modified_path) > 0:
            path_to_use = self.modified_path
        for i in range(len(path_to_use)):
            if path_to_use[i].code == path_to_use[-1].code:
                return False
            if path_to_use[i].code == first_node.code:
                if path_to_use[i + 1].code == second_node.code:
                    return True
        return False

    def reset(self):
        self.total_travel_time = 0
        self.destinations = {}
        # passenger capacity in bus
        self.capacity = self.original_capacity
        self.total_passengers_picked_up = 0
        self.total_profit_made = 0
        self.modified_path = []

    def pickup_passengers_at_node(self, node):
        if node.code == self.path[-1].code:
            return
        index = self.path.index(node)
        whats_left_in_path = self.path[index + 1:]
        for passenger in node.passengers_list:
            if self.capacity > 0:
                if passenger.destination in whats_left_in_path:
                    node.remove_passenger(passenger)
                    if passenger.destination not in self.destinations.keys():
                        self.add_destination(passenger.destination)
                    self.add_passengers_to_destination(passenger.destination, passenger)
                    self.capacity -= 1
                    self.total_passengers_picked_up += 1
                    self.total_profit_made += passenger.profit

    def pickup_passengers_at_node_going_to_farthest_node_in_path(self, node):
        index = self.path.index(node)
        whats_left_in_path = self.path[index + 1:]
        for path_node in reversed(whats_left_in_path):
            for passenger in node.passengers_list:
                if self.capacity > 0:
                    if passenger.destination.code == path_node.code:
                        node.remove_passenger(passenger)
                        if passenger.destination not in self.destinations.keys():
                            self.add_destination(passenger.destination)
                        self.add_passengers_to_destination(passenger.destination, passenger)
                        self.capacity -= 1
                        self.total_passengers_picked_up += 1
                        self.total_profit_made += passenger.profit

    def pickup_passengers_at_node_going_to_closest_node_in_path(self, node):
        index = self.path.index(node)
        whats_left_in_path = self.path[index + 1:]
        for path_node in whats_left_in_path:
            for passenger in node.passengers_list:
                if self.capacity > 0:
                    if passenger.destination.code == path_node.code:
                        node.remove_passenger(passenger)
                        if passenger.destination not in self.destinations.keys():
                            self.add_destination(passenger.destination)
                        self.add_passengers_to_destination(passenger.destination, passenger)
                        self.capacity -= 1
                        self.total_passengers_picked_up += 1
                        self.total_profit_made += passenger.profit

    def drop_off_passengers_at_node(self, node):

        if len(self.destinations.keys()) > 0:
            self.total_travel_time += self.average_stop_time
            if node in self.destinations.keys():
                passengers_for_node = self.destinations[node]
                amount_of_passengers = len(passengers_for_node)
                self.capacity += amount_of_passengers
                del self.destinations[node]

    def find_next_destination(self, current_node):
        # find next nearest destination
        if len(self.destinations.keys()) > 0:
            for i in range(len(self.path)):
                next_node = self.get_next_node_in_path(self.path[i])
                if next_node in self.destinations.keys():
                    return next_node
        else:
            return self.get_next_node_in_path(current_node)
        #     for i in range(len(self.path)):
        #         if self.path[i] in self.destinations.keys():
        #             return self.path[i]
        #
        #     # new_list = sorted(self.destinations.keys(), key=lambda x: x.code)
        #     # return new_list[0]
        # else:
        #     print('here')
        #     return self.get_next_node_in_path(current_node)

    def get_next_node_in_path(self, current_node):
        if current_node == self.path[-1]:
            return current_node
        for i in range(len(self.path)):
            if self.path[i].code == current_node.code:
                return self.path[i + 1]

    def travel_to(self, start_node, end_node):
        weight = start_node.get_weight_to_node(end_node)
        self.total_travel_time += weight

    def get_destinations(self):
        return self.destinations
