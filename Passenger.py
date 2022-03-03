import uuid


class Passenger:
    def __init__(self):
        self.passenger_id = uuid.uuid1()
        self.destination = None
        self.profit = 5
