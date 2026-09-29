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

    for rowChange, colChange in movements:
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
        rowIsValid = 0 <= row < self.dimensions[0]
        colIsValid = 0 <= col < self.dimensions[1]
        return rowIsValid and colIsValid # will return true if the cell is in bounds
    
    def neighbors(self, cell):
        return gridNeighbors(cell, self.dimensions) # returns the neighbors of a cell
    
    def openNeighbors(self, cell): # will only return the neighbors that are open
        result = []
        for neighbor in self.neighbors(cell):
            if neighbor in self.openCells:
                result.append(neighbor)
        return result 
    
            
    
    
        
