from pathfinding import shortest_path

class bot1:
    def __init__(self):
        self.initialPlan = None #stores initial plan to reach button
        self.isPlanned = False  #if True, plan to button already exists and bot will follow that plan, if False bot will create a plan to reach button in next move
        self.stepCount = 0 # stores number of steps taken to reach button

    def nextMove(self, ship, botPos, buttonPos, fireInitialPos):
        if not self.isPlanned: # if bot has not planned a path to button, it will plan to reach button 
            self.initialPlan = shortest_path(ship, botPos, buttonPos, {fireInitialPos})
            self.isPlanned = True #checks True to make sure bot will not plan again in next move
        if self.initialPlan is None or len(self.initialPlan) < 2: #No path exists or the bot is already at the button
            return botPos
        self.stepCount += 1
        return self.initialPlan[self.stepCount]