# Todo
 - [x] ship obj
   - [x] attribues: 
     - [x] length,
     - [x] squares[length][2], 
   - [x] methd: 
     - [x] isSunk() -> bool
     - [x] hit(x,y) -> bool

- [x] board obj
  - [x] attri: squares[n][n], ships[]
  - [x] methd: hit(x,y) -> bool
  - [x] methd: placeShip(ship)
    - [x] check validity
  - [x] methd: \_\_str\_\_()
  - [x] methd: game_over() -> bool
  - [x] methd: placeShipsRandomly()
    - [x] place ships randomly

main
    UI: welcome screen(pzliu)
    loop: place ships (Robin)
        - call the board.addShip
    loop: take turns (Robin)
    end: all ships sunk
    
class solver
    store the precaled values(pzliu)


## imports used:
classes.py: random