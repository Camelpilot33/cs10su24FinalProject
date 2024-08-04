from pynput import keyboard
import os
import sys
import classes
import solver
import colors

isWindows = sys.platform.startswith("win")
if not isWindows:  # Mac needs clear instead of cls to clear the console

    def clearConsole():
        """
        Clears the console screen.
        """
        os.system("clear")

else:

    def clearConsole():
        """
        Clears the console screen.
        """
        os.system("cls")


# Global Variables
"""
actual modes:
0: instruction
1: Setup 2p
2: Game 2p
3: Setup AI
4: Game AI
config:
10: select game mode
"""
gameMode = 0
instructions = [
    [
        "1. The game board is a 10 * 10 grid.",
        "2. You first choose where to place the ship.",
        "3. You then need to guess where enemy ships are.",
        "4. Enter coordinates to fire at that location.",
        "5. The game will tell you if you hit or missed a ship.",
        "6. Sink all enemy ships to win the game.",
        "Good luck, Captain!",
    ],
    0,
    0,
]
players = [classes.Board(), classes.Board()]
turn = 0
gm1TurnPart = 0  # whether sensitive data is shown
gm3TurnPart = 0
gm2TurnPart = 0
gm4TurnPart = 0
cursor = [0, 0]  # row, col

def gameOver(ai=False) -> bool:
    """
    Checks if the game is over by checking if all ships on either board are sunk.

    Args:
        p1Board: The first player's board.
        p2Board: The second player's board.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    p1Board = players[0]
    p2Board = players[1]
    # check if player 1 lost
    p1Lost = all([ship.isSunk(p1Board) for ship in p1Board.ships])
    # check if player 2 lost
    p2Lost=all([ship.isSunk(p2Board) for ship in p2Board.ships])
    if p1Lost or p2Lost:
        clearConsole()
        print(f"\r{colors.color.BOLD+colors.color.OKGREEN}Game Over!, {'Player 1' if p1Lost else 'Player 2'} wins!{colors.color.ENDC}\n\n")
        print("Player 1's Board:")
        print(p1Board.stringify())
        if ai:
            print("\n\nAI's Board:")
        else:
            print("Player 2's Board:")
        print(p2Board.stringify())
    return p1Lost or p2Lost


def printInstr():
    """
    Prints the instruction string at the current index in the instructions list.
    Adjusts the spacing based on the desired length of the string.
    Updates the length of the current instruction string in the instructions list.
    """
    # String to print
    string = instructions[0][instructions[1]] + " " * 5
    length = len(string)
    # Clear the line, print the string, and fill the rest with spaces (overwrite previous string)
    print(
        f"\r{colors.color.BOLD}{colors.color.OKBLUE}{string}{colors.color.ENDC}{' '*(max([len(i) for i in instructions[0]])-length)}",
        end="",
        flush=True,
    )
    # Update the length of the current instruction string
    instructions[2] = len(instructions[0][instructions[1]])


def select_game_mode(key):
    global gameMode
    if key.char == "1":
        gameMode = 1
        print(f"Selected 2-player mode")
    elif key.char == "2":
        gameMode = 3
        setupAI()
        print(f"Selected AI mode")
    return True


def setupAI():
    global players
    players[1] = classes.Board()
    shipsLeft = 5
    while shipsLeft > 0:
        nextShip = list(classes.Board.types.keys())[5 - shipsLeft]
        nextShipLength = classes.Board.types[nextShip]
        ship = classes.Ship([(0, 0) for i in range(nextShipLength)], nextShip)
        players[1].placeShipRandom(nextShip)
        shipsLeft -= 1
    return True


def handle_gm0(key):
    """
    Handles the key events for game mode 0.

    Parameters:
    - key: The key event to handle.

    Returns:
    - True if the program should continue handling key events.
    - False if the program should stop handling key events.

    Key Events:
    - If the key is 'right' or 'space', increments the instruction index and checks if the game should start.
    - If the key is 'left', decrements the instruction index and prints the instruction.
    - If the key is 'q' or 'esc', stops handling key events.

    """
    global gameMode
    # Cycle forward
    if key == keyboard.Key.right or key == keyboard.Key.space:
        instructions[1] += 1
        if instructions[1] >= len(instructions[0]):  # go to next game mode
            # print("\r\nStarting the game...  (press any key to continue)\n")
            print(
                "\r\nPress 1 if you want to play against another player, 2 if you want to play against an AI"
            )
            gameMode = 10
            return True
        printInstr()
    # Go back
    elif key == keyboard.Key.left:
        if instructions[1] == 0:
            return True
        instructions[1] = (instructions[1] - 1) % len(instructions[0])
        printInstr()
    # None of the tested keys were pressed
    return True

# setup modes
def handle_gm1_2p(key):
    """
    Handles the game logic for players in game mode 1 (placement).

    Args:
        key: The key pressed by the player.

    Returns:
        bool: True if the game logic is successfully handled, False otherwise (exits).
    """

    global gameMode
    global turn
    global gm1TurnPart
    global cursor
    # Cycle forward
    shipsLeft = 5 - len(players[turn].ships)

    if shipsLeft == 0:
        clearConsole()
        print("\rAll ships placed!\nPress any key to start the game.")
        gameMode = 2
        return True

    if gm1TurnPart == 0:
        clearConsole()
        print(
            f"\rPlayer {turn+1}: ({shipsLeft} ships left)... {colors.color.BOLD}{colors.color.WARNING}(Only continue if it is your turn){colors.color.ENDC}\n"
        )
        gm1TurnPart = 1
        return True
    if gm1TurnPart == 1:
        clearConsole()
        nextShip = list(classes.Board.types.keys())[shipsLeft - 1]
        nextShipLength = classes.Board.types[nextShip]
        # Movement
        if (
            key == keyboard.Key.up
            or key == keyboard.Key.down
            or key == keyboard.Key.left
            or key == keyboard.Key.right
        ):
            if key == keyboard.Key.up:
                cursor[0] = (cursor[0] - 1) % 10
            elif key == keyboard.Key.down:
                cursor[0] = (cursor[0] + 1) % 10
            elif key == keyboard.Key.left:
                cursor[1] = (cursor[1] - 1) % 10
            elif key == keyboard.Key.right:
                cursor[1] = (cursor[1] + 1) % 10
        # Orientation
        elif key == keyboard.KeyCode.from_char(
            "h"
        ) or key == keyboard.KeyCode.from_char("v"):
            # Place the ship
            ship = classes.Ship([(0, 0) for i in range(nextShipLength)], nextShip)
            if key == keyboard.KeyCode.from_char("h"):
                for i in range(nextShipLength):
                    ship.squares[i] = (cursor[0], cursor[1] + i)
            else:
                for i in range(nextShipLength):
                    ship.squares[i] = (cursor[0] + i, cursor[1])

            # Check if the ship can be placed
            if players[turn].placeShip(ship):

                # Place the ship
                # players[turn].placeShip(cursor, nextShip, orientation)
                # Update the game state
                gm1TurnPart = 0
                turn = (turn + 1) % 2
                print("\rShip placed!\nPlease pass the computer to the next player.\n")
                # reset cursor
                cursor = [0, 0]
                return True
            else:
                print(
                    f"\r{colors.color.FAIL}!! Invalid ship placement. Try again.{colors.color.ENDC}\n"
                )
        print(
            f"\rYou have to place the {nextShip} ship (length {colors.color.BOLD}{colors.color.WARNING}{nextShipLength}{colors.color.ENDC}).\nUse {colors.color.BOLD}{colors.color.WARNING}Arrow Keys{colors.color.ENDC} to move the cursor, {colors.color.BOLD}{colors.color.WARNING}'h' / 'v'{colors.color.ENDC} to place the ship.\nIt will place the ship at your cursor, oriented down or right\n"
        )
        print(players[turn].stringify(cursor))
        # gm1TurnPart = 0
        # turn = (turn + 1) % 2
        # return True
    # None of the tested keys were pressed
    return True


def handle_gm3_AI(key):
    """
    Handles the game logic for players in game mode 3 (placement).

    Args:
        key: The key pressed by the player.

    Returns:
        bool: True if the game logic is successfully handled, False otherwise (exits).
    """
    global gameMode
    global gm3TurnPart
    global cursor
    global turn
    # Cycle forward
    turn = 0
    shipsLeft = 5 - len(players[turn].ships)
    gm3TurnPart = 1
    if shipsLeft == 0:
        clearConsole()
        print("\rAll ships placed!\nPress any key to start the game.")
        gameMode = 4
        return True

    if gm3TurnPart == 1:
        clearConsole()
        nextShip = list(classes.Board.types.keys())[shipsLeft - 1]
        nextShipLength = classes.Board.types[nextShip]
        # Movement
        if (
            key == keyboard.Key.up
            or key == keyboard.Key.down
            or key == keyboard.Key.left
            or key == keyboard.Key.right
        ):
            if key == keyboard.Key.up:
                cursor[0] = (cursor[0] - 1) % 10
            elif key == keyboard.Key.down:
                cursor[0] = (cursor[0] + 1) % 10
            elif key == keyboard.Key.left:
                cursor[1] = (cursor[1] - 1) % 10
            elif key == keyboard.Key.right:
                cursor[1] = (cursor[1] + 1) % 10
        # Orientation
        elif key == keyboard.KeyCode.from_char(
            "h"
        ) or key == keyboard.KeyCode.from_char("v"):
            # Place the ship
            ship = classes.Ship([(0, 0) for i in range(nextShipLength)], nextShip)
            if key == keyboard.KeyCode.from_char("h"):
                for i in range(nextShipLength):
                    ship.squares[i] = (cursor[0], cursor[1] + i)
            else:
                for i in range(nextShipLength):
                    ship.squares[i] = (cursor[0] + i, cursor[1])

            # Check if the ship can be placed
            if players[turn].placeShip(ship):

                # Place the ship
                # players[turn].placeShip(cursor, nextShip, orientation)
                print("Ship placed!")
                # Update the game state
                # reset cursor
                cursor = [0, 0]
                return True
            else:
                print(colors.color.FAIL+"\r!! Invalid ship placement. Try again.\n")
        print(
            f"\rYou have to place the {nextShip} ship (length {nextShipLength}).\nUse Arrow keys to move the cursor, h/v to place the ship.\nIt will place the ship at your cursor, oriented down or right\n"
        )
        print(players[turn].stringify(cursor))
        # gm1TurnPart = 0
        # turn = (turn + 1) % 2
        # return True
    # None of the tested keys were pressed
    return True

# game modes
def handle_gm2_2p(key):

    if gameOver():
        return False

    global gameMode
    global cursor
    global turn
    global gm2TurnPart
    clearConsole()
    if key == keyboard.Key.enter and gm2TurnPart == 1:
        # Fire
        if players[(turn + 1) % 2].grid[cursor[0]][cursor[1]] != 0:
            print("\rBad input! Press any key to continue.")
            gm2TurnPart = 0
            return True
        board = players[(turn + 1) % 2]
        sunkShips = set([ship for ship in board.ships if ship.isSunk(board)])
        result = players[(turn + 1) % 2].hit(tuple(cursor))
        if result == True:
            sunkThisTurn = (
                set([ship for ship in board.ships if ship.isSunk(board)]) - sunkShips
            )
            print(
                f"\r{colors.color.FAIL}Hit! {'You sunk the '+colors.color.WARNING+sunkThisTurn.pop().shipType+'!' if sunkThisTurn else ''}{colors.color.ENDC}\n"
            )
        elif result == False:
            print(colors.color.OKGREEN + "\rMiss!" + colors.color.ENDC)
        # Update the game state
        turn = (turn + 1) % 2
        gm2TurnPart = 0
        return True
    # Movement
    if (
        key == keyboard.Key.up
        or key == keyboard.Key.down
        or key == keyboard.Key.left
        or key == keyboard.Key.right
    ):
        if key == keyboard.Key.up:
            cursor[0] = (cursor[0] - 1) % 10
        elif key == keyboard.Key.down:
            cursor[0] = (cursor[0] + 1) % 10
        elif key == keyboard.Key.left:
            cursor[1] = (cursor[1] - 1) % 10
        elif key == keyboard.Key.right:
            cursor[1] = (cursor[1] + 1) % 10
    print(
        f"\rPlayer {turn+1}: {colors.color.BOLD}{colors.color.WARNING}Firing...{colors.color.ENDC}\n"
    )
    print("\rUse Arrow keys to move the cursor, Enter to fire\n")

    gm2TurnPart = 1
    print(players[(turn + 1) % 2].stringify(cursor, False))


def handle_gm4_AI(key):
    """
    Handles the game logic for the AI player in game mode 4.

    Args:
        key: The key input from the user.

    Returns:
        True if the game state is updated successfully, False otherwise.
    """

    if gameOver(True):
        return False

    global gameMode
    global cursor
    global turn
    global gm4TurnPart
    clearConsole()
    player_board = players[0]
    ai_board = players[1]

    if turn % 2 == 0:  # HUMAN
        if key == keyboard.Key.enter and gm4TurnPart == 1:
            # Fire
            if ai_board.grid[cursor[0]][cursor[1]] != 0:
                print("\rBad input! Press any key to continue.")
                gm4TurnPart = 0
                return True
            board = ai_board
            sunkShips = set([ship for ship in board.ships if ship.isSunk(board)])
            result = ai_board.hit(tuple(cursor))
            if result == True:
                sunkThisTurn = (
                    set([ship for ship in board.ships if ship.isSunk(board)])
                    - sunkShips
                )
                print(
                    f"\r{colors.color.FAIL}Hit! {'You sunk the '+colors.color.WARNING+sunkThisTurn.pop().shipType+'!' if sunkThisTurn else ''}{colors.color.ENDC}\n"
                )
            elif result == False:
                print("\rMiss!")
            turn = (turn + 1) % 2
            return True
        if (
            key == keyboard.Key.up
            or key == keyboard.Key.down
            or key == keyboard.Key.left
            or key == keyboard.Key.right
        ):
            if key == keyboard.Key.up:
                cursor[0] = (cursor[0] - 1) % 10
            elif key == keyboard.Key.down:
                cursor[0] = (cursor[0] + 1) % 10
            elif key == keyboard.Key.left:
                cursor[1] = (cursor[1] - 1) % 10
            elif key == keyboard.Key.right:
                cursor[1] = (cursor[1] + 1) % 10
        print("\rUse Arrow keys to move the cursor, Enter to fire\n")
        # Update the game state
    else:  # AI
        print("\rAI's Turn! (This might take a few seconds...)\n")
        square_freq = solver.solve_battleship(player_board)
        max_freq = 0
        target = (0, 0)
        for i in range(10):
            for j in range(10):
                if square_freq[i][j] > max_freq:
                    max_freq = square_freq[i][j]
                    target = (i, j)
        result = player_board.hit(target)
        row, col = target
        rowLetter = chr(row + 65)
        print(f"\rThe AI fired at {rowLetter}{col + 1}")
        board = player_board
        sunkShips = set([ship for ship in board.ships if ship.isSunk(board)])
        if result == True:
            sunkThisTurn = (
                set([ship for ship in board.ships if ship.isSunk(board)]) - sunkShips
            )
            print(
                f"\r{colors.color.FAIL}Hit! {'The AI sunk the '+colors.color.WARNING+sunkThisTurn.pop().shipType+'!' if sunkThisTurn else ''}{colors.color.ENDC}\n"
            )
        elif result == False:
            print(colors.color.OKGREEN + "\rMiss!" + colors.color.ENDC)
        print(player_board.stringify())
        turn = (turn + 1) % 2
        gm4TurnPart = 0
        return True

    gm4TurnPart = 1
    print(players[(turn + 1) % 2].stringify(cursor, False))


def on_press(key):
    """
    Handles the key press event.

    Parameters:
    - key: The key that was pressed.

    Returns:
    - False: If the key is 'q' or the escape key (keyboard.Key.esc).
    """
    if (hasattr(key, "char") and key.char.lower() == "q") or key == keyboard.Key.esc:
        return False

    global gameMode

    try:
        if gameMode == 0:  # Instructions
            return handle_gm0(key)
        elif gameMode == 1:  # Setup 2p
            return handle_gm1_2p(key)
        elif gameMode == 2:  # Game 2p
            return handle_gm2_2p(key)
        elif gameMode == 3:  # Setup AI
            return handle_gm3_AI(key)
        elif gameMode == 4:  # Game AI
            return handle_gm4_AI(key)
        elif gameMode == 10:  # Select game mode
            return select_game_mode(key)
        else:
            print("\rGame mode " + str(gameMode) + " not impl yet. press q to quit")
    except AttributeError:  # Bad key pressed
        pass # do nothing


def welcome():
    """
    Displays a welcome message and instructions for the game.
    Returns:
        str: The string 'quit' if the user presses 'Q' to quit the game.
    """
    clearConsole()

    ascii_art = (
        r"""
     ____        _   _   _         _____ _     _        
    |  _ \      | | | | | |       / ____| |   (_)
    | |_) | __ _| |_| |_| | ___  | (___ | |__  _ _ __
    |  _ < / _` | __| __| |/ _ \  \___ \| '_ \| | '_ \ 
    | |_) | (_| | |_| |_| |  __/  ____) | | | | | |_) |
    |____/ \__,_|\__|\__|_|\___| |_____/|_| |_|_| .__/
                                                | |
         """+colors.color.OKCYAN+colors.color.BOLD+"By Samuel, Peizhuo, and Robin"+colors.color.ENDC+"          |_|"
        + "\n" * 2
    )

    print(ascii_art)
    print(
        "Right or Space to cycle through the options\nLeft to go back, q or Esc to quit\nThis window handles all your keys, so it might disable other windows\n"
    )
    printInstr()


def main():
    welcome()
    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        listener.join()


if __name__ == "__main__":
    main()
