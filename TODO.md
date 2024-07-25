# Todo


ship obj
    attri: length, squares[length][2], sunk
    methd: hit(x,y)->bool
board obj
    attri: squares[n][n], ships[]
    methd: hit(x,y)->bool, place_ship(ship), draw()
main
    loop: place ships
    loop: take turns
    end: all ships sunk

