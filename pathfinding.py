"""Shared pathfinding for ship navigation strategies."""

from collections import deque


def shortest_path(ship, start, goal, blocked_cells=()):
    open_cells = ship.openCells
    if start not in open_cells or goal not in open_cells:
        return None

    blocked = set(blocked_cells)
    if goal != start and goal in blocked:
        return None  # Fail fast if the target is blocked.

    previous = {start: start}  # Self-parent marks the start of the path.
    frontier = deque([start])  # BFS visits cells in distance order.

    while frontier:
        cell = frontier.popleft()
        if cell == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            return path[::-1]

        for neighbor in ship.openNeighbors(cell):
            if neighbor in previous or neighbor in blocked:
                continue
            previous[neighbor] = cell
            frontier.append(neighbor)

    return None
