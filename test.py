# =====================================================================
# 🛠️ YENİLENMİŞ LABİRENT TEST VE MATRİS MOTORU
# =====================================================================
from maze_ing import Maze

def run_perfect_maze_test(width: int, height: int):
    # 1. Labirenti Kur (Giriş ve Çıkışı sınırların içine aldık)
    maze = Maze(width, height, entry=(0, 0), exit=(width - 1, height - 1), perfect=True, seed=None)
    start_point = maze.entry
    end_point = maze.exit
    
    print(f"🎲 {width}x{height} boyutlarında yeni bir labirent inşa ediliyor...")
    final_paths = maze.generate()
    maze.fix_isolated_cells()

    # 5. Kesin Kontrol ve Raporlama
    
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
    
    # 6. Haritayı Konsola Çizdirme (Kartezyen Uyumlu: y yukarı doğru artar)
    solution_set = set(final_paths[0]) if final_paths else set()
    ft_cell_set = set(maze.ft_cell)
    
    print("--- LABİRENTİN GÖRSEL HARİTASI ---")
    print(" (S: Başlangıç, E: Bitiş, * : Çözüm Yolu, 42: Özel Yazı Hücreleri )\n")
    
    for y in reversed(range(maze.height)):
        # Kuzey Duvarları çizimi
        top_line = ""
        for x in range(maze.width):
            cell = maze.grid[x][y]
            top_line += "+---" if cell.walls["NORTH"] == 1 else "+   "
        print(top_line + "+")
        
        # Batı Duvarları ve Hücre Gövdeleri çizimi
        mid_line = ""
        for x in range(maze.width):
            cell = maze.grid[x][y]
            left_wall = "| " if cell.walls["WEST"] == 1 else "  "
            
            # Hücrenin içinde ne görüneceğini seçiyoruz
            if (x, y) == start_point:
                char = "S "
            elif (x, y) == end_point:
                char = "E "
            elif (x, y) in solution_set:
                char = "* "
            elif cell in ft_cell_set:
                char = "42"  # 42 yazısına ait hücreleri haritada görebilmek için
            else:
                char = "  "
            mid_line += left_wall + char
        # Haritanın en sağ (Doğu) sınır duvarı kapatması
        print(mid_line + "|")
        
    # En alt taban (Güney) sınır çizgisi
    bottom_line = ""
    for x in range(maze.width):
        cell = maze.grid[x][0]
        bottom_line += "+---" if cell.walls["SOUTH"] == 1 else "+   "
    print(bottom_line + "+")
    
    # 7. Hexadecimal Matris Çıktısı (Canlı wallnbr verisinden beslenir)
    print("\n--- LABİRENTİN NİHAİ HEXADECIMAL MATRİSİ ---")
    for y in reversed(range(maze.height)):
        row_hex = [maze.grid[x][y].get_hex_value() for x in range(maze.width)]
        print(" ".join(row_hex))

# Haritayı 15x11 yapalım ki merkeze yerleşecek olan 42 yazısı rahatça çizilebilsin!
run_perfect_maze_test(9, 9)