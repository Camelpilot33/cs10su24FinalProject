# class for each players' board
class Board:
    # The board will be printed with these labels:
    # 0: empty, 1: miss, 2: hit, 3: ship
    labels = {0: ".", 1: "O", 2: "X", 3: "#"}

    # Set up the board with an empty grid, no ships
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.ships = []

    # Hit handling method: returns True if a ship was hit, False otherwise
    def hit(self, square):
        # Check if the guess was a hit
        gotHit = False
        for ship in self.ships:
            if ship.isHit(square):
                gotHit = True
        # Update the board
        if gotHit:
            self.grid[square[0]][square[1]] = 2
            return True
        else:
            self.grid[square[0]][square[1]] = 1
            return False

    # Print the board
    def __str__(self):
        # Copy the grid
        printBoard = [[i for i in row] for row in self.grid]
        # Mark the ships
        for ship in self.ships:
            for s in ship.squares:
                if printBoard[s[0]][s[1]] != 2:
                    printBoard[s[0]][s[1]] = 3

        printBoard = "  1 2 3 4 5 6 7 8 9 10\n" + "\n".join(
            [
                f"{chr(i+65)} " + " ".join([Board.labels[cell] for cell in row])
                for (i, row) in enumerate(printBoard)
            ]
        )

        return printBoard


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


# Test
board = Board()
ship = Ship([(1, 1), (1, 2), (1, 3)], "Destroyer")
ship1 = Ship([(4, 2), (4, 3), (4, 4), (4, 5)], "Battleship")
board.ships.append(ship)
board.ships.append(ship1)
board.hit((1, 1))
board.hit((4, 4))
board.hit((2, 6))
print(board)
