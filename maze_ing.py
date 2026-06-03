import random
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
        return f"{self.wallnbr:X}"


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
        self.warning_message: str = ""
        self.entry = entry
        self.exit = exit
        self.outer_walls: set[tuple[tuple[int, int], str]] = set()  # !hangi koordinatta hangi yönde duvar zorunlu diye bakıcaz
        for x in range(self.width):
            current_column: list[Cell] = []
            for y in range(self.height):
                mazecell = Cell(x, y)
                current_column.append(mazecell)
            self.grid.append(current_column)
        if self.seed is not None:
            random.seed(self.seed)  # randoma bağlı kullandığımız fonksiyonların
        #     # random.shuffle(), random.randint() fln, her çalıştırmada aynı seçimi
        #     # yapmasını sağlayan bi işlevi varmış en çok nasıl hallederiz dediğim
        #     # şeyin bu kadar kolay hallolmasına şokum...
        self.out_wall()
        self.ft_write()  # bu ikisini direkt burda da en başta kararlaştırabilirmişiz
    def ft_write(self) -> None:
        if self.width > 8 and self.height > 6:
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
                    if (target_x, target_y) != self.entry and (target_x, target_y) != self.exit:
                        self.ft_cell.append(self.grid[a + x][b + y])  # b+y dediğimizde -'li koordinatlar geliyor o yüzden - dememiz lazım ama emin değilim

            if 0 <= a + 4 < self.width and 0 <= b + 3 < self.height:
                self.destroy_wall((a + 4, b + 3), (a + 3, b + 3))
            if 0 <= a + 7 < self.width and 0 <= b + 1 < self.height:
                self.destroy_wall((a + 6, b + 1), (a + 7, b + 1))
        else:
            with open("debug_log.txt", "w") as f:
                f.write("Error: Maze is too small to fit the 42 sign.\n")  # burada çıktıyı ekrana alamıyorum
                # ben de bi dosyaya yazdirayim dedim.

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

            while current[0] != end[0] or current[1] != end[1]:
                print("selam")
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
                    cell_break_count = random.randint(0, 2)  # o hicrede kaç duvar yıkacağımı seçiyorum,
                                                             # 4 diyince çok da yıkabiliyo 2'ye düşürdüm

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
                                # elimizde checker var ama kullanmamışız ki hiç.... ya buraya
                                # ya da destroy walla ekleyip kontrol etmek lazım ilk burası gelmişti aklıma
                                # şimdi düşününce destroy wall daha mantıklı geldi...... yarın tekrar düşünücem
                                start_x_min = max(0, x - 2)
                                start_x_max = min(self.width - 3, x)
                                start_y_min = max(0, y - 2)
                                start_y_max = min(self.height - 3, y)
                                illegal_area_found = False
                                for sx in range(start_x_min, start_x_max + 1):
                                    for sy in range(start_y_min, start_y_max + 1):
                                        # kontrol ediyoruz!
                                        if self.chechker_3x3():
                                            illegal_area_found = True
                                            break
                                    if illegal_area_found:
                                        break
                                # eğer checker3x3 bir boşluk yakaladıysa duvarı geri örüyoruz
                                if illegal_area_found:
                                    self.build_wall((x, y), (next_x, next_y))

    def get_open_neighbors(self, cell_coord: tuple[int, int]) -> list[tuple[int, int]]:
            x, y = cell_coord
            c1 = self.grid[x][y]
            open_neighbors = []

            if c1.walls.get("NORTH") == 0 and y + 1 < self.height:
                open_neighbors.append((x, y + 1))

            if c1.walls.get("SOUTH") == 0 and y - 1 >= 0:
                open_neighbors.append((x, y - 1))

            if c1.walls.get("EAST") == 0 and x + 1 < self.width:
                open_neighbors.append((x + 1, y))

            if c1.walls.get("WEST") == 0 and x - 1 >= 0:
                open_neighbors.append((x - 1, y))

            return open_neighbors


    def find_solution_ways(self) -> list[list[tuple[int, int]]]:
        start = self.entry
        end = self.exit

        from collections import deque
        queue = deque([ ([start], {start}) ])
        found_paths = []

        visit_counts = {}  # daha efektif çalışsın diye

        while queue:  # iki tane yol bulduysan devamına gerek yok çık buradan
            if len(found_paths) >= 2:
                break

            path, path_set = queue.popleft()
            curr_cell = path[-1]

            if curr_cell == end:
                found_paths.append(path)
                continue

            # bir hücre çok fazla alternatife boğulduysa kurtarıyoruz
            visit_counts[curr_cell] = visit_counts.get(curr_cell, 0) + 1
            if visit_counts[curr_cell] > 4:  # 4'ten fazla kez dallanmaya izin verme
                continue

            # mevcut hücrenini açık olan komsularını al
            for neighbor in self.get_open_neighbors(curr_cell):
                # döngüye girmesini engelle!!
                if neighbor not in path_set:
                    new_path = path + [neighbor]
                    new_path_set = path_set.copy()
                    new_path_set.add(neighbor)
                    queue.append((new_path, new_path_set))

        return found_paths

