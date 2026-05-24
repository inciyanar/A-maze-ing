class Cell:
    def __init__(self, x: int, y: int, nowall_list: list[str]):
        self.x = x
        self.y = y
        self.nowall = nowall_list

    # 'if next_coord not in path' kontrolünün tuple ile eşleşmesi için şart:
    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.x, self.y) == other
        return False


# SENİN ORİJİNAL FONKSİYONUN (Hücre tipleri Cell olarak güncellendi)
def find_shortest_way(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[Cell]]:
    line = [[start]]
    start_to_finish: list[list[Cell]] = []

    moves = {
        "NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)
    }

    while line:
        path = line.pop(0)
        current = path[-1]

        if current == end:
            start_to_finish.append(path)
            continue

        curr_x, curr_y = current
        current_cell = self.grid[curr_x][curr_y]

        for direction in current_cell.nowall:
            dx, dy = moves[direction]
            next_coord = (curr_x + dx, curr_y + dy)

            if 0 <= next_coord[0] < self.width:
                if 0 <= next_coord[1] < self.height:
                    if next_coord not in path:
                        new_path = list(path)
                        new_path.append(next_coord)
                        line.append(new_path)
    return start_to_finish


# ADAM GİBİ 4x4 LABİRENT TESTER'I
def run_perfect_maze_test():
    class OriginalMazeStructure:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            # grid[x][y] düzeninde matris başlatma
            self.grid = [[] for _ in range(width)]

    maze_instance = OriginalMazeStructure(width=4, height=4)

    # -------------------------------------------------------------------------
    # SENİN GRID[X][Y] SİSTEMİNE GÖRE KAPILARI TEK TEK ÖRÜYORUZ
    # -------------------------------------------------------------------------

    # SÜTUN 0 (x=0) -> y=0, y=1, y=2, y=3
    maze_instance.grid[0] = [
        Cell(0, 0, ["SOUTH", "EAST"]),
        Cell(0, 1, ["NORTH", "SOUTH"]),
        Cell(0, 2, ["NORTH", "SOUTH"]),
        Cell(0, 3, ["NORTH", "EAST"])
    ]

    # SÜTUN 1 (x=1) -> y=0, y=1, y=2, y=3
    maze_instance.grid[1] = [
        Cell(1, 0, ["WEST", "EAST"]),
        Cell(1, 1, ["SOUTH", "EAST"]),
        Cell(1, 2, ["NORTH", "SOUTH"]),
        Cell(1, 3, ["NORTH", "WEST"])
    ]

    # SÜTUN 2 (x=2) -> y=0, y=1, y=2, y=3
    maze_instance.grid[2] = [
        Cell(2, 0, ["WEST", "SOUTH"]),
        Cell(2, 1, ["NORTH", "WEST", "SOUTH", "EAST"]),
        Cell(2, 2, ["NORTH", "SOUTH", "EAST"]),
        Cell(2, 3, ["NORTH", "EAST"])
    ]

    # SÜTUN 3 (x=3) -> y=0, y=1, y=2, y=3
    maze_instance.grid[3] = [
        Cell(3, 0, ["SOUTH"]),
        Cell(3, 1, ["NORTH", "WEST", "SOUTH"]),
        Cell(3, 2, ["NORTH", "WEST"]),
        Cell(3, 3, ["WEST"])
    ]
    # -------------------------------------------------------------------------

    start_point = (0, 0)
    end_point = (3, 3)

    try:
        sonuclar = find_shortest_way(maze_instance, start_point, end_point)

        print("============ ADAM GİBİ HARİTA TEST SONUÇLARI ============")
        print(f"Toplam Bulunan Yol Sayısı: {len(sonuclar)}\n")

        # Kısa yollar üste gelsin
        sonuclar.sort(key=len)

        for i, yol in enumerate(sonuclar):
            print(f"Yol {i+1} (Uzunluk: {len(yol)} Adım):")
            print(f" -> {yol}\n")

    except Exception as e:
        print(f"Kod çalışırken hata aldı: {e}")


# Testi çalıştır
run_perfect_maze_test()
