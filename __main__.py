from pynput import keyboard
import termios
import tty
import sys

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

# Glabal Variables
gameMode = 0  # 0: instructions, 1: Setup, 2: Game
instructions = [
    [
        "1. The game board is a 10 * 10 grid where each cell represents a part of the ocean.",
        "2. You have to first choose where you want to place your ship.",
        "3. You need to guess where the enemy ships are hidden and sink them.",
        "4. Enter coordinates to fire at that location.",
        "5. The game will tell you if you hit or missed a ship.",
        "6. Sink all enemy ships to win the game.",
        "Good luck, Captain!",
    ],
    0,
    0,
]


def print_instr():
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
        f"\r{string}{' '*(max([len(i) for i in instructions[0]])-length)}",
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
        if instructions[1] >= len(instructions[0]):
            print("\r\nStarting the game...")
            gameMode = 1
            return True
        print_instr()
    # Go back
    elif key == keyboard.Key.left:
        if instructions[1] == 0:
            return True
        instructions[1] = (instructions[1] - 1) % len(instructions[0])
        print_instr()
    # None of the tested keys were pressed
    return True


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
        else:
            print("\rGame mode: " + str(gameMode))
    except AttributeError:  # Bad key pressed
        pass


def welcome():
    """
    Displays a welcome message and instructions for the game.
    Returns:
        str: The string 'quit' if the user presses 'Q' to quit the game.
    """

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
        "Instructions: (Use right or left arrows to cycle through instructions, press Space for next, press Q to quit)\n"
    )
    print_instr()


def main():
    welcome()
    try:
        tty.setraw(sys.stdin.fileno())
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    main()
