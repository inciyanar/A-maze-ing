# # =====================================================================
# # 🛠️ YENİLENMİŞ LABİRENT TEST VE MATRİS MOTORU
# # =====================================================================
# from maze_ing import Maze

# def run_perfect_maze_test(width: int, height: int):
#     # 1. Labirenti Kur (Giriş ve Çıkışı sınırların içine aldık)
#     maze = Maze(width, height, entry=(0, 0), exit=(width - 1, height - 1), perfect=True, seed=None)
#     start_point = maze.entry
#     end_point = maze.exit

#     print(f"🎲 {width}x{height} boyutlarında yeni bir labirent inşa ediliyor...")
#     final_paths = maze.generate()
#     maze.fix_isolated_cells()

#     # 5. Kesin Kontrol ve Raporlama

#     print("\n" + "="*20 + " KESİN TEST SONUCU " + "="*20)
#     if len(final_paths) == 1:
#         print(f"✅ BAŞARILI: Labirent 'Kusursuz (Perfect)' standartlara ulaştı!")
#         print(f"🎯 Çözüm Yolu Sayısı: {len(final_paths)} (Tam istediğimiz gibi TEK çözümlü)")
#         print(f"🏁 Çözüm Patikası Uzunluğu: {len(final_paths[0])} Hücre")
#     elif len(final_paths) == 0:
#         print("❌ BAŞARISIZ: Kurtarma esnasında ana yol kazara tamamen kilitlendi!")
#     else:
#         print(f"❌ BAŞARISIZ: Haritada hâlâ birden fazla ({len(final_paths)}) çözüm yolu var!")
#     print("="*59 + "\n")

#     # 6. Haritayı Konsola Çizdirme (Kartezyen Uyumlu: y yukarı doğru artar)
#     solution_set = set(final_paths[0]) if final_paths else set()
#     ft_cell_set = set(maze.ft_cell)

#     print("--- LABİRENTİN GÖRSEL HARİTASI ---")
#     print(" (S: Başlangıç, E: Bitiş, * : Çözüm Yolu, 42: Özel Yazı Hücreleri )\n")

#     for y in reversed(range(maze.height)):
#         # Kuzey Duvarları çizimi
#         top_line = ""
#         for x in range(maze.width):
#             cell = maze.grid[x][y]
#             top_line += "+---" if cell.walls["NORTH"] == 1 else "+   "
#         print(top_line + "+")

#         # Batı Duvarları ve Hücre Gövdeleri çizimi
#         mid_line = ""
#         for x in range(maze.width):
#             cell = maze.grid[x][y]
#             left_wall = "| " if cell.walls["WEST"] == 1 else "  "

#             # Hücrenin içinde ne görüneceğini seçiyoruz
#             if (x, y) == start_point:
#                 char = "S "
#             elif (x, y) == end_point:
#                 char = "E "
#             elif (x, y) in solution_set:
#                 char = "* "
#             elif cell in ft_cell_set:
#                 char = "42"  # 42 yazısına ait hücreleri haritada görebilmek için
#             else:
#                 char = "  "
#             mid_line += left_wall + char
#         # Haritanın en sağ (Doğu) sınır duvarı kapatması
#         print(mid_line + "|")

#     # En alt taban (Güney) sınır çizgisi
#     bottom_line = ""
#     for x in range(maze.width):
#         cell = maze.grid[x][0]
#         bottom_line += "+---" if cell.walls["SOUTH"] == 1 else "+   "
#     print(bottom_line + "+")

#     # 7. Hexadecimal Matris Çıktısı (Canlı wallnbr verisinden beslenir)
#     print("\n--- LABİRENTİN NİHAİ HEXADECIMAL MATRİSİ ---")
#     for y in reversed(range(maze.height)):
#         row_hex = [maze.grid[x][y].get_hex_value() for x in range(maze.width)]
#         print("".join(row_hex))

# # Haritayı 15x11 yapalım ki merkeze yerleşecek olan 42 yazısı rahatça çizilebilsin!
# run_perfect_maze_test(9, 9)


import os
from maze_ing import Maze

