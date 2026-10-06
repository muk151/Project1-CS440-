from pathfinding import shortest_path


def next_move(ship, bot_position, button_position, burning_cells, q, risk_weight=5):
    # Copy the fire state so this function leaves the caller's data unchanged.
    fires = set(burning_cells)
    possible_moves = ship.openNeighbors(bot_position) + [bot_position]
    best_move = bot_position
    best_score = float("inf")

    # Evaluate neighboring cells and staying still.
    for candidate in possible_moves:
        if candidate in fires:
            continue
        if candidate == button_position:
            return candidate  # The button stops the fire before it spreads.

        # K burning neighbors determine the chance this cell catches fire.
        K = 0
        for neighbor in ship.openNeighbors(candidate):
            if neighbor in fires:
                K += 1
        risk = 1 - (1 - q) ** K

        path = shortest_path(ship, candidate, button_position, fires)
        if path is None:
            continue  # Ignore moves with no route to the button around current fires.

        # Balance remaining steps against the chance of burning next turn.
        distance = len(path) - 1
        score = distance + risk_weight * risk
        if score < best_score:
            best_move = candidate
            best_score = score

    return best_move
