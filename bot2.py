from pathfinding import shortest_path


def next_move(ship, bot_position, button_position, burning_cells):
    fires = set(burning_cells)  # Snapshot the fire positions for this turn.
    if bot_position not in ship.openCells or bot_position in fires:
        return bot_position

    # Replan each turn, avoiding currently burning cells only.
    path = shortest_path(ship, bot_position, button_position, fires)
    if path is None or len(path) == 1:
        return bot_position
    return path[1]
