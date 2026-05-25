import random


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.coordinate = (x, y)
        
        # 🎯 OTOMATİK KAPALI BAŞLANGIÇ: Her hücre doğarken dört tarafı duvarla kaplı (1) doğar.
        self.walls = {
            "NORTH": 1,
            "EAST": 1,
            "SOUTH": 1,
            "WEST": 1
        }

    @property
    def wallnbr(self) -> int:
        """Duvarlar anlık olarak açılıp kapandıkça bu sayı CANLI olarak güncellenir."""
        return (self.walls["NORTH"] * 1) + \
               (self.walls["EAST"]  * 2) + \
               (self.walls["SOUTH"] * 4) + \
               (self.walls["WEST"]  * 8)

    def get_hex_value(self) -> str:
        """Hexadecimal çıktı için her an güncel canlı sayıyı kullanır."""
        return hex(self.wallnbr)[2:].upper()


class Maze():
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]] = []
        self.ft_cell: list[Cell] = []
        
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mazecell = Cell(x, y)
                current_column.append(mazecell)
            self.grid.append(current_column)

    def ft_write(self):
        if self.width >= 9 and self.height >= 7:
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

    def destroy_wall_between(self, cell1_coord: tuple[int, int], cell2_coord: tuple[int, int]):
            """İki hücre arasındaki duvarı ÇİFT TARAFLI olarak kalıcıca yıkar (0 yapar)."""
            x1, y1 = cell1_coord
            x2, y2 = cell2_coord
            c1 = self.grid[x1][y1]
            c2 = self.grid[x2][y2]
            
            if x1 == x2 and y2 == y1 + 1:     # c2, c1'in Kuzeyinde
                c1.walls["NORTH"] = 0
                c2.walls["SOUTH"] = 0
            elif x1 == x2 and y2 == y1 - 1:   # c2, c1'in Güneyinde
                c1.walls["SOUTH"] = 0
                c2.walls["NORTH"] = 0
            elif y1 == y2 and x2 == x1 + 1:   # c2, c1'in Doğusunda
                c1.walls["EAST"] = 0
                c2.walls["WEST"] = 0
            elif y1 == y2 and x2 == x1 - 1:   # c2, c1'in Batısında
                c1.walls["WEST"] = 0
                c2.walls["EAST"] = 0

    def build_wall_between(self, cell1_coord: tuple[int, int],
                           cell2_coord: tuple[int, int]) -> bool:
        x1, y1 = cell1_coord
        x2, y2 = cell2_coord
        c1 = self.grid[x1][y1]
        c2 = self.grid[x2][y2]
        # iki hücrenin birbirine göre hangi hücrede olduğunu kaydedeceğim.

        if x1 == x2 and y2 == y1 + 1: 
            if c2.walls["NORTH"] != 1 and c1.walls["SOUTH"] != 1:     # c2, c1'in Kuzeyinde
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

    def create_guaranteed_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
            """
            START'tan END'e kadar rastgele yol oluşturan fonksiyon
            """
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
                        if next_coord not in visited:
                            
                            # Geçici olarak duvarı yık
                            self.destroy_wall_between(current, next_coord)
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

    def random_broker(self, break_count: int = 2):
        """
        Haritadaki her iç hücre için belirlenen adet (break_count) kadar 
        rastgele iç duvarı yıkar. Dış sınır duvarlarına (ft_cell) asla dokunmaz.
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
                        dx, dy = moves[direction]
                        next_x, next_y = x + dx, y + dy
                        if 0 <= next_x < self.width and 0 <= next_y < self.height:
                            if current_cell.walls[direction] == 1:
                                self.destroy_wall_between((x, y),
                                                          (next_x, next_y))
    
    def find_solution_ways(self, start: tuple[int, int],
                        end: tuple[int, int]) -> list[list[tuple[int, int]]]:
        line = [[start]]
        # yolları biriktirdiğimiz liste, start ile baslıyor
        start_to_finish: list[list[tuple[int, int]]] = []

        moves = {
            "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
        }
        opposite_dir = {"NORTH": "SOUTH", "EAST": "WEST", "SOUTH": "NORTH", "WEST": "EAST"}
        while line:  # yol bitene kadar çalış
            path = line.pop(0)  # 0. indeksteki elemanı get. artık listede yok
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

                    if self.build_wall_between(curr_cell, next_cell) == True:
                        return True
        return False

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
                        next_coord = x + dx, y + dy
                        if 0 <= next_x < self.width and 0 <= next_y < self.height:
                            if next_coord not in self.ft_cell:
                                self.destroy_wall_between((x, y), (next_x, next_y))
                                any_cell_fixed = True
                                break # Tek bir duvar yıkıp kurtarmamız yeterli, sonraki hücreye geç
        return any_cell_fixed

    def check_3x3_blank(self, x: int, y: int) -> bool:
        """ (x,y) deki bir hücrenin 3x3'lük bir yerde center olup olmadığına bakar"""
        if x <= 0 or x >= self.width - 1 or y <= 0 or y >= self.height - 1:
            return False
        curr_cell = self.grid[x][y]
        check_neigborhood: list[tuple[int, int]] = [(1, 0), (-1, 0), (-1, 1), (0,1), (1, 1), (-1, -1), (0, -1), (1, -1)]
        for (dx, dy) in check_neigborhood:

            return False





