# class for each players' board
class Board:
    size = 10

    # Set up the board with an empty grid, no ships
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.ships = []

    # Hit handling method
    def hit(square):
        # Check if the guess was a hit
        gotHit = False
        for ship in self.ships:
            if ship.isHit(square):
                gotHit = True
        # Update the board
        if gotHit:
            self.grid[square[0]][square[1]] = 2
        else:
            self.grid[square[0]][square[1]] = 1


# Ship class
class Ship:
    # Set up the ship
    def __init__(self, squares, shipType):
        self.squares = squares  # list of tuples
        self.sunk = False  # bool
        self.shipType = shipType  # string

    # check if guess was a hit
    def isHit(self, square):
        return square in self.squares
