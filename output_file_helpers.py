from maze_ing import Maze


def convert_path_to_string(path: list[tuple[int, int]]) -> str:
    """
    Converts a sequence of coordinate nodes into cardinal direction
    tokens (N, E, S, W).
    Args:
        path (list): Sequential coordinate tuples representing the path.
    Returns:
        str: Continuous string of direction characters.
    """
    if not path or len(path) < 2:
        return ""
    direction_letters: list[str] = []
    for i in range(len(path) - 1):
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]

        dx = next_x - curr_x
        dy = next_y - curr_y

        if dx == 0 and dy == 1:
            direction_letters.append("N")
        elif dx == 1 and dy == 0:
            direction_letters.append("E")
        elif dx == 0 and dy == -1:
            direction_letters.append("S")
        elif dx == -1 and dy == 0:
            direction_letters.append("W")
        else:
            raise ValueError(
                f"Invalid path step: from {path[i]} to {path[i+1]} dne!"
            )
    return "".join(direction_letters)


def write_output_file(
        file_path: str, maze: Maze, shortest_path: list[tuple[int, int]]
        ) -> None:
    """
    Writes the structural map matrix data, bounds, path data to a text file.
    """
    path_str: str = convert_path_to_string(shortest_path)
    with open(file_path, "w", encoding="utf-8") as file:
        for y in reversed(range(maze.height)):
            row_hex: list[str] = [f"{maze.grid[x][y].wallnbr:X}"
                                  for x in range(maze.width)]
            file.write("".join(row_hex) + "\n")
        file.write("\n")
        file.write(f"{maze.entry[0]},{maze.entry[1]}\n{maze.exit[0]},"
                   f"{maze.exit[1]}\n{path_str}\n")
