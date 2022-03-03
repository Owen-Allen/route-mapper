class Bus:
    def __init__(self, name='', capacity=50):
        self.name = name
        self.path = []
        self.total_travel_time = 0

        # passenger capacity in bus
        self.capacity = capacity

    def set_path(self, path):
        self.path = path

    def set_total_travel_time(self, total_travel_time):
        self.total_travel_time = total_travel_time

    def get_total_travel_time(self):
        return self.total_travel_time