import random 
from bot1 import bot1 
from bot2 import next_move as nextMove2
from bot3 import next_move as nextMove3
from bot4 import next_move as nextMove4
from pathfinding import shortest_path
from ship import generateShip, chooseInitialPos

shipSize = 10 # size of ship
numTrials = 100 # number of trials for testing each bot
qValuesNum = 10 # number of q values to test each bot
botNumbers = [1,2,3,4] # list of bots
outcomes = ["success", "trapped by fire", "moved into fire", "burned after fire spread", "button burned", "step limit reached" ]

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
    

def runBotSim(ship, botStart, buttonPos, initialFire, q, number, fireSeed): # runs the simulation for a specific and returns that bot's outcome and the number of steps taken
    botPos = botStart
    fireCells = {initialFire}
    fireRng = random.Random(fireSeed)
    if number == 1:
        botStrat = bot1()
    else: 
        botStrat = None
    maxSteps = shipSize * shipSize * 2

    for step in range(maxSteps):
        nextBotPos = botMove(botStrat, number, ship, botPos, buttonPos, fireCells, initialFire, q) # gets the next move from the bot strategy
        if nextBotPos == botPos:
            path = shortest_path(ship, botPos, buttonPos, fireCells)
            if number != 4 or path is None:
                return "trapped by fire", step  
        botPos = nextBotPos

        if botPos in fireCells:
            return "moved into fire", step + 1
        if botPos == buttonPos: 
            return "success", step + 1
        
        fireCells = spreadFire(ship, fireCells, q, fireRng)
        if botPos in fireCells:
            return "burned after fire spread", step + 1
        if buttonPos in fireCells:
            return "button burned", step + 1
    
    return "step limit reached", maxSteps
def testRuns(): # runs the simulation for all bots and all q values and returns the results
    rng = random.Random()
    qValues = [0.0, 0.75, 1.0]
    results = {}

    while len(qValues) < qValuesNum:
        q = round(rng.uniform(0, 1), 2) # generates random q values between 0 and 1
        if q not in qValues:
            qValues.append(q)
    qValues.sort()

    for botNum in botNumbers: # initializes the results dictionary for each bot and q value
        results[botNum] = {}
        for q in qValues:
            results[botNum][q] = {}
            for outcome in outcomes:
                results[botNum][q][outcome] = 0
    
    scenarios = []
    for c in range(numTrials):
        ship = generateShip(shipSize, rng)
        botStart, buttonPos, initialFire = chooseInitialPos(ship, rng)
        fireSeed = rng.randint(0,10000000) # generates a random position for the fire spread to ensure different fire spread patterns for each trial
        scenarios.append((ship, botStart, buttonPos, initialFire, fireSeed))

    for q in qValues: # runs the simulation for each bot and q value and updates the results dictionary with the outcomes
        for ship, botStart, buttonPos, initialFire, fireSeed in scenarios:
            for botNum in botNumbers:
                outcome, c = runBotSim(ship, botStart, buttonPos, initialFire, q, botNum, fireSeed)
                results[botNum][q][outcome] += 1
    
    return results, qValues

def main(): # runs the testRuns function and then prints the results for each bot and the corresponding q value 
    results, qValues = testRuns()  
    for q in qValues:
        print("q = " + str(q))
        for botNum in botNumbers:
            botResults = results[botNum][q]
            print("Bot " + str(botNum) + ": " + str(botResults["success"]) + "/" + str(numTrials) + " successes")
            for outcome in outcomes[1:]:
                print("  " + outcome + ": " + str(botResults[outcome]))

        print()

if __name__ == "__main__":
    main()