from pynput import keyboard

def welcome():
    """welcome interface"""
    
    # Some cool fonts :0
    ascii_art = r"""
     ____        _   _   _         _____ _     _       
    |  _ \      | | | | | |       / ____| |   (_)      
    | |_) | __ _| |_| |_| | ___  | (___ | |__  _ _ __  
    |  _ < / _` | __| __| |/ _ \  \___ \| '_ \| | '_ \ 
    | |_) | (_| | |_| |_| |  __/  ____) | | | | | |_) |
    |____/ \__,_|\__|\__|_|\___| |_____/|_| |_|_| .__/ 
                                                | |    
                                                |_|   """
    
    print(ascii_art)
    # Print the instructions
    print("Instructions: (Use right or left arrows to operate through instructions, press Q to quit)")
    instructions = [ 
        "1. The game board is a 10 * 10 grid where each cell represents a part of the ocean.",
        "2. You have to first choose where you want to place your ship.",
        "3. You need to guess where the enemy ships are hidden and sink them.",
        "4. Enter coordinates to fire at that location.",
        "5. The game will tell you if you hit or missed a ship.",
        "6. Sink all enemy ships to win the game.",
        "Good luck, Captain!"
    ]

    current_instruction = 0  # Iter for list
    print(instructions[current_instruction], end = "")

    def on_press(key):
        nonlocal current_instruction # not a new var! 
        if key == keyboard.Key.right:
            current_instruction = (current_instruction + 1) % len(instructions)
            print("\r" + " " * 100 + "\r", end = "") # clear prev output
            print(instructions[current_instruction], end = "")
        elif key == keyboard.Key.left: 
            current_instruction = (current_instruction - 1) % len(instructions)
            print("\r" + " " * 100 + "\r", end = "") 
            print(instructions[current_instruction], end = "")
        elif key.char and key.char.lower() == 'q':
            return False
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    return 'quit'

def main():
    res = welcome()
    print("\nExited successfully")

if __name__ == "__main__":
    main()