# optimizasyon için sadece 2 line değiştirmekten bahsetti ai 228, 237.
    # def find_solution_ways(self) -> list[list[tuple[int, int]]]:
    #     start = self.entry
    #     end = self.exit
    #     line = [[start]]  # optimizasyon için: line = deque([[start]])
    #     # yolları biriktirdiğimiz liste, start ile baslıyor
    #     start_to_finish: list[list[tuple[int, int]]] = []

    #     moves = {
    #         "NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)
    #     }
    #     opposite_dir = {"NORTH": "SOUTH", "EAST": "WEST", "SOUTH": "NORTH", "WEST": "EAST"}
    #     while line:  # yol bitene kadar çalış
    #         path = line.pop(0)  # 0. indeksteki elemanı get. artık listede yok
    #         # optimizasyon için: path = line.popleft()
    #         current = path[-1]  # son eleman demek oluyor.
    #         if current == end:  # çıkısa geldim mi kontrolü
    #             start_to_finish.append(path)

    #             if len(start_to_finish) >= 2:
    #                 return start_to_finish
    #             continue  # geldiysem while'a dönüş

    #         curr_x, curr_y = current
    #         current_cell = self.grid[curr_x][curr_y]

    #         # selfgrid üzerinden hücrenin bilgilerini çekiyorum

    #         for direction, has_wall in current_cell.walls.items():
    #             # o hücrenin yönlerine tek tek bakıcaz,
    #             # sözlük olarak tuterken items key-value çiftlerini
    #             # ikili ikili getiriyor
    #             if has_wall == 0:
    #             # Eğer MEVCUT hücremizde o yönde duvar YOKSA (0 ise) o yöne hamle yapabiliriz
    #                 dx, dy = moves[direction]
    #             # yönü koordinat olarak harekete çeviriyorum.
    #                 next_coord = (curr_x + dx, curr_y + dy)
    #             # gitmek istediğimiz koordinatı oluştruduk
    #                 if 0 <= next_coord[0] < self.width:
    #                     if 0 <= next_coord[1] < self.height:
    #                         # labirentin sınırlarını aştım mı diye bakıyorum
    #                         if next_coord not in path:
    #                             # eğer o hücreye daha önce uğramadıysam
    #                             next_cell = self.grid[next_coord[0]][next_coord[1]]
    #                             if current_cell.walls[direction] == 0 and next_cell.walls[opposite_dir[direction]] == 0:
    #                                 new_path = list(path)
    #                                 # mecvut koordinatı kaydettim
    #                                 new_path.append(next_cell.coordinate)
    #                                 # bir sonraki HÜCRENİN koordinatını listeye ekledim
    #                                 line.append(new_path)
    #                                 # yeni yolu yol listesinde kaydettim.
    #     return start_to_finish

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

            main_edges = set()
            for i in range(len(main_path) - 1):
                # Yönden bağımsız olmak için koordinatları sıralayıp tuple yapıyoruz
                edge = tuple(sorted([main_path[i], main_path[i+1]]))
                main_edges.add(edge)
            this_turn_built = False  # geçerli yolda duvar örülüp örülmediğine bakıyor, örüldüyse diğer yola gitmek için
            for path in all_paths[1:]:  # 1. indeksteki yoldan başlıyruz
                for i in range(len(path) - 1):  # alt. yol ilk yoldan ne zaman kopar
                    # sonrakini de kontrol ettiğim için -1 tasmasın diye
                    curr_cell = path[i]
                    next_cell = path[i+1]
                    edge = tuple(sorted([curr_cell, next_cell]))
                    if edge not in main_edges:
                        attempt = 0
                        while True:
                            attempt += 1
                            # Eğer 50 kere rastgele deneyip kapatacak yer bulamadıysan ekimizdeki i'yi kullanalım
                            if attempt > 50:
                                k = i
                            else:
                                k = random.randint(i, len(path) - 2)
                            # path üzerinde ayrıştıktan sonra random iki kücre arasına duvar öreriz.
                            curr_cell = path[k]
                            next_cell = path[k + 1]
                            edge = tuple(sorted([curr_cell, next_cell]))

                            if edge not in main_edges:
                                if self.build_wall(curr_cell, next_cell) == True:
                                    this_turn_built = True
                                    wall_built = True
                                    # döngünün en başına dönüldüğünde this_turn_buillt
                                    #  sıfırlanacak ama biz en az bile bir duvar
                                    # ördüysek return True edebilmek için bunu
                                    # kullanıyoruz
                                    break # İçteki while'ı kırıyoruz dıştaki for'a geçiyor
                    if this_turn_built:
                        break
                if this_turn_built:
                    break # Bu alternatif yollardan birine duvar ördük, harita değişti!
                      # O yüzden alt yolları gezmeyi bırakıp, en dıştaki while başına dönüp
                      # find_solution_ways()'i taze verilerle yeniden çalıştırmak için burayı da kırıyoruz.
            flag = True
        return wall_built

    """ def fix_isolated_cells(self) -> bool:

        Perfect_maker çalıştıktan sonra haritayı son bir kez tarar.
        4 duvarı da kapalı kalmış hücreleri bulur ve onları rastgele
        bir iç komşusuna bağlar.

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
 """
    from collections import deque  # çektim ama tanımadı, neden anlamadım

    def fix_isolated_cells(self) -> bool:

        # bu fonksiyonda girişten başlayarak ulaşabildigimiz tüm hücrelere ulaşıyoruz,
        # ulaşamadıklarımız isolated demektir.
        start_coord = self.entry
        visited = set()  # ziyaret edilen yerlerin kümesi, bu olmadıgı için patladık

        tail = self.deque([start_coord])  # deque olan bir kuyruk ekliyorum.
        # bu kuyruk kontrol edilecek olan hücreleri tutuyor, tek tek buradan alıp
        # döngüye sokuyoruz
        visited.add(start_coord)

        moves = {"NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)}

        # kuyrukta hücre kalmayana kadar devam et
        while tail:
            curr_x, curr_y = tail.popleft()  # normalde pop kullanmıştık, deque oldugu
            # için artık popleft, kuyrugun en önü oluyor.buradan hücre çekiyorum
            curr_cell = self.grid[curr_x][curr_y]

            for direction, (dx, dy) in moves.items():
                if curr_cell.walls.get(direction, 1) == 0:  # yol açık ise
                    nx, ny = curr_x + dx, curr_y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:  # labirent sınırlarındaysa
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))  # ziyaret kümesine ekler
                            tail.append((nx, ny))  # dequenin sonuna ekler

        # artık girişten itibaren ulaşılabilen tüm hücreler visited içinde
        any_cell_fixed = False

        for x in range(self.width):  # tüm haritayı tarıyorum
            for y in range(self.height):
                current_coord = (x, y)

                if current_coord not in visited and self.grid[x][y] not in self.ft_cell:
                    # eğer hücre izole ise, 4 komsusuna bakıyorum random, hangisi visited içinde
                    # onu bulmam lazim
                    directions = list(moves.keys())
                    random.shuffle(directions)

                    for direction in directions:
                        dx, dy = moves[direction]
                        next_x, next_y = x + dx, y + dy
                        next_coord = (next_x, next_y)

                        # hangi komsu oldugunu bulduktan sonra oradaki duvarı yıkıyorum.
                        if 0 <= next_x < self.width and 0 <= next_y < self.height:
                            if next_coord in visited and self.grid[next_x][next_y] not in self.ft_cell:
                                self.destroy_wall(current_coord, next_coord)
                                visited.add(current_coord)
                                any_cell_fixed = True
                                break

        return any_cell_fixed

    def chechker_3x3(self) -> bool:
        start_x = self.entry[0]
        start_y = self.entry[1]
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


def generate(maze: Maze):
    maze.ft_write()
    if any(Cell.coordinate == maze.entry for Cell in maze.ft_cell):
        raise ValueError("Error: Entry coordinates cannot be on the 42 sign.")
    if any(Cell.coordinate == maze.exit for Cell in maze.ft_cell):
        raise ValueError("Error: Exit coordinates cannot be on the 42 sign.")
    maze.create_guaranteed_path()
    maze.random_broker()
    if maze.perfect == True:
        while maze.perfect_maker():
            while True:
                cells_fixed = maze.fix_isolated_cells()
                if not cells_fixed:
                    break
    if maze.perfect == False:
        cells_fixed = True
        while cells_fixed:
            cells_fixed = maze.fix_isolated_cells()
    if maze.warning_message:
        print(maze.warning_message)
    return maze.find_solution_ways()
