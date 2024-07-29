# Todo
ship obj
    attri: length, squares[length][2], sunk
    methd: hit(x,y)->bool

board obj
    attri: squares[n][n], ships[]
    methd: hit(x,y)->bool, place_ship(ship), draw()
    methd: game_over()->bool,
    methd: add_ship(ship)->bool
        check_validity()

main
    UI: welcome screen(pzliu)
    loop: place ships (Robin)
        - call the board.addShip
    loop: take turns (Robin)
    end: all ships sunk
    
class solver
    store the precaled values(pzliu)
