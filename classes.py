import random
from colors import color as clr


# Board class
class Board:
    # The board will be printed with these labels:
    # 0: empty, 1: miss, 2: hit, 3: ship
    labels: dict[int, str] = {
        0: clr.OKBLUE + "." + clr.ENDC,
        1: clr.BOLD + "O" + clr.ENDC,
        2: clr.FAIL + "X" + clr.ENDC,
        3: clr.WARNING + "#" + clr.ENDC,
    }
    types: dict[str, int] = {
        "Destroyer": 2,
        "Submarine": 3,
        "Cruiser": 3,
        "Battleship": 4,
        "Carrier": 5,
    }

    def __init__(self: "Board") -> None:
        """
        Initializes a new instance of the class.

        The __init__ method is called when a new object of the class is created. It initializes the grid attribute as a 10x10 matrix filled with zeros and the ships attribute as an empty list.
        """
        self.grid: list[list[int]] = [[0 for x in range(10)] for y in range(10)]
        self.ships: list[Ship] = []

    def hit(self: "Board", square: tuple[int, int]) -> bool:
        """
        Checks if the guess was a hit and updates the board accordingly.

        Parameters:
        - square (tuple): The coordinates of the square being guessed.

        Returns:
        - bool: True if the guess was a hit, False otherwise.
        """
        gotHit: bool = False
        for ship in self.ships:
            if ship.isHit(square):
                gotHit = True

        if gotHit: # hit
            self.grid[square[0]][square[1]] = 2
            return True
        else: # miss
            self.grid[square[0]][square[1]] = 1
            return False

    def gameOver(self: "Board") -> bool:
        """
        Checks if the game is over.

        Returns:
        - bool: True if all ships are sunk, False otherwise.
        """
        for ship in self.ships:
            if not ship.isSunk(self):
                return False
        return True

    def placeShip(self: "Board", ship: "Ship") -> bool:
        """
        Places a ship on the board.

        Parameters:
        - ship (Ship): The ship to place on the board.

        Returns:
        - True if the ship was successfully placed, False otherwise.
        """
        for s in ship.squares:
            if s[0] < 0 or s[0] > 9 or s[1] < 0 or s[1] > 9: # out of bounds
                return False
            for otherShip in self.ships:
                for otherSquare in otherShip.squares:
                    if s == otherSquare: # overlapping
                        return False
        self.ships.append(ship)
        return True

    def placeShipRandom(self: "Board", shipType: str, triesLeft: int=100) -> bool:
        """
        Places a ship on the board at random coordinates.

        Parameters:
        - ship (Ship): The ship to place on the board.

        Returns:
        - True if the ship was successfully placed, False otherwise.
        """
        ship: "Ship" = Ship([(0, 0) for _ in range(Board.types[shipType])], shipType)

        # Randomly choose the orientation of the ship
        orientation: str = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            x: int = random.randint(0, 9 - len(ship.squares))
            y: int = random.randint(0, 9)
            for i in range(len(ship.squares)):
                ship.squares[i] = (x + i, y)
        else:
            x: int = random.randint(0, 9)
            y: int = random.randint(0, 9 - len(ship.squares))
            for i in range(len(ship.squares)):
                ship.squares[i] = (x, y + i)

        if not self.placeShip(ship) and triesLeft > 0: # try again
            return self.placeShipRandom(shipType, triesLeft - 1)
        elif triesLeft == 0: # give up
            return False
        return True

    # Print the board
    def stringify(self: "Board", selected: tuple|None=None, drawShips: bool=True) -> str:
        """
        Returns a string representation of the board.

        The string representation includes the grid with ships marked as '3' and empty cells marked with their respective labels.
        The grid is formatted with row and column labels.

        Returns:
            str: A string representation of the board.
        """
        # Copy the grid
        numBoard: list[list[int]] = [[i for i in row] for row in self.grid]
        # Mark the ships
        if drawShips:
            for ship in self.ships:
                for s in ship.squares:
                    if numBoard[s[0]][s[1]] != 2:
                        numBoard[s[0]][s[1]] = 3

        # add coordinates
        if selected is not None:
            r,c = selected
            printBoard: str = "  1 2 3 4 5 6 7 8 9 10\n" + clr.ENDC
            for i, row in enumerate(numBoard):
                printBoard += f"{chr(i+65)} "
                for j, cell in enumerate(row):
                    if (i, j) == (r, c):
                        printBoard += f"\b{clr.BOLD+clr.HL}[{Board.labels[cell]}{clr.BOLD+clr.HL}]{clr.ENDC}"
                    else:
                        printBoard += f"{Board.labels[cell]}"
                        # if j+1 != c or r != i:
                        printBoard += " "
                printBoard += "\n"
        else:
            printBoard = "  1 2 3 4 5 6 7 8 9 10\n" + "\n".join(
                [
                    f"{chr(i+65)} "
                    + " ".join([Board.labels[cell] for cell in row])
                    + " "
                    for (i, row) in enumerate(numBoard)
                ]
            )

        return printBoard

    def __str__(self: "Board") -> str:
        return self.stringify(None)


# Ship class
class Ship:
    def __init__(self: "Ship", squares: list[tuple[int,int]], shipType: str) -> None:
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
        self.squares = squares
        self.shipType = shipType

    def isSunk(self: "Ship", board: "Board") -> bool:
        """
        Checks if the ship is sunk.

        Returns:
        - True if all squares of the ship are hit, False otherwise.
        """
        for square in self.squares:
            if board.grid[square[0]][square[1]] != 2:
                return False
        return True

    def isHit(self: "Ship", square: tuple[int, int]) -> bool:
        """
        Checks if a given square is hit.

        Parameters:
        - square: The square to check.

        Returns:
        - True if the square is hit, False otherwise.
        """
        return square in self.squares