# =====================================================================
# 🛠️ YENİLENMİŞ LABİRENT TEST VE MATRİS MOTORU
# =====================================================================

def run_perfect_maze_test(width: int, height: int):
    # 1. Labirenti Kur
    maze = Maze(width, height)
    start_point = (0, 0)
    end_point = (width - 1, height - 1)
    
    print(f"🎲 {width}x{height} boyutlarında yeni bir labirent inşa ediliyor...")
    
    # 2. İlk Adım: Garanti Patikayı Çiz
    guaranteed_coords = maze.create_guaranteed_path(start_point, end_point)
    print(f" Patika Oluşturuldu: START -> END arası ilk garanti koridor açıldı.")
    
    # 3. İkinci Adım: Çevre Hücreleri Rastgele Kır (Kaos)
    # Koridor yapısı için random_broker'ı hücre başına 1-2 duvar kıracak şekilde optimize ettik
    maze.random_broker() 
    print("💥 Kaos Yaratıldı: İç hücreler rastgele esnetildi.")
    
    # Budama ve kurtarma öncesi durumu ölçelim
    initial_paths = maze.find_solution_ways(start_point, end_point)
    print(f"🔄 Optimizasyon öncesi alternatif yol sayısı: {len(initial_paths)}")
    
    # 4. Üçüncü Adım: PING-PONG Döngüsü (Kusursuzlaştır & Kurtar)
    print("\n✂️ Optimizasyon ve Kurtarma döngüsü başlatılıyor...")
    iteration = 0
    
    while True:
        iteration += 1
        # A) Kaçak kısayolları ve alternatif döngüleri temizle
        perfect_loops = 0
        while maze.perfect_maker(start_point, end_point):
            perfect_loops += 1
            
        # B) Budamadan sonra 4 duvarı kapalı kalan hücreleri bul ve kurtar
        cells_fixed = maze.fix_isolated_cells()
        
        print(f"  > Tur {iteration}: {perfect_loops} kaçak yol kapatıldı. İzole hücre kurtarıldı mı? -> {cells_fixed}")
        
        # C) Eğer hiçbir izole hücreye dokunulmadıysa mükemmel dengeye ulaştık demektir!
        if not cells_fixed:
            break

    # 5. Kesin Kontrol ve Raporlama
    final_paths = maze.find_solution_ways(start_point, end_point)
    
    print("\n" + "="*20 + " KESİN TEST SONUCU " + "="*20)
    if len(final_paths) == 1:
        print(f"✅ BAŞARILI: Labirent 'Kusursuz (Perfect)' standartlara ulaştı!")
        print(f"🎯 Çözüm Yolu Sayısı: {len(final_paths)} (Tam istediğimiz gibi TEK çözümlü)")
        print(f"🏁 Çözüm Patikası Uzunluğu: {len(final_paths[0])} Hücre")
    elif len(final_paths) == 0:
        print("❌ BAŞARISIZ: Kurtarma esnasında ana yol kazara tamamen kilitlendi!")
    else:
        print(f"❌ BAŞARISIZ: Haritada hâlâ birden fazla ({len(final_paths)}) çözüm yolu var!")
    print("="*59 + "\n")
    
    # 6. Haritayı Konsola Çizdirme
    solution_set = set(final_paths[0]) if final_paths else set()
    print("--- LABİRENTİN GÖRSEL HARİTASI ---")
    print(" (S: Başlangıç, E: Bitiş, * : Çözüm Yolu )")
    
    for y in reversed(range(maze.height)):
        # Üst Duvarlar
        top_line = ""
        for x in range(maze.width):
            cell = maze.grid[x][y]
            top_line += "+---" if cell.walls["NORTH"] == 1 else "+   "
        print(top_line + "+")
        
        # Yan Duvarlar ve Hücre İçleri
        mid_line = ""
        for x in range(maze.width):
            cell = maze.grid[x][y]
            left_wall = "| " if cell.walls["WEST"] == 1 else "  "
            
            if (x, y) == start_point:
                char = "S "
            elif (x, y) == end_point:
                char = "E "
            elif (x, y) in solution_set:
                char = "* "
            else:
                char = "  "
            mid_line += left_wall + char
        print(mid_line + "|")
    print("+---" * maze.width + "+")
    
    # 7. Senin İstediğin Hexadecimal Matris Çıktısı
    print("\n--- LABİRENTİN NİHAİ HEXADECIMAL MATRİSİ ---")
    for y in reversed(range(maze.height)):
        row_hex = [maze.grid[x][y].get_hex_value() for x in range(maze.width)]
        print(" ".join(row_hex))

# Testi 10x10 boyutlarında çalıştırıp sonucu izleyelim
run_perfect_maze_test(5,5)