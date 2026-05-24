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
            self.wall_info[3] = 1
            # west
            wall -= 8
        else:
            self.nowall.add("WEST")
        if wall >= 4:
            self.wall_info[2] = 1
            # south
            wall -= 4
        else:
            self.nowall.add("SOUTH")
        if wall >= 2:
            self.wall_info[1] = 1
            # east
            wall -= 2
        else:
            self.nowall.add("EAST")
        if wall == 1:
            self.wall_info[0] = 1
            # north
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
        a: int = (self.width - 7) / 2
        b: int = (self.height - 5) / 2
        filled = Cell(a, b, 15)
        coord: list[tuple[int, int]] = [(0, 0), (0, -1), (0, -2), (1, -2),
                                        (2, -2), (2, -3), (2, -4), (6, -4),
                                        (5, -4), (4, -4), (4, -3), (4, -2),
                                        (5, -2), (6, -2), (6, -1), (6, 0),
                                        (5, 0), (4, 0)]
        for (x, y) in coord:
            filled = Cell(a+x, b+y, 15)
            self.ft_cell += filled

    def random_broker(self, x: int, y: int):
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
                        temp_cell.wall -= 4
                        temp_cell.wall_info[2] = 0
                        self.grid[x][y+1] = temp_cell
            else:
                broken_cell.nowall.discard("NORTH")
                broken_cell.wall_info[0] = 1
                broken_cell.wall += 1

        if "SOUTH" in broken_cell.nowall and y < self.height - 1:
            temp_cell = self.grid[x][y-1]
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
            return [curr_x][curr_y + 1]
        if direction == "SOUTH":
            return [curr_x][curr_y - 1]
        if direction == "EAST":
            return [curr_x + 1][curr_y]
        if direction == "WEST":
            return [curr_x - 1][curr_y]

    def brokeforsolve(self):
        parser = Deneme()
        info = parser.parsing()
        entry = info["ENTRY"]
        entry_parse: list[int] = entry.split(',')


def find_shortest_way(self, start: tuple[int, int],
                      end: tuple[int, int]) -> list[list[Cell]]:
    line = [[start]]
    # yolları biriktirdiğimiz liste, start ile baslıyor
    start_to_finish: list[list[Cell]] = []

    moves = {
        "NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)
    }

    while line:
        # yol bitene kadar çalış
        path = line.pop(0)
        # 0. indeksteki elemanı get. artık listede değil
        current = path[-1]
        # -1. indeks son eleman demek oluyor.

        if current == end:
            # çıkısa geldim mi dye kontrol ediyorum
            start_to_finish.append(path)
            continue
            # geldiysem dönguyu bitiriyorum

        curr_x, curr_y = current
        current_cell = self.grid[curr_x][curr_y]

        # selfgrid üzerinden hücrenin bilgilerini çekiyorum

        for direction in current_cell.nowall:
            # o hücrenin açık olan her yönüne bak

            dx, dy = moves[direction]
            # yönü koordinat olarak harekete çeviriyorum.
            next_coord = (curr_x + dx, curr_y + dy)
            # gitmek istediğimiz koordinatı oluştruduk

            if 0 <= next_coord[0] < self.width:
                if 0 <= next_coord[1] < self.height:
                    # labirentin sınırlarını aştım mı diye bakıyorum
                    if next_coord not in path:
                        # eğer o hücreye daha önce uğramadıysam
                        new_path = list(path)
                        # mecvut koordinatı kaydettim
                        new_path.append(next_coord)
                        # bir sonraki koordinatı listeye ekledim
                        line.append(new_path)
                        # yeni yolu yol listesinde kaydettim.
    return start_to_finish


def perfect_maker(self, start: tuple[int, int], end: tuple[int, int]):
    # başka yol var mi diye bakıyorum
    shortest_path = self.find_shortest_way(start, end)
    # en kısa yolu bana verdi.
    if not shortest_path:
        # yol yoksa çıktım, error da dondurebiliriz
        return

    path_set = set(shortest_path)
    # yolu kümelere çevirdim.

    for x in range(self.width):
        # tüm satırları dolas
        for y in range(self.height):
            # tüm kolonları dolas
            current_coord = (x, y)
            # bulunduğun hucrenin koordinatını cek
            cell = self.grid(x, y)
            # o hücrenin bilgilerini çek (sanırım nesne muhabetti bu oluyor)
            directions_to_close = []
            # duvar örülecek yönler

        for direction in list(cell.nowall):
            # açık tüm kapılara bakıyoru
            if direction == "NORTH":
                # eğer kapı açık ise
                next_coord = (x, y-1)
                # bir sonraki hücre için koordinatı revize ediyoruz.
            if direction == "SOUTH":
                next_coord = (x, y+1)
            if direction == "EAST":
                next_coord = (x + 1, y)
            if direction == "WEST":
                next_coord = (x-1, y)

            if next_coord not in path_set:
                # galiba burda patladim
                directions_to_close.append(direction, next_coord)


def perfect_maker(self, start: tuple[int, int], end: tuple[int, int]):
    # başka yol var mi diye bakıyorum
    all_paths = []
    # tüm yolları depolayalım
    visited = set()
    # ziyaret edilen hücreler

    def find_all_paths(current, target, current_path):
        if current == target:
            # çıkışa geldiysem
            all_paths.append(list(current_path))
            # tüm yolları kaydet
            return
        visited.add(current)
        # ziyaret ettikçe ekle
        curr_x, curr_y = current
        current_cell = self.grid[curr_x][curr_y]
        # current hücrenin kooridnatlarını aldım

        moves = {  # hareketlerin koordinatlarını öğrettim.
            "NORTH:": (curr_x, curr_y - 1), "SOUTH": (curr_x, curr_y + 1),
            "EAST": (curr_x + 1, curr_y), "WEST": (curr_x - 1, curr_y)
        }

        for direction in current_cell.nowall:
            pass



# DFS ile olası tüm çözüm yollarını bul
# Yolları uzunluklarına göre sırala (uzunluklarına göre değil de, kaydedilen yol harici yollar)
# Diğer yolları perfect yoldan kopar
# 2. yolla birlikte koparmaya başla, 2. yoldan giderken perfect yolun dışına çıktığı ilk hücreyi bul
# Ayrıştığı yeri bulunca duvar ör. Simetrik diger hücrenin de duvarını ör.

