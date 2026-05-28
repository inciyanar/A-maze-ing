import random
import pars_ing
import typing


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.coordinate = (x, y)
        
        #  OTOMATİK KAPALI BAŞLANGIÇ: Her hücre doğarken dört tarafı duvarla kaplı (1) doğar.
        self.walls = {"NORTH": 1, "EAST": 1, "SOUTH": 1, "WEST": 1}

    @property
    def wallnbr(self) -> int:
        """Duvarlar anlık olarak açılıp kapandıkça bu sayı CANLI olarak güncellenir."""
        return (self.walls["NORTH"] * 1) + \
               (self.walls["EAST"]  * 2) + \
               (self.walls["SOUTH"] * 4) + \
               (self.walls["WEST"]  * 8)

    def get_hex_value(self) -> str:
        """Hexadecimal çıktı için her an güncel canlı sayıyı kullanır."""
        return hex(self.wallnbr).upper()


class Maze():
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                  exit: tuple[int, int], perfect: bool,
                  seed: typing.Optional[int] = None):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        self.ft_cell: list[Cell] = []
        self.perfect = perfect
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.outer_walls: set[tuple[tuple[int, int], str]] = set()  # !hangi koordinatta hangi yönde duvar zorunlu diye bakıcaz
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mazecell = Cell(x, y)
                current_column.append(mazecell)
            self.grid.append(current_column)
        self.out_wall()
        self.ft_write()  # bu ikisini direkt burda da en başta kararlaştırabilirmişiz
    def ft_write(self) -> None:
        if self.width >= 8 and self.height >= 6:
            a: int = (self.width - 7) // 2  # // yapınca int'e kesiyo
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
                    self.ft_cell.append(self.grid[a + x][b + y])  # b+y dediğimizde -'li koordinatlar geliyor o yüzden - dememiz lazım ama emin değilim

    def out_wall(self):
        for x in range(self.width):
            # En alt satırın SOUTH duvarı
            self.outer_walls.add(((x, 0), "SOUTH"))
            # En üst satırın NORTH duvarı
            self.outer_walls.add(((x, self.height - 1), "NORTH"))
        for y in range(self.height):
            # En sol sütunun WEST duvarı
            self.outer_walls.add(((0, y), "WEST"))
            # En sağ sütunun EAST duvarı
            self.outer_walls.add(((self.width - 1, y), "EAST"))

    def destroy_wall(self, cell1_coord: tuple[int, int],
                             cell2_coord: tuple[int, int]) -> None:
            """İki hücre arasındaki duvarı ÇİFT TARAFLI olarak yıkar (0 yapar)."""
            x1, y1 = cell1_coord
            x2, y2 = cell2_coord
            c1 = self.grid[x1][y1]
            c2 = self.grid[x2][y2]
            #####DIŞ DUVARI YIKMIYORUZ HİÇ, içerdeki iki if onun için!!
            if x1 == x2 and y2 == y1 + 1:     # c2, c1'in Kuzeyinde
                if (cell1_coord, "NORTH") in self.outer_walls:
                    if (cell2_coord, "SOUTH") in self.outer_walls: 
                        return
                c1.walls["NORTH"] = 0
                c2.walls["SOUTH"] = 0
            elif x1 == x2 and y2 == y1 - 1:   # c2, c1'in Güneyinde
                if (cell1_coord, "SOUTH") in self.outer_walls:
                    if (cell2_coord, "NORTH") in self.outer_walls:
                        return
                c1.walls["SOUTH"] = 0
                c2.walls["NORTH"] = 0
            elif y1 == y2 and x2 == x1 + 1:   # c2, c1'in Doğusunda
                if (cell1_coord, "EAST") in self.outer_walls:
                    if (cell2_coord, "WEST") in self.outer_walls:
                        return
                c1.walls["EAST"] = 0
                c2.walls["WEST"] = 0
            elif y1 == y2 and x2 == x1 - 1:   # c2, c1'in Batısında
                if (cell1_coord, "WEST") in self.outer_walls:
                    if (cell2_coord, "EAST") in self.outer_walls:
                        return
                c1.walls["WEST"] = 0
                c2.walls["EAST"] = 0

    def build_wall(self, cell1_coord: tuple[int, int],
                           cell2_coord: tuple[int, int]) -> bool:
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        # iki hücrenin birbirine göre hangi hücrede olduğunu kaydedeceğim.

        if x1 == x2 and y2 == y1 + 1: 
            if c1.walls["NORTH"] != 1 and c2.walls["SOUTH"] != 1:
                 # c2, c1'in Kuzeyinde
                c1.walls["NORTH"] = 1
                c2.walls["SOUTH"] = 1
                return True
        elif x1 == x2 and y2 == y1 - 1:   # c2, c1'in Güneyinde
            if c1.walls["SOUTH"] != 1 and c2.walls["NORTH"] != 1:     # c2, c1'in Kuzeyinde
                c1.walls["SOUTH"] = 1
                c2.walls["NORTH"] = 1
                return True
        elif y1 == y2 and x2 == x1 + 1:   # c2, c1'in Doğusunda
            if c1.walls["EAST"] != 1 and c2.walls["WEST"] != 1:
                c1.walls["EAST"] = 1
                c2.walls["WEST"] = 1
                return True
        elif y1 == y2 and x2 == x1 - 1:   # c2, c1'in Batısında
            if c1.walls["WEST"] != 1 and c2.walls["EAST"] != 1:
                c1.walls["WEST"] = 1
                c2.walls["EAST"] = 1
                return True
        return False
        # burada da duvarları açmış olduk aslında

    def create_guaranteed_path(self) -> list[tuple[int, int]]:
            """
            START'tan END'e kadar rastgele yol oluşturan fonksiyon
            """
            start = self.entry 
            end = self.exit
            path = [start]
            visited = {start}
            current = start
            
            moves = {"NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)}
            
            while current != end:
                curr_x, curr_y = current
                directions = ["NORTH", "EAST", "SOUTH", "WEST"]
                random.shuffle(directions)
                
                moved = False
                for direction in directions:
                    dx, dy = moves[direction]
                    next_x, next_y = curr_x + dx, curr_y + dy
                    next_coord = (next_x, next_y)
                    
                    # Sınırlar içinde mi ve daha önce bu garanti yol üstünde basıldı mı?
                    if 0 <= next_x < self.width and 0 <= next_y < self.height:
                        next_cell = self.grid[next_x][next_y]
                        if next_cell not in self.ft_cell:
                            if next_coord not in visited:
                                
                                # Geçici olarak duvarı yık
                                self.destroy_wall(current, next_coord)
                                # Her şey temizse patikayı ilerlet
                                visited.add(next_coord)
                                path.append(next_coord)
                                current = next_coord
                                moved = True
                                break
                # Eğer çıkmaz sokağa girip sıkışırsa diye moved 
                # kullandık, ör 4x4 lük haritada (3,4)->(4,4) yaptık 
                # (4,3)'e de önceden uğramışsak kitleniyo maze ondan
                if not moved:
                    path.pop()
                    if path:
                        current = path[-1]
                    else:
                        # Sıfırlanma durumu (Çok sıkışırsa baştan başlasın)
                        current = start
                        path = [start]
                        visited = {start}
                        
            return path

    def random_broker(self, break_count: int = 2) -> None:
        """
        Haritadaki her iç hücre için belirlenen adet (break_count) kadar 
        rastgele iç duvarı yıkar. Belki sonra gerekir diye buraya break_c
        yazdım ama kullanmayadabiliriz hiç. 
        Dış sınır duvarlarına (ft_cell) dokunmaz.
        """
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        # Tüm iç hücreleri geziyoruz.
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                current_cell = self.grid[x][y]
                if current_cell not in self.ft_cell:
                    cell_break_count = random.randint(1, 4)  # o hicrede kaç duvar yıkacağımı seçiyorum

                    chosen_directions = random.sample(directions,
                                                      cell_break_count)  #yıkacağım duvar sayısı kadar random yön listesinden seçtim
                    
                    for direction in chosen_directions:
                        if current_cell.walls[direction] == 0:
                            continue
                        dx, dy = moves[direction]
                        next_x, next_y = x + dx, y + dy
                        if 0 <= next_x < self.width and 0 <= next_y < self.height:
                            next_cell = self.grid[next_x][next_y]
                            if next_cell not in self.ft_cell:
                                self.destroy_wall((x, y), (next_x, next_y))

# optimizasyon için sadece 2 line değiştirmekten bahsetti ai 228, 237. 
    def find_solution_ways(self) -> list[list[tuple[int, int]]]:
        start = self.entry 
        end = self.exit
        line = [[start]]  # optimizasyon için: line = deque([[start]])
        # yolları biriktirdiğimiz liste, start ile baslıyor
        start_to_finish: list[list[tuple[int, int]]] = []

        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        opposite_dir = {"NORTH": "SOUTH", "EAST": "WEST", "SOUTH": "NORTH", "WEST": "EAST"}
        while line:  # yol bitene kadar çalış
            path = line.pop(0)  # 0. indeksteki elemanı get. artık listede yok 
            # optimizasyon için: path = line.popleft()
            current = path[-1]  # son eleman demek oluyor.
            if current == end:  # çıkısa geldim mi kontrolü
                start_to_finish.append(path)
                continue  # geldiysem while'a dönüş

            curr_x, curr_y = current
            current_cell = self.grid[curr_x][curr_y]

            # selfgrid üzerinden hücrenin bilgilerini çekiyorum

            for direction, has_wall in current_cell.walls.items():
                # o hücrenin yönlerine tek tek bakıcaz, 
                # sözlük olarak tuterken items key-value çiftlerini
                # ikili ikili getiriyor
                if has_wall == 0:
                # Eğer MEVCUT hücremizde o yönde duvar YOKSA (0 ise) o yöne hamle yapabiliriz
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
                                if current_cell.walls[direction] == 0 and next_cell.walls[opposite_dir[direction]] == 0:
                                    new_path = list(path)
                                    # mecvut koordinatı kaydettim
                                    new_path.append(next_cell.coordinate)
                                    # bir sonraki HÜCRENİN koordinatını listeye ekledim
                                    line.append(new_path)
                                    # yeni yolu yol listesinde kaydettim.
        return start_to_finish

# find_solution_ways için daha optimize çalışabilmesi için deque diye bir yapı
# önerdi ai fatihle deniz de böyle bir şeyden bahsediyordu ne olduğuna bakıcam
# şimdi tester ile denerken çok yavaş maze basıyor hatta büyük mazeleri hiç 
# basmıyor sebep bu olabilir bi araştıralım

    def perfect_maker(self) -> bool:
        # başka yol varsa kapatiyorum
        wall_built = False
        while True:
            all_paths = self.find_solution_ways()  # tüm yolları depolayalım
            
            if len(all_paths) <= 1:
                break  # Eğer 1 veya daha az yol kaldıysa labirent artık perfect'tir, döngüden çık!

            all_paths.sort(key=len)  # en kısa olandan uzun olana sıraladı
            main_path = all_paths[0]  # en kısa olana ana yol dedim
            main_path_set = set(main_path)  # kümeye çevirdim
            this_turn_built = False  # geçerli yolda duvar örülüp örülmediğine bakıyor, örüldüyse diğer yola gitmek için
            for path in all_paths[1:]:  # 1. indeksteki yoldan başlıyruz
                for i in range(len(path) - 1):  # alt. yol ilk yoldan ne zaman kopar
                    # sonrakini de kontrol ettiğim için -1 tasmasın diye
                    curr_cell = path[i]
                    next_cell = path[i+1]
                    if curr_cell in main_path_set and next_cell not in main_path_set:
                        if self.build_wall(curr_cell, next_cell) == True:
                            this_turn_built = True
                            wall_built = True  
                            # döngünün en başına dönüldüğünde this_turn_buillt
                            #  sıfırlanacak ama biz en az bile bir duvar 
                            # ördüysek return True edebilmek iiçin bunu 
                            # kullanıyoruz
                            break # İçteki for'u kır, bir sonraki alternatife git (veya while başına dön)
                if this_turn_built:
                    break # Bu alternatif yollardan birine duvar ördük, harita değişti! 
                      # O yüzden alt yolları gezmeyi bırakıp, en dıştaki while başına dönüp 
                      # find_solution_ways()'i taze verilerle yeniden çalıştırmak için burayı da kırıyoruz.
        return wall_built

    def fix_isolated_cells(self) -> bool:
        """
        Perfect_maker çalıştıktan sonra haritayı son bir kez tarar.
        4 duvarı da kapalı kalmış hücreleri bulur ve onları rastgele 
        bir iç komşusuna bağlar.
        """
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        any_cell_fixed = False  # Eğer bi hücre düzeltildiyse perfect_cell tekrar çalışsın diye
        for x in range(self.width):
            for y in range(self.height):
                current_cell = self.grid[x][y]
                # Eğer hücre ft_cell listesinde değilse ve 4 duvarı da tamamen kapalıysa (15)
                if current_cell not in self.ft_cell and current_cell.wallnbr == 15:
                    # Hücreyi kurtarmak için yönleri karıştırıp bir komşu arıyoruz
                    random.shuffle(directions)
                    for direction in directions:
                        dx, dy = moves[direction]
                        next_x, next_y = x + dx, y + dy
                        if 0 <= next_x < self.width:
                            if 0 <= next_y < self.height:
                                next_cell = self.grid[next_x][next_y]
                        else:
                            continue
                        if 0 <= next_x < self.width:
                            if 0 <= next_y < self.height:
                                if next_cell not in self.ft_cell:
                                    self.destroy_wall((x, y),
                                                      (next_x, next_y))
                                    any_cell_fixed = True
                                    break # Tek bir duvar yıkıp kurtarmamız yeterli, sonraki hücreye geç
        return any_cell_fixed

    def chechker_3x3(self) -> bool:
        start_x = self.entry[0]
        start_y = self.entry[1]
        # bu if blokunu nasıl kısaltacagımı bilmiyorum :()
        if start_x < 0 or start_y < 0:
            return False  # burada dış sınırlara taşıyor mu diye baktım
        if start_x + 2 >= self.width or start_y + 2 >= self.height:
            return False
        for i in range (3):  # tüm 3x3 luk alanı gezmek için dongu
            for j in range (3):
                curr_cell = self.grid[start_x + i][ start_y + j]
                # incelenen hücreyi çektim
                if j < 2 and curr_cell.walls["NORTH"] == 1:
                    # en üstteki haric duvarların kuzeyi kapalı mı?
                    return False
                if i < 2 and curr_cell.walls["EAST"] == 1: 
                    # en batıdaki haric duvaların batısı kapalı mı? wall_info[1]
                    return False
                if j > 2 and curr_cell.walls["SOUTH"] == 1:  # wall_info[2]
                    return False
                if i > 2 and curr_cell.walls["WEST"] == 1:  # wall_info[3]
                    return False
        return True

    def generate(self):
        self.ft_write()
        self.create_guaranteed_path()
        self.random_broker()
        while True:
            while self.perfect_maker():
                pass
            cells_fixed = self.fix_isolated_cells()
            if not cells_fixed:
                break
        return self.find_solution_ways()