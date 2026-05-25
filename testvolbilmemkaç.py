import random

class Cell():
    def __init__(self, x_coord: int, y_coord: int, wall: int):
        self.wall_info: list[int] = [0, 0, 0, 0]  # Index'ler -> 0: NORTH, 1: EAST, 2: SOUTH, 3: WEST
        self.nowall: set[str] = set()
        self.wall = wall
        self.coordinate: tuple[int, int] = (x_coord, y_coord)
        
        # Sayısal wall değerini yönlere çözüyoruz
        if wall >= 8:
            self.wall_info[3] = 1 # WEST duvarı var
            wall -= 8
        else:
            self.nowall.add("WEST")
            
        if wall >= 4:
            self.wall_info[2] = 1 # SOUTH duvarı var
            wall -= 4
        else:
            self.nowall.add("SOUTH")
            
        if wall >= 2:
            self.wall_info[1] = 1 # EAST duvarı var
            wall -= 2
        else:
            self.nowall.add("EAST")
            
        if wall >= 1:
            self.wall_info[0] = 1 # NORTH duvarı var
            wall -= 1
        else:
            self.nowall.add("NORTH")

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.coordinate == other
        return False


class Maze():
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        self.ft_cell: list[Cell] = []
        
        # Başlangıçta her yer 15 (Tamamen duvarla kaplı)
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mc = Cell(x, y, 15)
                current_column.append(mc)
            self.grid.append(current_column)

    def destroy_wall_between(self, cell1_coord: tuple[int, int], cell2_coord: tuple[int, int]):
        """İki hücre arasındaki duvarı ÇİFT TARAFLI olarak kalıcıca yıkar."""
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        
        if x1 == x2 and y2 == y1 + 1: # c2, c1'in Kuzeyinde
            c1.nowall.add("NORTH"); c1.wall_info[0] = 0
            c2.nowall.add("SOUTH"); c2.wall_info[2] = 0
        elif x1 == x2 and y2 == y1 - 1: # c2, c1'in Güneyinde
            c1.nowall.add("SOUTH"); c1.wall_info[2] = 0
            c2.nowall.add("NORTH"); c2.wall_info[0] = 0
        elif y1 == y2 and x2 == x1 + 1: # c2, c1'in Doğusunda
            c1.nowall.add("EAST");  c1.wall_info[1] = 0
            c2.nowall.add("WEST");  c2.wall_info[3] = 0
        elif y1 == y2 and x2 == x1 - 1: # c2, c1'in Batısında
            c1.nowall.add("WEST");  c1.wall_info[3] = 0
            c2.nowall.add("EAST");  c2.wall_info[1] = 0

    def random_broker(self, x: int, y: int):
        wallnbr: int = random.randint(0, 14)
        # Mevcut hücreyi kırılmış haliyle grid'e koyuyoruz
        self.grid[x][y] = Cell(x, y, wallnbr)
        
        # Hücrenin kendi içinden açılan yönleri komşularıyla ÇİFT TARAFLI senkronize ediyoruz
        if "NORTH" in self.grid[x][y].nowall and y < self.height - 1:
            self.destroy_wall_between((x, y), (x, y + 1))
        if "SOUTH" in self.grid[x][y].nowall and y > 0:
            self.destroy_wall_between((x, y), (x, y - 1))
        if "EAST" in self.grid[x][y].nowall and x < self.width - 1:
            self.destroy_wall_between((x, y), (x + 1, y))
        if "WEST" in self.grid[x][y].nowall and x > 0:
            self.destroy_wall_between((x, y), (x - 1, y))

    def build_wall_between(self, cell1_coord: tuple[int, int], cell2_coord: tuple[int, int]):
        """İki hücre arasına ÇİFT TARAFLI olarak duvar örer (Yolu kapatır)."""
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        
        if x1 == x2 and y2 == y1 + 1:
            c1.nowall.discard("NORTH"); c1.wall_info[0] = 1
            c2.nowall.discard("SOUTH"); c2.wall_info[2] = 1
        elif x1 == x2 and y2 == y1 - 1:
            c1.nowall.discard("SOUTH"); c1.wall_info[2] = 1
            c2.nowall.discard("NORTH"); c2.wall_info[0] = 1
        elif y1 == y2 and x2 == x1 + 1:
            c1.nowall.discard("EAST");  c1.wall_info[1] = 1
            c2.nowall.discard("WEST");  c2.wall_info[3] = 1
        elif y1 == y2 and x2 == x1 - 1:
            c1.nowall.discard("WEST");  c1.wall_info[3] = 1
            c2.nowall.discard("EAST");  c2.wall_info[1] = 1

    def find_solution_ways(self, start: tuple[int, int],
                        end: tuple[int, int]) -> list[list[tuple[int, int]]]:
        line = [[start]]
        start_to_finish: list[list[tuple[int, int]]] = []
        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        
        dir_to_idx = {"NORTH": 0, "EAST": 1, "SOUTH": 2, "WEST": 3}
        opposite_dir = {"NORTH": 2, "EAST": 3, "SOUTH": 0, "WEST": 1}

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

                if 0 <= next_coord[0] < self.width and 0 <= next_coord[1] < self.height:
                    if next_coord not in path:
                        next_cell = self.grid[next_coord[0]][next_coord[1]]
                        
                        my_wall_idx = dir_to_idx[direction]
                        opp_wall_idx = opposite_dir[direction]
                        
                        # Çift taraflı duvar güvenliği kontrolü
                        if current_cell.wall_info[my_wall_idx] == 0 and next_cell.wall_info[opp_wall_idx] == 0:
                            new_path = list(path)
                            new_path.append(next_cell.coordinate)
                            line.append(new_path)
        return start_to_finish

    def perfect_maker(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        all_paths = self.find_solution_ways(start, end)

        if len(all_paths) <= 1:
            return False

        all_paths.sort(key=len)
        main_path = all_paths[0]
        main_path_set = set(main_path)

        for path in all_paths[1:]:
            for i in range(len(path) - 1):
                curr_cell = path[i]
                next_cell = path[i+1]

                if curr_cell in main_path_set and next_cell not in main_path_set:
                    self.build_wall_between(curr_cell, next_cell)
                    return True
        return False
    
    def draw_maze(self, start: tuple[int, int], end: tuple[int, int]):
        all_paths = self.find_solution_ways(start, end)
        solution_set = set(all_paths[0]) if all_paths else set()

        print("\n=== ÇÖZÜM YOLU GÖSTERİLEN LABİRENT ===")
        for y in reversed(range(self.height)):
            # 1. Satır: Kuzey Duvarları
            top_line = ""
            for x in range(self.width):
                cell = self.grid[x][y]
                top_line += "+---" if cell.wall_info[0] == 1 else "+   "
            print(top_line + "+")

            # 2. Satır: İç Boşluklar ve Batı/Doğu sınırları
            mid_line = ""
            for x in range(self.width):
                cell = self.grid[x][y]
                left_wall = "| " if cell.wall_info[3] == 1 else "  "
                
                if cell.coordinate == start:
                    center = "S"
                elif cell.coordinate == end:
                    center = "E"
                elif cell.coordinate in solution_set:
                    center = "."
                else:
                    center = " "
                
                mid_line += left_wall + center + " "
            print(mid_line + "|")
            
        print("+---" * self.width + "+")


# --- ENTEGRE ÇALIŞTIRMA ---
maze = Maze(8, 8) # Test için ideal boyut
start_point = (0, 0)
end_point = (7, 7)

# Haritayı rastgele kırıyoruz
for x in range(maze.width):
    for y in range(maze.height):
        maze.random_broker(x, y)

# İlk kırmada şansımıza yol çıkmadıysa, en az 1 yol çıkana kadar tekrar kur
initial_paths = maze.find_solution_ways(start_point, end_point)
while len(initial_paths) == 0:
    for x in range(maze.width):
        for y in range(maze.height):
            maze.random_broker(x, y)
    initial_paths = maze.find_solution_ways(start_point, end_point)

print("Alternatif yollar kapatılıyor, labirent kusursuzlaştırılıyor...")
while maze.perfect_maker(start_point, end_point):
    pass

print("Tebrikler! Tek çözümlü (Kusursuz) haritanız başarıyla üretildi!")
maze.draw_maze(start_point, end_point)