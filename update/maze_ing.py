import random
import typing
from collections import deque


class Cell:
    """
    Represents a single cell within the maze grid.
    Attributes:
        x (int): The X-coordinate of the cell.
        y (int): The Y-coordinate of the cell.
        coordinate (tuple): A tuple containing (x, y) coordinates.
        walls (dict): Dictionary tracking active walls.
        (1 for active, 0 for broken)
    """
    def __init__(self, x: int, y: int):
        """Initializes a Cell instance with all walls closed."""
        self.x = x
        self.y = y
        self.coordinate = (x, y)
        self.walls = {"NORTH": 1, "EAST": 1, "SOUTH": 1, "WEST": 1}

    @property
    def wallnbr(self) -> int:
        """
        Calculates the bitmask integer value representation
        of the active walls.
        Returns:
            int: The combined wall value (North=1, East=2, South=4, West=8).
        """
        return (self.walls["NORTH"] * 1) + \
               (self.walls["EAST"] * 2) + \
               (self.walls["SOUTH"] * 4) + \
               (self.walls["WEST"] * 8)

    def get_hex_value(self) -> str:
        """
        Converts the numerical wall value into a uppercase Hexadecimal string.
        """
        return f"{self.wallnbr:X}"


class Maze():
    """
    Represents the full maze structure, holding the grid data
    and generation algorithms.
    Attributes:
        width (int): Total column count.
        height (int): Total row count.
        grid (list): 2D list containing Cell objects.
        ft_cell (list): List of cells reserved for the '42' text sign.
    """
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool,
                 seed: typing.Optional[int] = None):
        """
        Initializes the maze structure, setups outer boundaries and
        structures '42' sign.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        self.ft_cell: list[Cell] = []
        self.perfect = perfect
        self.seed = seed
        self.warning_message: str = ""
        self.entry = entry
        self.exit = exit
        self.outer_walls: set[tuple[tuple[int, int], str]] = set()
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mazecell = Cell(x, y)
                current_column.append(mazecell)
            self.grid.append(current_column)
        if self.seed is not None:
            random.seed(self.seed)
        self.out_wall()
        self.ft_write()

    def ft_write(self) -> None:
        """
        Carves out coordinates to embed the '42' signature sign inside
        the grid. Triggers a warning message if the maze dimensions
        are too tight to fit it.
        """
        if self.width > 8 and self.height > 6:
            a: int = (self.width - 7) // 2
            b: int = (self.height - 5) // 2
            coord: list[tuple[int, int]] = [(2, 0), (2, 1), (2, 2), (1, 2),
                                            (0, 2), (0, 3), (0, 4), (4, 4),
                                            (5, 4), (6, 4), (6, 3), (6, 2),
                                            (5, 2), (4, 2), (4, 1), (4, 0),
                                            (4, 0), (5, 0), (6, 0)]
            for (x, y) in coord:
                target_x = a + x
                target_y = b + y
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    self.ft_cell.append(self.grid[a + x][b + y])
            if 0 <= a + 4 < self.width and 0 <= b + 3 < self.height:
                self.destroy_wall((a + 4, b + 3), (a + 3, b + 3))
            if 0 <= a + 7 < self.width and 0 <= b + 1 < self.height:
                self.destroy_wall((a + 6, b + 1), (a + 7, b + 1))
        else:
            msg = "Error: Maze is too small to fit the 42 sign."
            self.warning_message = msg

    def out_wall(self) -> None:
        """
        Identifies and registers absolute boundary walls on the outermost
        grid rows/columns.
        """
        for x in range(self.width):
            self.outer_walls.add(((x, 0), "NORTH"))
            self.outer_walls.add(((x, self.height - 1), "SOUTH"))
        for y in range(self.height):
            self.outer_walls.add(((0, y), "WEST"))
            self.outer_walls.add(((self.width - 1, y), "EAST"))

    def destroy_wall(self, cell1_coord: tuple[int, int],
                     cell2_coord: tuple[int, int]) -> None:
        """
        Breaks down shared walls between two adjacent cells if they
        are not outer boundaries.
        """
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        if x1 == x2 and y2 == y1 - 1:
            if (cell1_coord, "NORTH") in self.outer_walls:
                if (cell2_coord, "SOUTH") in self.outer_walls:
                    return
            c1.walls["NORTH"] = 0
            c2.walls["SOUTH"] = 0
        elif x1 == x2 and y2 == y1 + 1:
            if (cell1_coord, "SOUTH") in self.outer_walls:
                if (cell2_coord, "NORTH") in self.outer_walls:
                    return
            c1.walls["SOUTH"] = 0
            c2.walls["NORTH"] = 0
        elif y1 == y2 and x2 == x1 + 1:
            if (cell1_coord, "EAST") in self.outer_walls:
                if (cell2_coord, "WEST") in self.outer_walls:
                    return
            c1.walls["EAST"] = 0
            c2.walls["WEST"] = 0
        elif y1 == y2 and x2 == x1 - 1:
            if (cell1_coord, "WEST") in self.outer_walls:
                if (cell2_coord, "EAST") in self.outer_walls:
                    return
            c1.walls["WEST"] = 0
            c2.walls["EAST"] = 0

    def build_wall(self, cell1_coord: tuple[int, int],
                   cell2_coord: tuple[int, int]) -> bool:
        """
        Reconstructs/closes a wall partition between two adjacent cells.
        Returns:
        bool: True if a wall was built successfully, False if already present.
        """
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]

        if x1 == x2 and y2 == y1 - 1:
            if c1.walls["NORTH"] != 1 and c2.walls["SOUTH"] != 1:
                c1.walls["NORTH"] = 1
                c2.walls["SOUTH"] = 1
                return True
        elif x1 == x2 and y2 == y1 + 1:
            if c1.walls["SOUTH"] != 1 and c2.walls["NORTH"] != 1:
                c1.walls["SOUTH"] = 1
                c2.walls["NORTH"] = 1
                return True
        elif y1 == y2 and x2 == x1 + 1:
            if c1.walls["EAST"] != 1 and c2.walls["WEST"] != 1:
                c1.walls["EAST"] = 1
                c2.walls["WEST"] = 1
                return True
        elif y1 == y2 and x2 == x1 - 1:
            if c1.walls["WEST"] != 1 and c2.walls["EAST"] != 1:
                c1.walls["WEST"] = 1
                c2.walls["EAST"] = 1
                return True
        return False

    def create_guaranteed_path(self) -> list[tuple[int, int]]:
        """
        Generates a randomized guaranteed path connecting entry
        and exit coordinates.
        Ensures the path bypasses protected '42' sign cells.
        """
        start = self.entry
        end = self.exit
        path = [start]
        visited = {start}
        current = start
        moves = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0),
                 "WEST": (-1, 0)}
        while current[0] != end[0] or current[1] != end[1]:
            curr_x, curr_y = current
            directions = ["NORTH", "EAST", "SOUTH", "WEST"]
            random.shuffle(directions)
            moved = False
            for direction in directions:
                dx, dy = moves[direction]
                next_x, next_y = curr_x + dx, curr_y + dy
                next_coord = (next_x, next_y)
                if 0 <= next_x < self.width and 0 <= next_y < self.height:
                    next_cell = self.grid[next_x][next_y]
                    if next_cell not in self.ft_cell:
                        if next_coord not in visited:
                            self.destroy_wall(current, next_coord)
                            visited.add(next_coord)
                            path.append(next_coord)
                            current = next_coord
                            moved = True
                            break
            if not moved:
                path.pop()
                if path:
                    current = path[-1]
                else:
                    current = start
                    path = [start]
                    visited = {start}
        return path

    def random_broker(self, break_count: int = 2) -> None:
        """
        Randomly fractures interior walls across the maze to
        introduce loops/braids.
        Maintains valid configurations using 3x3 layout verification checks.
        """
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        moves = {
            "NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                current_cell = self.grid[x][y]
                if current_cell not in self.ft_cell:
                    cell_break_count = random.randint(0, 2)

                    chosen_directions = random.sample(directions,
                                                      cell_break_count)

                    for direction in chosen_directions:
                        if current_cell.walls[direction] == 0:
                            continue
                        dx, dy = moves[direction]
                        next_x, next_y = x + dx, y + dy
                        if (0 <= next_x < self.width and
                                0 <= next_y < self.height):
                            next_cell = self.grid[next_x][next_y]
                            if next_cell not in self.ft_cell:
                                self.destroy_wall((x, y), (next_x, next_y))
                                start_x_min = max(0, x - 2)
                                start_x_max = min(self.width - 3, x)
                                start_y_min = max(0, y - 2)
                                start_y_max = min(self.height - 3, y)
                                illegal_area_found = False
                                for sx in range(start_x_min, start_x_max + 1):
                                    for sy in range(start_y_min,
                                                    start_y_max + 1):
                                        if self.checker_3x3():
                                            illegal_area_found = True
                                            break
                                    if illegal_area_found:
                                        break
                                if illegal_area_found:
                                    self.build_wall((x, y), (next_x, next_y))

    def get_open_neighbors(
            self, cell_coord: tuple[int, int]
            ) -> list[tuple[int, int]]:
        """
        Finds adjacent neighboring coordinates that can be
        reached without encountering a wall.
        Returns:
            list: Accessible coordinates from the source cell.
        """
        x, y = cell_coord
        c1 = self.grid[x][y]
        open_neighbors = []
        if c1.walls.get("NORTH") == 0 and y - 1 >= 0:
            open_neighbors.append((x, y - 1))

        if c1.walls.get("SOUTH") == 0 and y + 1 < self.height:
            open_neighbors.append((x, y + 1))

        if c1.walls.get("EAST") == 0 and x + 1 < self.width:
            open_neighbors.append((x + 1, y))

        if c1.walls.get("WEST") == 0 and x - 1 >= 0:
            open_neighbors.append((x - 1, y))

        return open_neighbors

    def find_solution_ways(self) -> list[list[tuple[int, int]]]:
        """
        Uses to find accessible paths from entry to exit.
        Returns:
            list: List of valid solution paths discovered.
        """
        start = self.entry
        end = self.exit
        queue = deque([([start], {start})])
        found_paths: list[list[tuple[int, int]]] = []
        visit_counts: dict[tuple[int, int], int] = {}
        while queue:
            if len(found_paths) >= 2:
                break
            path, path_set = queue.popleft()
            curr_cell = path[-1]
            if curr_cell == end:
                found_paths.append(path)
                continue
            visit_counts[curr_cell] = visit_counts.get(curr_cell, 0) + 1
            if visit_counts[curr_cell] > 4:
                continue
            for neighbor in self.get_open_neighbors(curr_cell):
                if neighbor not in path_set:
                    new_path = path + [neighbor]
                    new_path_set = path_set.copy()
                    new_path_set.add(neighbor)
                    queue.append((new_path, new_path_set))
        return found_paths

    def perfect_maker(self) -> bool:
        """
        Enforces 'perfect maze' properties by selectively blocking
        alternative paths. Guarantees that exactly one distinct solution
        route exists.
        Returns:
            bool: True if alternative paths were sealed,
            False if already perfect.
        """
        wall_built = False
        while True:
            all_paths = self.find_solution_ways()
            if len(all_paths) == 1:
                break
            all_paths.sort(key=len)
            main_path = all_paths[0]
            main_edges = set()
            for i in range(len(main_path) - 1):
                edge = tuple(sorted([main_path[i], main_path[i+1]]))
                main_edges.add(edge)
            this_turn_built = False
            for path in all_paths[1:]:
                for i in range(len(path) - 1):
                    curr_cell = path[i]
                    next_cell = path[i+1]
                    edge = tuple(sorted([curr_cell, next_cell]))
                    if edge not in main_edges:
                        attempt = 0
                        while True:
                            attempt += 1
                            if attempt > 50:
                                k = i
                            else:
                                k = random.randint(i, len(path) - 2)
                            curr_cell = path[k]
                            next_cell = path[k + 1]
                            edge = tuple(sorted([curr_cell, next_cell]))
                            if edge not in main_edges:
                                if (self.build_wall(curr_cell, next_cell)
                                        is True):
                                    this_turn_built = True
                                    wall_built = True
                                    break
                    if this_turn_built:
                        break
                if this_turn_built:
                    break
        return wall_built

    def fix_isolated_cells(self) -> bool:
        """
        Connects disconnected/isolated regions back to the main reachable grid.
        Rebuilds the reachable set after every repair pass so that chains of
        isolated cells are all correctly resolved.
        Returns:
            bool: True if structural repairs were made,
            False if everything is connected.
        """
        moves = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0),
                 "WEST": (-1, 0)}

        def build_visited() -> set:
            """Entry — returns all currently reachable coords."""
            visit: set = {self.entry}
            tail: deque = deque([self.entry])
            while tail:
                cx, cy = tail.popleft()
                for direction, (dx, dy) in moves.items():
                    if self.grid[cx][cy].walls.get(direction, 1) == 0:
                        nx, ny = cx + dx, cy + dy
                        if (0 <= nx < self.width and 0 <= ny < self.height
                                and (nx, ny) not in visit):
                            visit.add((nx, ny))
                            tail.append((nx, ny))
            return visit

        any_cell_fixed = False
        while True:
            visited = build_visited()
            fixed_this_round = False
            for x in range(self.width):
                for y in range(self.height):
                    current_coord = (x, y)
                    if (current_coord not in visited and
                            self.grid[x][y] not in self.ft_cell):
                        directions = list(moves.keys())
                        random.shuffle(directions)
                        for direction in directions:
                            dx, dy = moves[direction]
                            next_x, next_y = x + dx, y + dy
                            next_coord = (next_x, next_y)
                            if (0 <= next_x < self.width and
                                    0 <= next_y < self.height):
                                if (next_coord in visited and
                                   self.grid[next_x][next_y]
                                        not in self.ft_cell):
                                    self.destroy_wall(current_coord,
                                                      next_coord)
                                    visited.add(current_coord)
                                    any_cell_fixed = True
                                    fixed_this_round = True
                                    break
            if not fixed_this_round:
                break
        return any_cell_fixed

    def checker_3x3(self) -> bool:
        """
        Validates structural conditions inside a 3x3 local cluster starting at
        entry coordinates.
        Returns:
            bool: Validation results.
        """
        start_x = self.entry[0]
        start_y = self.entry[1]
        if start_x < 0 or start_y < 0:
            return False
        if start_x + 2 >= self.width or start_y + 2 >= self.height:
            return False
        for i in range(3):
            for j in range(3):
                curr_cell = self.grid[start_x + i][start_y + j]
                if j < 2 and curr_cell.walls["NORTH"] == 1:
                    return False
                if i < 2 and curr_cell.walls["EAST"] == 1:
                    return False
                if j > 2 and curr_cell.walls["SOUTH"] == 1:
                    return False
                if i > 2 and curr_cell.walls["WEST"] == 1:
                    return False
        return True


def generate(maze: Maze) -> list[list[tuple[int, int]]]:
    """
    Orchestrates the entire execution pipeline to structure and build
    a functional maze.
    Returns:
        list: Discovered solutions after build completion.
    """
    maze.ft_write()
    if any(cell.coordinate == maze.entry for cell in maze.ft_cell):
        raise ValueError("Error: Entry coordinates cannot be on the 42 sign.")
    if any(cell.coordinate == maze.exit for cell in maze.ft_cell):
        raise ValueError("Error: Exit coordinates cannot be on the 42 sign.")
    maze.create_guaranteed_path()
    maze.random_broker()
    # Always repair isolation from path carving / random_broker first.
    # Without this, perfect_maker may see only one solution path and exit
    # immediately, so fix_isolated_cells would never run.
    maze.fix_isolated_cells()
    if maze.perfect is True:
        while maze.perfect_maker():
            maze.fix_isolated_cells()
    if maze.perfect is False:
        maze.fix_isolated_cells()
    if maze.warning_message:
        print(maze.warning_message)
    return maze.find_solution_ways()
