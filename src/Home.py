import math

class Home:

    def __init__(self, index_pair, home_index):
        self.xy_index = index_pair
        self.home_index = home_index


    def distance_to(self, index):
        x_delta = self.xy_index[0] - index[0]
        y_delta = self.xy_index[1] - index[1]
        return math.sqrt(x_delta**2 + y_delta**2)

    def __str__(self):
        return "<" + self.home_index.__str__() + " @ " + "(" + str(self.xy_index[0]) + "," + str(self.xy_index[1]) + ")>"

    def __repr__(self):
        return self.home_index.__str__()

    def __eq__(self, other):
        if self.home_index == other.home_index and self.xy_index == other.xy_index:
            return True
        else:
            return False