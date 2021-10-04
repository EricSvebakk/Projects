

class Cell:

    # The Cell class-object is dead when first called
    def __init__(self):
        self._alive = False

    # The Cell is represented by te alive-variable
    def __repr__(self):
        if self._alive:
            return "O"
        else:
            return "."

    # A method for setting the Cell to alive
    def alive(self):
        self._alive = True

    # A method for setting the Cell to dead
    def dead(self):
        self._alive = False

    # A method for checking the current state of the Cell
    def status(self):
        return self._alive

