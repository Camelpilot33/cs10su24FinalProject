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
cursor = [0, 0]  # r,c


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
            print("\r\nPress 1 if you want to play against another player, 2 if you want to play against an AI")
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

def select_game_mode(key):
    global gameMode
    if key.char == '1':
        gameMode = 1
        print(f"Selected 2-player mode")
    elif key.char == '2':
        gameMode = 3
        print(f"Selected AI mode")
    return True

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
                print(f"\r{colors.color.FAIL}!! Invalid ship placement. Try again.{colors.color.ENDC}\n")
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
    Handles the game logic for players in game mode 2 (placement).

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
    turn = 1
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
        elif key == keyboard.KeyCode.from_char("h") or key == keyboard.KeyCode.from_char("v"):
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
                print("\r!! Invalid ship placement. Try again.\n")
        print(
            f"\rYou have to place the {nextShip} ship (length {nextShipLength}).\nUse Arrow keys to move the cursor, h/v to place the ship.\nIt will place the ship at your cursor, oriented down or right\n"
        )
        print(players[turn].stringify(cursor))
        # gm1TurnPart = 0
        # turn = (turn + 1) % 2
        # return True
    # None of the tested keys were pressed
    return True

def handle_gm2_2p(key):
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
            sunkThisTurn = set([ship for ship in board.ships if ship.isSunk(board)]) - sunkShips
            print(f"\rHit! {'You sunk the '+colors.color.WARNING+sunkThisTurn.pop().shipType+"!" if sunkThisTurn else ''}\n")
        elif result == False:
            print("\rMiss!")
        elif result == 3:
            print("\rYou already fired there!")
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
    print(f"\rPlayer {turn+1}: {colors.color.BOLD}{colors.color.WARNING}Firing...{colors.color.ENDC}\n")
    print("\rUse Arrow keys to move the cursor, Enter to fire\n")

    gm2TurnPart = 1
    print(players[(turn+1)%2].stringify(cursor, False))

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
        elif gameMode == 3:  # Setup for AI game mode
            return handle_gm3_AI(key)
        elif gameMode == 10:  # Select game mode
            return select_game_mode(key)
        else:
            print("\rGame mode " + str(gameMode) + " not impl yet. press q to quit")
    except AttributeError:  # Bad key pressed
        pass


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
    By Robin, Peizhuo, and Samuel               |_|"""
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
