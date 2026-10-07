import random 
from bot1 import bot1 
from bot2 import next_move as nextMove2
from bot3 import next_move as nextMove3
from bot4 import next_move as nextMove4
from pathfinding import shortest_path
from ship import generateShip, chooseInitialPos

shipSize = 10 # size of ship
numTrials = 200 # number of trials for testing each bot
qValuesNum = 10 # number of q values to test each bot
botNumbers = [1,2,3,4] # list of bots

def spreadFire(ship, fireCells, q, rng):
    nextFireCells = set(fireCells)

    for cell in ship.openCells:
        neighborsBurning = 0 # K in the probability formula 
        for neighbor in ship.openNeighbors(cell):
            if neighbor in fireCells: 
                neighborsBurning += 1
        
        if neighborsBurning > 0: 
            probability = 1-(1-q)**neighborsBurning # fire probabilty formula 
            if rng.random() < probability:
                nextFireCells.add(cell)
    return nextFireCells

def botMove(bot, number, ship, botPos, buttonPos, fireCells, initialFire, q): # sends information to the specific bot strategy and returns the next move
    if number == 1:
        return bot.nextMove(ship, botPos, buttonPos, initialFire)
    if number == 2:
        return nextMove2(ship, botPos, buttonPos, fireCells)
    if number == 3:
        return nextMove3(ship, botPos, buttonPos, fireCells)
    if number == 4:
        return nextMove4(ship, botPos, buttonPos, fireCells, q)
    

def runBotSim(ship, botStart, buttonPos, initialFire, q, number, fireSeed):
    botPos = botStart
    fireCells = {initialFire}
    fireRng = random.Random(fireSeed) 
    if number == 1:
        botStrat = bot1()
    else: 
        botStrat = None
    maxSteps = shipSize * shipSize * 2

    for b in range(maxSteps):
        nextBotPos = botMove(botStrat, number, ship, botPos, buttonPos, fireCells, initialFire, q)
        if nextBotPos == botPos and number != 4:
            return False
        botPos = nextBotPos
        if botPos in fireCells:
            return False
        if botPos == buttonPos:
            return True
        fireCells = spreadFire(ship, fireCells, q, fireRng)
        if botPos in fireCells or buttonPos in fireCells:
            return False
    
    return False

def testRuns():
    rng = random.Random()
    qValues = []
    results = {}

    while len(qValues) < qValuesNum:
        q = round(rng.uniform(0.1, 0.5), 2)
        if q not in qValues:
            qValues.append(q)
    qValues.sort()

    for botNum in botNumbers:
        results[botNum] = {}
        for q in qValues:
            results[botNum][q] = 0
    
    scenarios = []
    for c in range(numTrials):
        ship = generateShip(shipSize, rng)
        botStart, buttonPos, initialFire = chooseInitialPos(ship, rng)
        fireSeed = rng.randint(0,10000000)
        scenarios.append((ship, botStart, buttonPos, initialFire, fireSeed))

    for q in qValues:
        for ship, botStart, buttonPos, initialFire, fireSeed in scenarios:
            for botNum in botNumbers:
                success = runBotSim(ship, botStart, buttonPos, initialFire, q, botNum, fireSeed)
                if success:
                    results[botNum][q] += 1
    
    return results, qValues

def main():
    results, qValues = testRuns()
    for q in qValues:
        print(f"q = {q}")
        for botNum in botNumbers:
            successRate = results[botNum][q]
            print(f"Bot {botNum}: {successRate}/{numTrials}")
        print()

if __name__ == "__main__":
    main()