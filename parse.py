import sys
import typing
class Deneme():
    def parsing(self):
        file: typing.TextIO = open('config.txt', 'r')
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


if __name__ == "__main__":
    a = Deneme()
    a.parsing()

class Cell():
    def __init__(self, x_coord: int, y_coord: int, wall):
        if(wall >= 8):
            self.west: int = 1
            wall -= 8
        else:
            self.west = 0
        if(wall >=4):
            self.south: int =1
            wall -= 4
        else:
            self.south: int =0
        if(wall >=2):
            self.east: int =1
            wall -= 2
        else:
            self.east: int =0
        if(wall ==1):
            self.north: int =1
        else:
            self.north: int =0
        self.wall = wall
        coordinate: tuple[int, int] = (x_coord, y_coord)


class Maze():
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        x: int
        y: int
        for y in range(self.height):
            current_row: list[Cell] = []
            for x in range(self.width):
                mc = Cell(x, y, 15)
                current_row += mc
            self.grid += current_row

