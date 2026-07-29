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
            coord: list[tuple[int, int]] = [(0, 0), (0, 1), (0, 2), (1, 2),
                                            (2, 2), (2, 3), (2, 4), (4, 4),
                                            (5, 4), (6, 4), (4, 3), (6, 2),
                                            (5, 2), (4, 2), (6, 1), (4, 0),
                                            (5, 0), (6, 0)]
            for (x, y) in coord:
                target_x = a + x
                target_y = b + y
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    self.ft_cell.append(self.grid[a + x][b + y])
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
                     cell2_coord: tuple[int, int]) -> bool:
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
                    return True
            c1.walls["NORTH"] = 0
            c2.walls["SOUTH"] = 0
        elif x1 == x2 and y2 == y1 + 1:
            if (cell1_coord, "SOUTH") in self.outer_walls:
                if (cell2_coord, "NORTH") in self.outer_walls:
                    return True
            c1.walls["SOUTH"] = 0
            c2.walls["NORTH"] = 0
        elif y1 == y2 and x2 == x1 + 1:
            if (cell1_coord, "EAST") in self.outer_walls:
                if (cell2_coord, "WEST") in self.outer_walls:
                    return True
            c1.walls["EAST"] = 0
            c2.walls["WEST"] = 0
        elif y1 == y2 and x2 == x1 - 1:
            if (cell1_coord, "WEST") in self.outer_walls:
                if (cell2_coord, "EAST") in self.outer_walls:
                    return True
            c1.walls["WEST"] = 0
            c2.walls["EAST"] = 0
        if self.checker_3x3(x1, y1):
            self.build_wall((x1, y1), (x2, y2))
            return False
        return True

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
                                        if self.checker_3x3(sx, sy):
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
        def reachable_count() -> int:
            seen = {self.entry}
            queue = deque([self.entry])
            while queue:
                cx, cy = queue.popleft()
                for nxt in self.get_open_neighbors((cx, cy)):
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append(nxt)
            return len(seen)

        wall_built = False
        baseline = reachable_count()
        moves = {"EAST": (1, 0), "SOUTH": (0, 1)}
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                if cell in self.ft_cell:
                    continue
                for direction, (dx, dy) in moves.items():
                    if cell.walls[direction] != 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                    if self.grid[nx][ny] in self.ft_cell:
                        continue
                    if self.build_wall((x, y), (nx, ny)):
                        if reachable_count() == baseline:
                            wall_built = True
                        else:
                            self.destroy_wall((x, y), (nx, ny))
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

        def build_visited() -> set[tuple[int, int]]:
            """Entry — returns all currently reachable coords."""
            visit: set[tuple[int, int]] = {self.entry}
            tail: deque[tuple[int, int]] = deque([self.entry])
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

    def fix_isolated_cells_nonper(self) -> bool:
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

        for x in range(self.width):
            for y in range(self.height):
                curr_cell = self.grid[x][y]
                if (curr_cell.wallnbr in (7, 11, 13, 14)):
                    if (curr_cell.coordinate not in (self.entry, self.exit)):
                        directions = list(moves.keys())
                        random.shuffle(directions)
                        for direction in directions:
                            dx, dy = moves[direction]
                            next_x, next_y = x + dx, y + dy
                            next_coord = (next_x, next_y)
                            if (0 <= next_x < self.width and
                                    0 <= next_y < self.height):
                                if (self.grid[next_x][next_y]
                                        not in self.ft_cell):
                                    if (self.destroy_wall(curr_cell.coordinate,
                                                      next_coord) == False):
                                        return False
        return True


    def checker_3x3(self, x: int, y: int) -> bool:
        """
        Checks if the given cell (x, y) is part of ANY 3x3 fully open
        empty block by testing all possible 9 relative positions
        where (x, y) can reside inside a 3x3 grid.
        """
        for dx in range(3):
            for dy in range(3):
                start_x = x - dx
                start_y = y - dy
                if start_x < 0 or start_y < 0:
                    continue
                if start_x + 2 >= self.width or start_y + 2 >= self.height:
                    continue
                open_internal_walls = 0
                total_internal_walls = 0
                for i in range(3):
                    for j in range(3):
                        curr_x = start_x + i
                        curr_y = start_y + j
                        cell = self.grid[curr_x][curr_y]

                        if i < 2:
                            total_internal_walls += 1
                            if cell.walls["EAST"] == 0:
                                open_internal_walls += 1
                        if j < 2:
                            total_internal_walls += 1
                            if cell.walls["SOUTH"] == 0:
                                open_internal_walls += 1
                if total_internal_walls > 0 and (open_internal_walls / total_internal_walls) > 0.8:
                    return True
        return False

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
    maze.fix_isolated_cells()
    if maze.perfect is True:
        while maze.perfect_maker():
            maze.fix_isolated_cells()
    if maze.perfect is False:
        if maze.fix_isolated_cells_nonper() == False:
            generate(maze)
    return maze.find_solution_ways()
