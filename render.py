import random
import os
from maze_ing import Maze

class Render():
    def __init__(self) -> None:
        # Sabit el yapımı temalarımızı kurucu metodun içinde tanımlıyoruz
        self.theme: dict[str, str] = {
            "WALL": "\033[38;5;105m██\033[0m",       # mor
            "ENTRY": "\033[105m  \033[0m",     # Magenta
            "EXIT": "\033[106m  \033[0m",      # Cyan
            "PATH": "\033[48;5;210m  \033[0m",      # Neon Yeşil
            "FT_42": "\033[48;5;121m  \033[0m"       # Mavi
        }

    def random_theme(self) -> None:
        # Kontrastın güzel olması ve siyah zemin üzerinde görünmez olmamaları için
        # 16 ile 231 arasındaki canlı/parlak renk havuzunu kullanmak daha okmuş
        wall_color: int = random.randint(16, 231)
        entry_color: int = random.randint(16, 231)
        exit_color: int = random.randint(16, 231)
        path_color: int = random.randint(16, 231)
        ft_color: int = random.randint(16, 231)
        self.theme = {
                "WALL": f"\033[38;5;{wall_color}m██\033[0m",  #buradaki renk işlemlerini note.txt içine sonradan çalışmak için kaydettim bir tık karışık
                "ENTRY": f"\033[48;5;{entry_color}m  \033[0m",
                "EXIT": f"\033[48;5;{exit_color}m  \033[0m",
                "PATH": f"\033[48;5;{path_color}m  \033[0m",
                "FT_42": f"\033[48;5;{ft_color}m  \033[0m"
            }

    def render(self, maze: Maze, show_path: bool = True) -> None:
        """
        Aktif olan güncel temayı (self.current_theme) baz alarak labirenti ekrana çizer.
        """
        # Renkleri doğrudan nesne durumundan çekiyoruz (Parametreden kurtulduk!)
        os.system('cls' if os.name == 'nt' else 'clear')  # Terminali temizle, böylece her render taze başlar
        W_WALL: str = self.theme["WALL"]
        BG_GIRIS: str = self.theme["ENTRY"]
        BG_CIKIS: str = self.theme["EXIT"]
        BG_YOL: str = self.theme["PATH"]
        BG_42: str = self.theme["FT_42"]
        W_EMPTY: str = "  "

        ft_cells = maze.ft_cell
        buf_w: int = maze.width * 2 + 1
        buf_h: int = maze.height * 2 + 1
        found_paths = maze.find_solution_ways()
        solutions = set(found_paths[0])
        # basıldığında düzgün bi görüntü almak için 2x+1 yapıyoruz
        # haritayı böyle olunca bi hücre için:
        # (0,0)Hücre Alanının Render Koordinatları
        # MERKEZ (Hücrenin İçi - Oyacağımız Yer): (1, 1) = (rx, ry)
        # KUZEY (Üst Kapı / Duvar): (1, 2) (ry + 1)
        # GÜNEY (Alt Kapı / Duvar): (1, 0) (ry - 1)
        # DOĞU (Sağ Kapı / Duvar): (2, 1) (rx + 1)
        # BATI (Sol Kapı / Duvar): (0, 1) (rx - 1)
        # gibi oluyo biraz karışık ama halledicem
        render_list: list[list[str]] = [[W_WALL for _ in range(buf_h)] for _ in range(buf_w)]
        # içindeki her bir kareyi en başta tamamen duvarla (W_WALL) dolduruyoruz
        for x in range(maze.width):
            for y in range(maze.height):
                cell = maze.grid[x][y]
                rx = 2 * x + 1
                ry = 2 * y + 1
                # hücre merkezlerini boyama;
                if (x, y) == maze.entry:
                    render_list[rx][ry] = BG_GIRIS  # Giriş koordinatıysa giriş rengine boya
                elif (x, y) == maze.exit:
                    render_list[rx][ry] = BG_CIKIS  # Çıkış koordinatıysa çıkış rengine
                elif show_path and (x, y) in solutions:
                    render_list[rx][ry] = BG_YOL    # En kısa yolsa ve show_path true ise
                elif cell in ft_cells:
                    render_list[rx][ry] = BG_42     # '42' merkezi
                else:
                    render_list[rx][ry] = W_EMPTY   # Normal bir koridorsa buradaki duvarı yık, boşluk yap
                # hücrenin etrafındaki duvarları yönetiyoruz;
                if cell.walls["NORTH"] == 0 and ry + 1 < buf_h:
                    if (show_path
                            and (x, y) in solutions
                            and (x, y + 1) in solutions):
                        render_list[rx][ry + 1] = BG_YOL
                    else:
                        render_list[rx][ry + 1] = W_EMPTY

                if cell.walls["SOUTH"] == 0 and ry - 1 >= 0:
                    if (show_path
                            and (x, y) in solutions
                            and (x, y - 1) in solutions):
                        render_list[rx][ry - 1] = BG_YOL
                    else:
                        render_list[rx][ry - 1] = W_EMPTY

                if cell.walls["WEST"] == 0 and rx - 1 >= 0:
                    if (show_path
                            and (x, y) in solutions
                            and (x - 1, y) in solutions):
                        render_list[rx - 1][ry] = BG_YOL
                    else:
                        render_list[rx - 1][ry] = W_EMPTY

                if cell.walls["EAST"] == 0 and rx + 1 < buf_w:
                    if (show_path
                            and (x, y) in solutions
                            and (x + 1, y) in solutions):
                        render_list[rx + 1][ry] = BG_YOL
                    else:
                        render_list[rx + 1][ry] = W_EMPTY
        # Terminal ekranı yazmaya her zaman en üst satırdan başlarsa
        # her print()'te bir alt satıra kayar. Yani ilk 0. satır ekrana
        # basılır bu olmasın diye y eksenini reversed ediyoruz
        # 5. Terminale Satır Satır Yazdırma (Y ekseni ters çevrilerek)
        for ry in reversed(range(buf_h)):
            print("".join([render_list[rx][ry] for rx in range(buf_w)]))
