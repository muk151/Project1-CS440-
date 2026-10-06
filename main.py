import random 
from bot1 import bot1 
from bot2 import next_move as nextMove2
from bot3 import next_move as nextMove3
from pathfinding import shortest_path
from ship import generateShip, chooseInitialPos 

def spreadFire(ship, fireCells, q, rng):
    nextFireCells = set(fireCells)
    
    for cell in ship.openCells:
        
    