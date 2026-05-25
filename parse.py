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
        self.solve: list[Cell] = []

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
            self.ft_cell.append(filled)

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
            if temp_cell not in self.ft_cell:
                if "NORTH" not in temp_cell.nowall:
                    temp_cell.nowall.add("NORTH")
                    temp_cell.wall -= 1
                    temp_cell.wall_info[0] = 0
            else:
                broken_cell.nowall.discard("SOUTH")
                broken_cell.wall_info[2] = 1
                broken_cell.wall += 4
        if "EAST" in broken_cell.nowall and x < self.width - 1:
            temp_cell = self.grid[x+1][y]
            if temp_cell not in self.ft_cell:
                if "WEST" not in temp_cell.nowall:
                    temp_cell.nowall.add("WEST")
                    temp_cell.wall -= 8
                    temp_cell.wall_info[3] = 0
            else:
                broken_cell.nowall.discard("EAST")
                broken_cell.wall_info[3] = 1
                broken_cell.wall += 8
        if "WEST" in broken_cell.nowall and x > 0:
            temp_cell = self.grid[x-1][y]
            if temp_cell not in self.ft_cell:
                if "EAST" not in temp_cell.nowall:
                    temp_cell.nowall.add("EAST")
                    temp_cell.wall -= 2
                    temp_cell.wall_info[1] = 0
                else:
                    broken_cell.nowall.discard("WEST")
                    broken_cell.wall_info[1] = 1
                    broken_cell.wall += 2

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

    def build_wall_between(self, cell1_coord: tuple[int, int], cell2_coord: tuple[int, int]):
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        direction = None
        opp_direction = None
        dir_index1: int
        dir_index2: int
        # iki hücrenin birbirine göre hangi hücrede olduğunu kaydedeceğim.

        if x1 == x2 and y2 == y1 + 1:
            direction = "NORTH"
            dir_index1 = 0
            opp_direction = "SOUTH"
            dir_index2 = 2

            # ör: cell2 cell1'in kuzeyinde
        elif x1 == x2 and y2 == y1 - 1:
            direction = "SOUTH"
            dir_index1 = 2
            opp_direction = "NORTH"
            dir_index2 = 0
        elif y1 == y2 and x2 == x1 + 1:
            direction = "EAST"
            dir_index1 = 1
            opp_direction = "WEST"
            dir_index2 = 3
        elif y1 == y2 and x2 == x1 - 1:
            direction = "WEST"
            dir_index1 = 3
            opp_direction = "EAST"
            dir_index2 = 1
        # directiondaki yön cell1'de kapatacağımız, 
        # opp_directiondaki ce cell2'de kapatacağımz yön
        # hücreler komşu değilse None olarak kalırlar bi işlem yapmayız zaten
        if direction and opp_direction:  # None değilse
            c1.nowall.discard(direction)
            c1.wall_info[dir_index1] = 1
            c2.nowall.discard(opp_direction)
            c2.wall_info[dir_index2] = 1
        # burada da duvarları kapatmış olduk aslında

    def find_shortest_way(self, start: tuple[int, int],
                        end: tuple[int, int]) -> list[list[Cell]]:
        line = [[start]]
        # yolları biriktirdiğimiz liste, start ile baslıyor
        start_to_finish: list[list[Cell]] = []

        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
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
        # başka yol varsa kapatiyorum
        all_paths = self.find_shortest_way(start, end)  # tüm yolları depolayalım

        if len(all_paths) <= 1:  # birden fazla yol varsa fonk içine gir
            return

        all_paths(key=len)  # en kısa olandan uzun olana sıraladı
        main_path = all_paths[0]  # en kısa olana ana yol dedim
        main_path_set = set(main_path)  # kümeye çevirdim

        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }

        for path in all_paths[1:]:  # 1. indeksteki yoldan başlıyruz

            for i in range(len(path) - 1):  # alt. yol ilk yoldan ne zaman kopar
                # sonrakini de kontrol ettiğim için -1 tasmasın diye
                curr_cell = path[i]
                next_cell = path[i+1]

                if curr_cell in main_path_set and next_cell not in main_path_set:
                    # su anki hücre ana yolda varsa ama sonraki yolda degilse dur
                    curr_x, curr_y = curr_cell  # hücrelerin koordinatları aldık
                    next_x, next_y = next_cell  # hücrelerimizin yapısında kordinatlarını tutan bi tuple 
                                                # değişkeni var onu kullanırsak daha kolar olur bu arada işimiz

                    # for d, (dx, dy) in moves():  # hangi yönde farklılk olduğunu ara
                    #     if curr_x + dx == next_x and curr_y + dy == next_y:
                    #         target_direction = d
                    #         break
                    # if target_direction:  # bulduysam o hücreyi çekiyoruz
                    #     current_cell = self.grid[curr_x][curr_y]
                    # bu aşamada duvar örme fonksiyonunu yazıp kullanmak
                    # mantıklı olur gibi geldi her seferinde duvar örme
                    # algoritması yazmaktansa sanki -ENP
                    self.build_wall_between(curr_cell.coordinate, next_cell.coordinate)

# burdan sonra current_cell ve next_xell duvarlarının örülmesi gerek


# DFS ile olası tüm çözüm yollarını bul
# Yolları uzunluklarına göre sırala (uzunluklarına göre değil de, kaydedilen yol harici yollar)
# Diğer yolları perfect yoldan kopar
# 2. yolla birlikte koparmaya başla, 2. yoldan giderken perfect yolun dışına çıktığı ilk hücreyi bul
# Ayrıştığı yeri bulunca duvar ör. Simetrik diger hücrenin de duvarını ör.
