import uuid


class Passenger:
    def __init__(self, profit=5):
        self.passenger_id = uuid.uuid1()
        self.destination = None
        self.profit = profit

    def __repr__(self):
        return "Destination: " + self.destination.name

    def __str__(self):
        return "Destination: " + self.destination.name