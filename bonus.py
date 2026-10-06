import random

from bot2 import next_move
from ship import Ship, chooseInitialPos

"""This compares three connected layouts and choose the best one for Bot 2."""

TRIALS = 100  # Number of runs for each layout at each q value.
Q_VALUES = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  # Fire spread probabilities to compare.


def make_layouts():
    # Each shape has 20 open cells on a 10 by 10 board.
    # Open only the square's border to create a cycle with two routes.
    ring = set()
    for row in range(2, 8):
        for col in range(2, 8):
            if row in (2, 7) or col in (2, 7):
                ring.add((row, col))

    # Compare the cycle with a two-row strip and a filled rectangle.
    ladder = {(row, col) for row in (4, 5) for col in range(10)}
    compact = {(row, col) for row in range(3, 7) for col in range(2, 7)}
    return {"ring": ring, "ladder": ladder, "compact": compact}


def spread_fire(ship, fires, q, rng):
    # Use the original fires for every calculation so spread is simultaneous.
    next_fires = set(fires)
    for cell in sorted(ship.openCells - fires):
        K = 0  # Count the cell's currently burning neighbors.
        for neighbor in ship.openNeighbors(cell):
            if neighbor in fires:
                K += 1
        # Ignite this cell with the probability given by the assignment.
        if rng.random() < 1 - (1 - q) ** K:
            next_fires.add(cell)
    return next_fires


def run_trial(ship, q, rng):
    # Randomly place the bot, button, and fire in three distinct open cells.
    bot, button, fire = chooseInitialPos(ship, rng)
    fires = {fire}

    while True:
        # The bot moves before the fire spreads each turn.
        next_position = next_move(ship, bot, button, fires)
        if next_position == bot:
            return False  # Bot 2 stays only when it has no route.
        bot = next_position
        if bot in fires:
            return False
        if bot == button:
            return True  # Pressing the button stops the fire immediately.

        fires = spread_fire(ship, fires, q, rng)
        # A burning bot is dead; a burning button cannot be reached by Bot 2.
        if bot in fires or button in fires:
            return False


def score_layout(ship):
    # Reset the seed for each layout to make the comparison reproducible.
    rng = random.Random(440)
    successes = 0
    for q in Q_VALUES:
        for _ in range(TRIALS):
            if run_trial(ship, q, rng):
                successes += 1
    # Score each layout by its success fraction across all runs and q values.
    return successes / (len(Q_VALUES) * TRIALS)


def main():
    best_name = ""
    best_ship = None
    best_score = -1

    print("Average Bot 2 success across q values:")
    for name, cells in make_layouts().items():
        ship = Ship(cells, (10, 10), 10)
        score = score_layout(ship)
        print(f"{name}: {score:.1%}")
        # Keep the layout with the highest observed success rate.
        if score > best_score:
            best_name = name
            best_ship = ship
            best_score = score

    print(f"\nBest of these layouts for Bot 2: {best_name} ({best_score:.1%})")
    # Show the winning layout without bot, button, or fire markers.
    print(best_ship.shipPicture(set(), None, None))


if __name__ == "__main__":
    main()
