import random

# class for each players' board
class Board:
    # The board will be printed with these labels:
    # 0: empty, 1: miss, 2: hit, 3: ship
    labels = {0: ".", 1: "O", 2: "X", 3: "#"}
    types = {"Destroyer": 2, "Submarine": 3, "Cruiser": 3, "Battleship": 4, "Carrier": 5}

    def __init__(self):
        """
        Initializes a new instance of the class.

        The __init__ method is called when a new object of the class is created. It initializes the grid attribute as a 10x10 matrix filled with zeros and the ships attribute as an empty list.
        """
        self.grid = [[0 for x in range(10)] for y in range(10)]
        self.ships = []

    def hit(self, square):
        """
        Checks if the guess was a hit and updates the board accordingly.

        Parameters:
        - square (tuple): The coordinates of the square being guessed.

        Returns:
        - bool: True if the guess was a hit, False otherwise.
        """
        gotHit = False
        for ship in self.ships:
            if ship.isHit(square):
                gotHit = True

        if gotHit:
            self.grid[square[0]][square[1]] = 2
            return True
        else:
            self.grid[square[0]][square[1]] = 1
            return False
    
    def gameOver(self):
        """
        Checks if the game is over.

        Returns:
        - bool: True if all ships are sunk, False otherwise.
        """
        for ship in self.ships:
            if not ship.isSunk(self):
                return False
        return True
    
    def placeShip(self, ship):
        """
        Places a ship on the board.

        Parameters:
        - ship (Ship): The ship to place on the board.

        Returns:
        - True if the ship was successfully placed, False otherwise.
        """
        for s in ship.squares:
            if s[0] < 0 or s[0] > 9 or s[1] < 0 or s[1] > 9:
                return False
            for otherShip in self.ships:
                for otherSquare in otherShip.squares:
                    if s == otherSquare:
                        return False 
        self.ships.append(ship)
        return True

    def placeShipRandom(self, shipType, triesLeft=100):
        """
        Places a ship on the board at random coordinates.

        Parameters:
        - ship (Ship): The ship to place on the board.

        Returns:
        - True if the ship was successfully placed, False otherwise.
        """
        ship = Ship([(0, 0) for i in range(Board.types[shipType])], shipType)

        # Randomly choose the orientation of the ship
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            x = random.randint(0, 9 - len(ship.squares))
            y = random.randint(0, 9)
            for i in range(len(ship.squares)):
                ship.squares[i] = (x + i, y)
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 9 - len(ship.squares))
            for i in range(len(ship.squares)):
                ship.squares[i] = (x, y + i)

        if not self.placeShip(ship) and triesLeft > 0:
            return self.placeShipRandom(shipType, triesLeft - 1)
        elif triesLeft == 0:
            return False
        return True
        

    # Print the board
    def __str__(self):
        """
        Returns a string representation of the board.

        The string representation includes the grid with ships marked as '3' and empty cells marked with their respective labels.
        The grid is formatted with row and column labels.

        Returns:
            str: A string representation of the board.
        """
        # Copy the grid
        printBoard = [[i for i in row] for row in self.grid]
        # Mark the ships
        for ship in self.ships:
            for s in ship.squares:
                if printBoard[s[0]][s[1]] != 2:
                    printBoard[s[0]][s[1]] = 3

        # add coordinates
        printBoard = "  1 2 3 4 5 6 7 8 9 10\n" + "\n".join(
            [
                f"{chr(i+65)} " + " ".join([Board.labels[cell] for cell in row])
                for (i, row) in enumerate(printBoard)
            ]
        )

        return printBoard


# Ship class
class Ship:
    def __init__(self, squares, shipType):
        """
        Initializes a Ship object.

        Parameters:
        - squares (list of tuples): The list of squares occupied by the ship.
        - shipType (string): The type of the ship.

        Attributes:
        - squares (list of tuples): The list of squares occupied by the ship.
        - sunk (bool): Indicates whether the ship is sunk or not.
        - shipType (string): The type of the ship.
        """
        self.squares = squares  # list of tuples
        self.shipType = shipType  # string

    def isSunk(self, board):
        """
        Checks if the ship is sunk.

        Returns:
        - True if all squares of the ship are hit, False otherwise.
        """
        for square in self.squares:
            if board.grid[square[0]][square[1]] != 2:
                return False
        return True

    
    def isHit(self, square):
        """
        Checks if a given square is hit.

        Parameters:
        - square: The square to check.

        Returns:
        - True if the square is hit, False otherwise.
        """
        return square in self.squares


# # Tests
# board = Board()
# ship = Ship([(1, 1), (1, 2), (1, 3)], "Destroyer")
# ship1 = Ship([(4, 2), (4, 3), (4, 4), (4, 5)], "Battleship")
# print(board.placeShip(ship))
# print(board.placeShip(ship1))
# print(board.placeShipRandom("Carrier"))
# print(board.gameOver())
# board.hit((1, 1))
# board.hit((1, 2))
# board.hit((1, 3))
# print(board.gameOver())
# print(board)
