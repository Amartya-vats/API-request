# class to keep track of all partners
# consists of all data like name etc
class Partner:
    def __init__(self, data):
        self.first = data['firstName']
        self.last = data['lastName']
        self.email = data['email']
        self.country = data['country']
        self.dates = data['availableDates']