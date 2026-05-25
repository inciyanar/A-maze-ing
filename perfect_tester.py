import random
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
        if wall >= 1:
            self.wall_info[0] = 1
            # north
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
        # 0 ile 14 arası rastgele kırılmış yeni bir hücre üretiyoruz
        wallnbr: int = random.randint(0, 14)
        broken_cell = Cell(x, y, wallnbr)
        self.grid[x][y] = broken_cell

        # NORTH Kontrolü (Yukarıdaki komşunun SOUTH duvarını yık)
        if "NORTH" in broken_cell.nowall and y < self.height - 1:
            temp_cell = self.grid[x][y+1]
            if temp_cell not in self.ft_cell:
                temp_cell.nowall.add("SOUTH")
                temp_cell.wall_info[2] = 0  # Karşı hücrenin Güney duvarını indir
            else:
                broken_cell.nowall.discard("NORTH")
                broken_cell.wall_info[0] = 1

        # SOUTH Kontrolü (Aşağıdaki komşunun NORTH duvarını yık) -> dürüst sınır kontrolü y > 0
        if "SOUTH" in broken_cell.nowall and y > 0:
            temp_cell = self.grid[x][y-1]
            if temp_cell not in self.ft_cell:
                temp_cell.nowall.add("NORTH")
                temp_cell.wall_info[0] = 0  # Karşı hücrenin Kuzey duvarını indir
            else:
                broken_cell.nowall.discard("SOUTH")
                broken_cell.wall_info[2] = 1

        # EAST Kontrolü (Sağdaki komşunun WEST duvarını yık)
        if "EAST" in broken_cell.nowall and x < self.width - 1:
            temp_cell = self.grid[x+1][y]
            if temp_cell not in self.ft_cell:
                temp_cell.nowall.add("WEST")
                temp_cell.wall_info[3] = 0  # Karşı hücrenin Batı duvarını indir
            else:
                broken_cell.nowall.discard("EAST")
                broken_cell.wall_info[1] = 1

        # WEST Kontrolü (Soldaki komşunun EAST duvarını yık)
        if "WEST" in broken_cell.nowall and x > 0:
            temp_cell = self.grid[x-1][y]
            if temp_cell not in self.ft_cell:
                temp_cell.nowall.add("EAST")
                temp_cell.wall_info[1] = 0  # Karşı hücrenin Doğu duvarını indir
            else:
                broken_cell.nowall.discard("WEST")
                broken_cell.wall_info[3] = 1
    # def choose_next_cell(self, curr_x: int, curr_y: int) -> tuple[int, int]:
    #     direction = random.choice(list(self.grid[curr_x][curr_y].nowall))
    #     if direction == "NORTH":
    #         return [curr_x][curr_y + 1]
    #     if direction == "SOUTH":
    #         return [curr_x][curr_y - 1]
    #     if direction == "EAST":
    #         return [curr_x + 1][curr_y]
    #     if direction == "WEST":
    #         return [curr_x - 1][curr_y]

    # def brokeforsolve(self):
    #     parser = Deneme()
    #     info = parser.parsing()
    #     entry = info["ENTRY"]
    #     entry_parse: list[int] = entry.split(',')

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

    def find_solution_ways(self, start: tuple[int, int],
                        end: tuple[int, int]) -> list[list[tuple[int, int]]]:
        line = [[start]]
        # yolları biriktirdiğimiz liste, start ile baslıyor
        start_to_finish: list[list[tuple[int, int]]] = []

        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        # Yönlerin wall_info listesindeki indeks karşılıkları
        # 0: NORTH, 1: EAST, 2: SOUTH, 3: WEST
        dir_to_idx = {"NORTH": 0, "EAST": 1, "SOUTH": 2, "WEST": 3}
        # Komşu hücrenin bize bakan ters yönleri
        opposite_dir = {"NORTH": 2, "EAST": 3, "SOUTH": 0, "WEST": 1}
        while line:  # yol bitene kadar çalış
            path = line.pop(0)  # 0. indeksteki elemanı get. artık listede yok
            current = path[-1]  # son eleman demek oluyor.
            if current == end:  # çıkısa geldim mi kontrolü
                start_to_finish.append(path)
                continue  # geldiysem while'a dönüş

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
                            next_cell = self.grid[next_coord[0]][next_coord[1]]
                            # hücreyi çekiyorum burda
                            # !!!!!!
                            # Kontrol 1: Mevcut hücrede o yönde duvar var mı? (wall_info kontrolü)
                            # Kontrol 2: Karşıdaki hücrenin bize bakan tarafında duvar var mı?
                            # perfec_testerla denerken bu olmadığı için hata alıp durdum....
                            my_wall_idx = dir_to_idx[direction]  # Kontrol edeceğim yönlerin index'ini alıyorum wall_info'ya bakıcam
                            opp_wall_idx = opposite_dir[direction]
                            if current_cell.wall_info[my_wall_idx] == 0 and next_cell.wall_info[opp_wall_idx] == 0:
                                new_path = list(path)
                                # mecvut koordinatı kaydettim
                                new_path.append(next_cell.coordinate)
                                # bir sonraki HÜCRENİN koordinatını listeye ekledim
                                line.append(new_path)
                                # yeni yolu yol listesinde kaydettim.
        return start_to_finish

  # perfect fonksiyonu harita oluştururken tek yol kalana kadar while içinde
  # çalıştırabilmek için böyle yapsak daha ok dedi ai ısrarla, itaat ettim...
    def perfect_maker(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        # başka yol varsa kapatiyorum
        all_paths = self.find_solution_ways(start, end)  # tüm yolları depolayalım

        if len(all_paths) <= 1:  # birden fazla yol varsa fonk içine gir
            return False

        all_paths.sort(key=len)  # en kısa olandan uzun olana sıraladı
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
                                                # biz find_shortest_way içinde sadece kord listeleri listesi
                                                #tuttuğumuz için olmadı bu bu arada.
                    # for d, (dx, dy) in moves():  # hangi yönde farklılk olduğunu ara
                    #     if curr_x + dx == next_x and curr_y + dy == next_y:
                    #         target_direction = d
                    #         break
                    # if target_direction:  # bulduysam o hücreyi çekiyoruz
                    #     current_cell = self.grid[curr_x][curr_y]
                    # bu aşamada duvar örme fonksiyonunu yazıp kullanmak
                    # mantıklı olur gibi geldi her seferinde duvar örme
                    # algoritması yazmaktansa sanki -ENP
                    self.build_wall_between(curr_cell, next_cell)
                    return True
                    # harita değişti en baştan çağırıcaz güncel halinde o yüzden return
        return False
    

    def draw_maze(self, start: tuple[int, int], end: tuple[int, int]):
            """
            Labirenti çizer ve bulduğu tek çözüm yolunu ' . ' karakterleriyle haritaya işler.
            """
            # Son kalan tek çözümü hesapla
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

                # 2. Satır: İç Boşluklar / Hücre Merkezleri ve Yan Duvarlar
                mid_line = ""
                for x in range(self.width):
                    cell = self.grid[x][y]
                    # Sol duvar kontrolü
                    left_wall = "| " if cell.wall_info[3] == 1 else "  "
                    
                    # Hücre merkezinin ne olacağını belirle
                    if cell.coordinate == start:
                        center = "S"  # Start noktası
                    elif cell.coordinate == end:
                        center = "E"  # End noktası
                    elif cell.coordinate in solution_set:
                        center = "."  # Çözüm yolu patikası
                    else:
                        center = " "  # Boş koridor
                    
                    mid_line += left_wall + center + " "
                print(mid_line + "|")
                
            print("+---" * self.width + "+")

# burdan sonra current_cell ve next_xell duvarlarının örülmesi gerek


# DFS ile olası tüm çözüm yollarını bul
# Yolları uzunluklarına göre sırala (uzunluklarına göre değil de, kaydedilen yol harici yollar)
# Diğer yolları perfect yoldan kopar
# 2. yolla birlikte koparmaya başla, 2. yoldan giderken perfect yolun dışına çıktığı ilk hücreyi bul
# Ayrıştığı yeri bulunca duvar ör. Simetrik diger hücrenin de duvarını ör.


# Labirent nesnesini oluştur (Örn: 15x15)
maze = Maze(5, 5)

# 1. Aşama: Hücreleri random_broker ile rastgele kır
for x in range(maze.width):
    for y in range(maze.height):
        maze.random_broker(x, y)

# Başlangıç ve bitiş koordinatları
start_point = (0, 0)
end_point = (4, 4)

# 2. Aşama: Yapay zekanın ısrar ettiği o meşhur while döngüsü :)
print("Alternatif yollar kapatılıyor, labirent kusursuzlaştırılıyor...")
while maze.perfect_maker(start_point, end_point):
    pass  # perfect_maker True döndüğü sürece döngü devam edecek

print("Tebrikler! Tek çözümlü (Kusursuz) haritanız başarıyla üretildi!")

maze.draw_maze(start_point, end_point)