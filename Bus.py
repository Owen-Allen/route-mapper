class Bus:
    def __init__(self, name='', capacity=50):
        self.name = name
        self.path = []
        self.total_travel_time = 0

        # dict of destinations and amount of passengers for that destination that the bus must travel to
        self.destination = {}
        # passenger capacity in bus
        self.capacity = capacity

    def set_path(self, path):
        self.path = path

    def add_passengers_to_destination(self, node, passenger_amount):
        self.destination[node] += passenger_amount

    def add_destination(self, node):
        if node not in self.destination:
            self.destination[node] = 0

    def is_destination_is_in_path(self, destination):
        return destination in self.path

    def set_total_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time

    def get_total_travel_time(self):
        return self.total_travel_time