def run_interactive_maze(width: int, height: int):
    # --- 1. UYGULAMA DURUM DEĞİŞKENLERİ (STATE) ---
    show_path = True
    color_scheme = 0  # 0: Standart, 1: Alternatif Renk Modu

    # İlk labirenti oluşturuyoruz
    maze = Maze(width, height, entry=(0, 0), exit=(width - 5, height - 7), perfect=True, seed=None)
    final_paths = maze.generate()
    maze.fix_isolated_cells()

    while True:
        # --- 2. EKRANI TEMİZLE VE BAŞA AL ---
        print("\033[H\033[J", end="")

        # --- 3. DİNAMİK RENK MODLARI (Seçenek 3 için) ---
        if color_scheme == 0:
            W_WALL   = "\033[107m  \033[0m"   # Parlak Beyaz Duvar
            BG_GIRIS = "\033[45m  \033[0m"    # Mor Giriş
            BG_CIKIS = "\033[41m  \033[0m"    # Kırmızı Çıkış
            BG_YOL   = "\033[42m  \033[0m"    # Yeşil Çözüm Yolu
        else:
            W_WALL   = "\033[46m  \033[0m"    # Turkuaz Duvar (Alternatif)
            BG_GIRIS = "\033[43m  \033[0m"    # Sarı Giriş
            BG_CIKIS = "\033[101m  \033[0m"   # Açık Kırmızı Çıkış
            BG_YOL   = "\033[44m  \033[0m"    # Mavi Çözüm Yolu

        W_EMPTY  = "  "
        BG_42    = "\033[47m  \033[0m"        # Açık Gri '42' Hücreleri

        solution_set = set(final_paths[0]) if final_paths else set()
        ft_cell_set = set(maze.ft_cell)

        # --- 4. HARİTAYI ÇİZDİR ---
        # Üst Sınır Duvarı
        print(W_WALL * (maze.width * 2 + 1))

        for y in reversed(range(maze.height)):
            # Kuzey Duvarları Satırı
            top_line = ""
            for x in range(maze.width):
                cell = maze.grid[x][y]
                top_line += W_WALL
                top_line += W_WALL if cell.walls["NORTH"] == 1 else W_EMPTY
            print(top_line + W_WALL)

            # Batı Duvarları ve Hücre Gövdeleri Satırı
            mid_line = ""
            for x in range(maze.width):
                cell = maze.grid[x][y]
                mid_line += W_WALL if cell.walls["WEST"] == 1 else W_EMPTY

                # Hücre İçeriği (show_path durumuna göre çözüm yolu gizlenir/açılır)
                if (x, y) == maze.entry:
                    cell_render = BG_GIRIS
                elif (x, y) == maze.exit:
                    cell_render = BG_CIKIS
                elif show_path and (x, y) in solution_set:
                    cell_render = BG_YOL
                elif cell in ft_cell_set:
                    cell_render = BG_42
                else:
                    cell_render = W_EMPTY

                mid_line += cell_render
            print(mid_line + W_WALL)

        # Alt Sınır Duvarı
        print(W_WALL * (maze.width * 2 + 1))

        # --- 5. GÖRSELDEKİ MENÜ ARAYÜZÜ ---
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print(f"2. Show/Hide path from entry to exit (Şu an: {'AÇIK' if show_path else 'KAPALI'})")
        print("3. Rotate maze colors")
        print("4. Quit")

        # --- 6. HEXADECIMAL MATRİS ---
        print("\n--- LABİRENTİN NİHAİ HEXADECIMAL MATRİSİ ---")
        for y in reversed(range(maze.height)):
            row_hex = [f"{maze.grid[x][y].wallnbr:X}" for x in range(maze.width)]
            print("".join(row_hex))

        # --- 7. KULLANICI SEÇİMİNİ AL VE DURUMU GÜNCELLE ---
        choice = input("\nChoice? (1-4): ").strip()

        if choice == "1":
            # Labirenti sıfırdan yeniden üretiyoruz
            maze = Maze(width, height, entry=(0, 0), exit=(width - 1, height - 1), perfect=True, seed=None)
            final_paths = maze.generate()
            maze.fix_isolated_cells()

        elif choice == "2":
            # Çözüm yolunu gösteren boolean değişkeni tersine çeviriyoruz (True -> False -> True)
            show_path = not show_path

        elif choice == "3":
            # Renk paletini değiştiriyoruz (0 -> 1 -> 0)
            color_scheme = 1 - color_scheme

        elif choice == "4":
            print("\nUygulamadan çıkılıyor. Elveda!")
            break

        else:
            # Hatalı girişlerde ekranı hemen yenilemek yerine küçük bir uyarı verilebilir
            pass

# Programı başlatalım
run_interactive_maze(25, 12)
