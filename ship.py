import os 
from collections import deque
import random 

cell_position = tuple[int, int]
movements = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1)    # right
] 

def gridNeighbors(cell, dimensions=(10, 10)): # returns neighbors in grid

    row = cell[0]
    col = cell[1]
    neighbors = []

    for rowChange, colChange in dimensions:
        newRow = row + rowChange
        newCol = col + colChange
         
        if 0 <= newRow < dimensions[0] and 0 <= newCol < dimensions[1]:
            neighbors.append((newRow, newCol))
        
    return neighbors

class Ship: 
    def __init__(self, openCells, dimensions, shipSize):
        self.openCells = set(openCells)
        self.dimensions = dimensions
        self.shipSize = shipSize
        self.shipCells = []
    
    def inBounds(self, cell):
        row = cell[0]
        col = cell[1]
        rowIsValid = 0 <= row < len(self.dimensions)
        colIsValid = 0 <= col < len(self.dimensions[0])
        return rowIsValid and colIsValid # will return true if the cell is in bounds
    
    def neighbors(self, cell):
        return gridNeighbors(cell, self.dimensions) # returns the neighbors of a cell
    
    def openNeighbors(self, cell): # will only return the neighbors that are open
        result = []
        for neighbor in self.neighbors(cell):
            if neighbor in self.openCells:
                result.append(neighbor)
        return result 
    def isConnected(self, cells):
        if not cells:
            return False
        
        visited = set()
        queue = deque([cells[0]])
        
        while queue:
            current = queue.popleft()
            visited.add(current)
            
            for neighbor in self.openNeighbors(current):
                if neighbor in cells and neighbor not in visited:
                    queue.append(neighbor)
        
        return len(visited) == len(cells)
    def shipPicture(self, fire, bot, button):
        completedRow = []

        for row in range(len(self.dimensions)):
            currRow = []
            for col in range(len(self.dimensions[0])):
                cell = (row, col)
                if col in self.openCells:
                    symbol = "."  # open cell
                else:
                    symbol = "#" # closed cell
                
                if cell == button: # button
                    symbol = "X"
                if cell in fire: # fire
                    symbol = "F"
                if cell == bot: # bot
                    symbol = "B"
                currRow.append(symbol)
            completedRow.append(" ".join(currRow))
        return "\n".join(completedRow)

def openNeighborsCount(self, cell):
        count = 0
        for neighbor in self.neighbors(cell):
            if neighbor in self.openCells:
                count += 1
        return count
def findBlockedCellNeighbors(self, openCells, cell): # will find blocked cells that have only one open neighbor
        possibleOpenNeighbors = []
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                cell = (row, col)
                blockedCell = cell not in openCells
                if blockedCell:
                    numOpenNeighbors = self.openNeighborsCount(cell, openCells, self.dimensions)
                    if numOpenNeighbors == 1:
                        possibleOpenNeighbors.append(cell)
        return possibleOpenNeighbors
def deadEndCells(self, openCells, dimensions): 
        deadEndCells = []
        for cell in openCells:
            numOpenNeighbors = self.openNeighborsCount(cell, openCells, dimensions)
            if numOpenNeighbors == 1:
                deadEndCells.append(cell)
        return deadEndCells
def closedNeighbors(self, openCells, cell, dimensions):
        closedNeighbors = []
        for neighbor in gridNeighbors(cell, dimensions):
            if neighbor not in openCells:
                closedNeighbors.append(neighbor)
        return closedNeighbors
def generateShip(self, dimensions, rng=None):
        if rng is None:
            rng = random.Random()
        
        startRow = rng.randint(0, dimensions[0] - 1)
        startCol = rng.randint(0, dimensions[1] - 1)
        startCell = (startRow, startCol)
            
        openCells = {startCell}
        potentialCandidates = self.findBlockedCellNeighbors(openCells, dimensions)

        while len(potentialCandidates) > 0:
            cellChosen = rng.choice(potentialCandidates)
            openCells.add(cellChosen)
            potentialCandidates = self.findBlockedCellNeighbors(openCells, dimensions)

            
        currentDeadEndCells = self.deadEndCells(openCells, dimensions)
        originalDeadEndCells = len(currentDeadEndCells)
        maxDeadEndCells = originalDeadEndCells / 2

        while len(currentDeadEndCells) > maxDeadEndCells:
            deadEndCellsAllowed = []

            for deadEndCell in currentDeadEndCells:
                closedNeighbors = self.closedNeighbors(openCells, deadEndCell, dimensions)
                if len(closedNeighbors) > 0:
                    deadEndCellsAllowed.append(deadEndCell)
                
            if len(deadEndCellsAllowed) == 0:
                    break
                
            deadEndCellChosen = rng.choice(deadEndCellsAllowed)
            closedNeighbors = self.closedNeighbors(openCells, deadEndCellChosen, dimensions)
            cellToBeOpened = rng.choice(sorted(closedNeighbors))
            openCells.add(cellToBeOpened)
            currentDeadEndCells = self.deadEndCells(openCells, dimensions)
        
        ship = Ship(openCells, dimensions, self.shipSize)

        return ship
    
def chooseInitialPos(self, ship, rng=None):
        if rng is None:
            rng = random.Random()
        
        positionPossibilities = sorted(ship.openCells)
        positionChosen = rng.choice( positionPossibilities, 3) 

        botPosition = positionChosen[0]
        firePosition = positionChosen[1]
        buttonPosition = positionChosen[2]
        return botPosition, firePosition, buttonPosition 

def main():
     rng = random.Random(440)
     ship = generateShip(10, rng)

     bot, button, fire = chooseInitialPos(ship, rng)

     print(ship.shipPicture(fire, bot, button))
     print()

             
        





             

    
    
