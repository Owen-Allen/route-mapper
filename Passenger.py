import uuid


class Passenger:
    def __init__(self, profit=5):
        self.passenger_id = uuid.uuid1()
        self.destination = None
        self.profit = profit
