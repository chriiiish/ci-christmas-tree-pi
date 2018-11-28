import random

"""This represents a point on the LED strip that corresponds to a build on the build system"""
class BuildPoint:
    id = ""
    location = 0
    direction = 1

    """
    id = string representing the build identifier
    max = the maximum value of the position on the LED string
    """
    def __init__(self, id, max):
        self.id = id
        self.location = random.randint(0, max) # Set a random location on the LED strip
        self.direction = random.choice([-1,1]) # Set a random direction for the point to travel in

    """
    Sets and Returns the next position for this point
    max = the maximum value to return
    """
    def getAndSetNextPosition(self, max):
        self.location += self.direction
        return abs(self.location % (max + 1))
