# general algo implementaion

# For each ship, find all possible locations on the board where it could be placed.

# loop until timer > 5sec:
#     for random valid ship location:
#         frequencies[ship's squares] += 1
#     count += 1

# guess = max(frequencies)
from classes import Board
import random

def solve_battleship(board, cycles=1000):
    possible_loc = {}

    # For each ship from 1 to x
    for ship_type in Board.types:
        possible_loc[ship_type] = []
        ship_length = Board.types[ship_type]
        
        # For each square from 1 to 100
        for x in range(11-ship_length):
            for y in range(11-ship_length):
                
                # For each orientation from vertical to horizontal
                for orientation in ["horizontal", "vertical"]:
                    pos = []
                    if orientation == "horizontal":
                        if x + ship_length > 10:
                            continue
                        pos = [(x+i, y) for i in range(ship_length)]
                    else:
                        if y + ship_length > 10:
                            continue
                        pos = [(x, y+i) for i in range(ship_length)]

                    # If the ship would overhang the board, continue
                    if any(s[0] >= 10 or s[1] >= 10 for s in pos):
                        continue
                    
                    # If the ship would overlap a "miss" square, continue
                    if any(board.grid[s[0]][s[1]] == 1 for s in pos):
                        continue
                    
                    # Add this ship location to the list of possible locations
                    possible_loc[ship_type].append(pos)

    incompatible_loc = []

    # For each ship
    for ship_type in possible_loc:
        
        # For each possible ship location
        for pos in possible_loc[ship_type]:
            
            # For every other ship
            for other_ship_type in possible_loc:
                if ship_type == other_ship_type:
                    continue
                
                # For every possible other-ship location
                for other_ship_squares in possible_loc[other_ship_type]:
                    
                    # If the two ships would overlap, save to list of incompatible locations
                    if any(s in other_ship_squares for s in pos):
                        incompatible_loc.append((pos, other_ship_squares))

    location_freq = {ship_type: [0] * len(possible_loc[ship_type]) for ship_type in Board.types}
    valid_cnt = 0

    for _ in range(cycles):  # Loop A, y times
        selected_loc = {}
        valid = True

        # For each ship
        for ship_type in possible_loc:
            # Select one random possible ship location
            idx = random.randint(0, len(possible_loc[ship_type]) - 1)
            selected_location = possible_loc[ship_type][idx]

            # If location is incompatible with any other selected locations, continue loop A
            for loc in selected_loc.values():
                if (selected_location, loc) in incompatible_loc or (loc, selected_location) in incompatible_loc:
                    valid = False
                    break
            if not valid:
                break

            selected_loc[ship_type] = selected_location

        if not valid:
            continue

        # If this configuration conflicts with the current board state
        for selected_location in selected_loc.values():
            if any(board.grid[s[0]][s[1]] == 2 and s not in selected_location for s in selected_location):
                valid = False
                break
        if not valid:
            continue
        # For each selected ship location
        for ship_type, selected_location in selected_loc.items():
            location_freq[ship_type][possible_loc[ship_type].index(selected_location)] += 1
        
        valid_cnt += 1

    square_freq = [[0 for _ in range(10)] for _ in range(10)]
    
    # For each possible ship location
    for ship_type in possible_loc:
        for index, pos in enumerate(possible_loc[ship_type]):
            # For each square covered by this ship location
            for s in pos:
                if board.grid[s[0]][s[1]] == 0: #don't guess hit locations  
                    square_freq[s[0]][s[1]] += location_freq[ship_type][index]
    
    # Divide each element in square_freq by valid_cnt
    for x in range(10):
        for y in range(10):
            if valid_cnt == 0:
                return square_freq
            square_freq[x][y] /= valid_cnt 

    return square_freq
