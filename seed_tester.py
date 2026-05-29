import os
import random
import typing
from maze_ing import Maze

def run_interactive_maze(width: int, height: int, seed: typing.Optional[int] = None):
    # --- 1. UYGULAMA DURUM DEĞİŞKENLERİ (STATE) ---
    show_path = True
    color_scheme = 0  # 0: Cyberpunk/Matrix, 1: Retro Arcade
    current_seed = seed

    # Giriş ve çıkış koordinatlarını sabit tutuyoruz (Koddaki kaymayı önlemek için)
    entry_coord = (0, 0)
    exit_coord = (width - 1, height - 1)

    # İlk labirenti mevcut seed ile oluşturuyoruz
    maze = Maze(width, height, entry=entry_coord, exit=exit_coord, perfect=True, seed=current_seed)
    final_paths = maze.generate()
    maze.fix_isolated_cells()

    while True:
        # --- 2. EKRANI TEMİZLE VE BAŞA AL ---
        print("\033[H\033[J", end="")

        # --- 3. DİNAMİK RENK MODLARI ---
        if color_scheme == 0:
            W_WALL   = "\033[90m██\033[0m"     # Parlak Koyu Gri Duvarlar
            BG_GIRIS = "\033[105m  \033[0m"    # Parlak Magenta Giriş
            BG_CIKIS = "\033[106m  \033[0m"    # Parlak Cyan Çıkış
            BG_YOL   = "\033[102m  \033[0m"    # Canlı Yeşil Çözüm Yolu
            BG_42    = "\033[44m  \033[0m"     # Mavi '42' Hücreleri
        else:
            W_WALL   = "\033[44m██\033[0m"     # Klasik Mavi Duvarlar
            BG_GIRIS = "\033[102m  \033[0m"    # Yeşil Giriş
            BG_CIKIS = "\033[101m  \033[0m"    # Kırmızı Çıkış
            BG_YOL   = "\033[103m  \033[0m"    # Sarı Çözüm Yolu
            BG_42    = "\033[100m  \033[0m"    # Gri '42' Hücreleri

        W_EMPTY  = "  "

        solution_set = set(final_paths[0]) if final_paths else set()
        ft_cell_set = set(maze.ft_cell)

        # --- 4. 2D RENDER BUFFER OLUŞTURMA (Görsel Dağılmayı Önler) ---
        buf_w = width * 2 + 1
        buf_h = height * 2 + 1
        render_buffer = [[W_WALL for _ in range(buf_h)] for _ in range(buf_w)]

        for x in range(width):
            for y in range(height):
                cell = maze.grid[x][y]
                rx = x * 2 + 1
                ry = y * 2 + 1

                # Hücre içini boya
                if (x, y) == maze.entry:
                    render_buffer[rx][ry] = BG_GIRIS
                elif (x, y) == maze.exit:
                    render_buffer[rx][ry] = BG_CIKIS
                elif show_path and (x, y) in solution_set:
                    render_buffer[rx][ry] = BG_YOL
                elif cell in ft_cell_set:
                    render_buffer[rx][ry] = BG_42
                else:
                    render_buffer[rx][ry] = W_EMPTY

                # Duvar geçişlerini boya
                if cell.walls["NORTH"] == 0 and ry + 1 < buf_h:
                    render_buffer[rx][ry + 1] = BG_YOL if (show_path and (x, y) in solution_set and (x, y + 1) in solution_set) else W_EMPTY
                if cell.walls["SOUTH"] == 0 and ry - 1 >= 0:
                    render_buffer[rx][ry - 1] = BG_YOL if (show_path and (x, y) in solution_set and (x, y - 1) in solution_set) else W_EMPTY
                if cell.walls["WEST"] == 0 and rx - 1 >= 0:
                    render_buffer[rx - 1][ry] = BG_YOL if (show_path and (x, y) in solution_set and (x - 1, y) in solution_set) else W_EMPTY
                if cell.walls["EAST"] == 0 and rx + 1 < buf_w:
                    render_buffer[rx + 1][ry] = BG_YOL if (show_path and (x, y) in solution_set and (x + 1, y) in solution_set) else W_EMPTY

        # Buffer'ı ekrana bas
        for ry in reversed(range(buf_h)):
            print("".join([render_buffer[rx][ry] for rx in range(buf_w)]))

        # --- 5. MENÜ ARAYÜZÜ ---
        print("\n" + "=" * 35)
        print(f"  A-MAZE-ING (Active Seed: {current_seed})")
        print("=" * 35)
        print("1. Re-generate maze (with current seed)")
        print(f"2. Show/Hide path (Şu an: {'AÇIK' if show_path else 'KAPALI'})")
        print("3. Rotate maze colors")
        print("4. Change/Set seed")
        print("5. Quit")

        # --- 6. HEXADECIMAL MATRİS ---
        print("\n--- LABİRENTİN NİHAİ HEXADECIMAL MATRİSİ ---")
        for y in reversed(range(maze.height)):
            row_hex = [f"{maze.grid[x][y].wallnbr:X}" for x in range(maze.width)]
            print(" ".join(row_hex))

        # --- 7. KULLANICI SEÇİMİ VE DURUM GÜNCELLEME ---
        choice = input("\nChoice? (1-5): ").strip()

        if choice == "1":
            # Mevcut seed parametresi ile yeniden üretim testi
            maze = Maze(width, height, entry=entry_coord, exit=exit_coord, perfect=True, seed=current_seed)
            final_paths = maze.generate()
            maze.fix_isolated_cells()

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            color_scheme = 1 - color_scheme

        elif choice == "4":
            seed_input = input("Enter new integer seed (Leave empty for random/None): ").strip()
            current_seed = int(seed_input) if seed_input.isdigit() else None
            # Yeni seed girildiğinde otomatik olarak haritayı tetikliyoruz
            maze = Maze(width, height, entry=entry_coord, exit=exit_coord, perfect=True, seed=current_seed)
            final_paths = maze.generate()
            maze.fix_isolated_cells()

        elif choice == "5":
            print("\nUygulamadan çıkılıyor. Başarılar!")
            break

# Test çalıştırması (İlk başta 42 seed'i ile başlatıyoruz)
run_interactive_maze(25, 12, seed=42)