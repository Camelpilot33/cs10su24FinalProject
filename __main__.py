import keyboard
import time
def welcome():
    """welcome interface"""
    
    #some cool fonts :0
    ascii_art = r"""
    ____        _   _   _         _____ _     _       
    |  _ \      | | | | | |       / ____| |   (_)      
    | |_) | __ _| |_| |_| | ___  | (___ | |__  _ _ __  
    |  _ < / _` | __| __| |/ _ \  \___ \| '_ \| | '_ \ 
    | |_) | (_| | |_| |_| |  __/  ____) | | | | | |_) |
    |____/ \__,_|\__|\__|_|\___| |_____/|_| |_|_| .__/ 
                                                | |    
                                                |_|   """
    
    # print the instructions
    print("Instructions: (Use right or left arrows to operate through instructions, press Q to quit)")
    instructions = [ 
        "1. The game board is a 10 * 10 grid where each cell represents a part of the ocean.",
        "2. You need to guess where the enemy ships are hidden and sink them.",
        "3. Enter coordinates to fire at that location.",
        "4. The game will tell you if you hit or missed a ship.",
        "5. Sink all enemy ships to win the game.",
        "Good luck, Captain!"
    ]

    print(ascii_art)
    current_instruction = -1  # iter for list
    # print(instructions[current_instruction])
    print()

    # right -> next
    # left -> prev
    while True:
        if keyboard.is_pressed('right'):
            current_instruction = (current_instruction + 1) % len(instructions)
            print("\r" + " " * 80 + "\r" + instructions[current_instruction], end = "")
            time.sleep(0.3)  
        elif keyboard.is_pressed('left'):
            current_instruction = (current_instruction - 1) % len(instructions)
            print("\r" + " " * 80 + "\r" + instructions[current_instruction], end="")
            time.sleep(0.3)  
        elif keyboard.is_pressed('q'):
            return 'quit'

def main():
    res = welcome()
    print("exited successfully")

if __name__ == "__main__":
    main()