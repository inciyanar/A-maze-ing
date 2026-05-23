import sys
import typing
import random
class Deneme():
    def parsing(self) -> dict[str, str]:
        file_name: str = sys.argv[1]
        file: typing.TextIO = open(file_name, 'r')
        data: str = file.read()
        lines: list[str] = data.splitlines()
        i = 0
        okito: dict[str, str] = {}
        for item in lines:
            splversion = item.split('=')
            okito[splversion[0]] = splversion[1]
            i += 1
        i = 0

        for key, value in okito.items():
            print(f"{key}: {value}")
        return okito


class Cell():
    def __init__(self, x_coord: int, y_coord: int, wall):
        self.wall_info: list[int] = [0, 0, 0, 0]
        self.nowall: set[str] = set()
        self.wall = wall
        self.coordinate: tuple[int, int] = (x_coord, y_coord)
        if wall >= 8:
            self.wall_info[3] = 1  # west
            wall -= 8
        else:
            self.nowall.add("WEST")
        if wall >= 4:
            self.wall_info[2] = 1  # south
            wall -= 4
        else:
            self.nowall.add("SOUTH")
        if wall >= 2:
            self.wall_info[1] = 1  # east
            wall -= 2
        else:
            self.nowall.add("EAST")
        if wall == 1:
            self.wall_info[0] = 1  # north
        else:
            self.nowall.add("NORTH")



class Maze():
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        self.ft_cell: list[Cell] = []
        x: int
        y: int
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mc = Cell(x, y, 15)
                current_column.append(mc)
            self.grid.append(current_column)
        self.solve: set[Cell] = set()

    def ft_write(self):
        a: int = (self.width - 7 ) / 2
        b: int = (self.height - 5) / 2
        filled: Cell = (a, b, 15)
        coord:list[tuple[int, int]] = [(0,0), (0, -1), (0, -2), (1, -2),
        (2, -2), (2, -3), (2, -4), (6, -4), (5, -4), (4, -4), (4, -3),
        (4, -2), (5, -2), (6, -2), (6, -1), (6, 0), (5, 0), (4, 0)]
        for (x, y) in coord:
            filled: Cell = (a+x, b+y, 15)
            self.ft_cell += filled

    def random_broker(self, x: int, y:int):
        wallnbr: int = random.randint(0, 14)
        broken_cell = Cell(x, y, wallnbr)
        self.grid[x][y] = broken_cell
        temp_cell: Cell

        if "NORTH" in broken_cell.nowall:
            temp_cell = self.grid[x][y+1]
            if temp_cell not in self.ft_cell:
                if "SOUTH" not in temp_cell.nowall:
                    if temp_cell not in self.ft_cell:
                        temp_cell.nowall.add("SOUTH")
                        temp_cell.wall += 4
                        temp_cell.wall_info[2] = 0
                        self.grid[x][y-1] = temp_cell
            else:
                broken_cell.nowall.discard("NORTH")
                broken_cell.wall_info[0] = 1
                broken_cell.wall +=1


        if "SOUTH" in broken_cell.nowall and y < self.height - 1:
            temp_cell = self.grid[x][y+1]
            if "NORTH" not in temp_cell.nowall:
                temp_cell.nowall.add("NORTH")
                temp_cell.wall -= 1
                temp_cell.wall_info[0] = 0
        if "EAST" in broken_cell.nowall and x < self.width - 1:
            temp_cell = self.grid[x+1][y]
            if "WEST" not in temp_cell.nowall:
                temp_cell.nowall.add("WEST")
                temp_cell.wall -= 8
                temp_cell.wall_info[3] = 0
        if "WEST" in broken_cell.nowall and x > 0:
            temp_cell = self.grid[x-1][y]
            if "EAST" not in temp_cell.nowall:
                temp_cell.nowall.add("EAST")
                temp_cell.wall -= 2
                temp_cell.wall_info[1] = 0


    def choose_next_cell(self, curr_x: int, curr_y: int) -> tuple[int, int]:
        direction = random.choice(list(self.grid[curr_x][curr_y].nowall))
        if direction == "NORTH":
            return[curr_x][curr_y + 1]
        if direction == "SOUTH":
            return[curr_x][curr_y - 1]
        if direction == "EAST":
            return[curr_x + 1][curr_y]
        if direction == "WEST":
            return[curr_x - 1][curr_y]
        

    def brokeforsolve(self):
        parser = Deneme()
        info = parser.parsing()
        entry = info["ENTRY"]
        entry_parse: list[int] = entry.split(',')


