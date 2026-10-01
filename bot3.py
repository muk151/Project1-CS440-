from bot2 import next_move as bot2_next_move
from pathfinding import shortest_path


def next_move(ship, bot_position, button_position, burning_cells):
    fires = set(burning_cells)
    if bot_position not in ship.openCells or bot_position in fires:
        return bot_position

    # Route outside each fire's open neighboring cells.
    danger_zone = set(fires)
    for fire_cell in fires:
        if fire_cell in ship.openCells:
            danger_zone.update(ship.openNeighbors(fire_cell))

    path = shortest_path(ship, bot_position, button_position, danger_zone)
    if path is not None:
        return path[1] if len(path) > 1 else bot_position

    # Fall back to Bot 2's fire-only route if the buffer blocks every route.
    return bot2_next_move(ship, bot_position, button_position, fires)
