from maze_ing import Maze



def convert_path_to_string(path: list[tuple[int, int]]) -> str:
        """
        Output file'a hexten sonra çözüm yolu da yazdırılacak ama elimizde
        hep koordint var onu dönüştürme fonksiyonu
        """
        if not path or len(path) < 2:
            return ""

        direction_letters: list[str] = []

        # Yol üzerindeki koordinatlara bakıcaz
        for i in range(len(path) - 1):
            curr_x, curr_y = path[i]
            next_x, next_y = path[i + 1]

            dx = next_x - curr_x
            dy = next_y - curr_y

            if dx == 0 and dy == 1:
                direction_letters.append("N")
            elif dx == 1 and dy == 0:
                direction_letters.append("E")
            elif dx == 0 and dy == -1:
                direction_letters.append("S")
            elif dx == -1 and dy == 0:
                direction_letters.append("W")
            else:
                raise ValueError(
                    f"Invalid path step: from {path[i]} to {path[i+1]} dne!"  # düzelticez mesajı
                )

        return "".join(direction_letters)  # tüm yönleri tek str içinde toplar


def write_output_file(file_path: str, maze: Maze, shortest_path: list[tuple[int, int]]) -> None:
    """
    Labirenti ve çözüm yolunu subject dökümanında (IV.5) belirtilen katı formatta dosyaya yazar.
    """
    # Yön harflerine dönüştürme
    path_str: str = convert_path_to_string(shortest_path)
    
    file = open(file_path, "w", encoding="utf-8") 
    try:
        # labirent hex format, bizim testerlar da hep reverse basıyordu 
        # hem maze'i hem hex kısmını, burda da öyle yapmak gerekti
        for y in reversed(range(maze.height)):
            row_hex: list[str] = [f"{maze.grid[x][y].wallnbr:X}" for x in range(maze.width)]
            file.write("".join(row_hex) + "\n")
            
        file.write("\n")
        
        # entry \n exit \n solution
        file.write(f"{maze.entry[0]},{maze.entry[1]}\n{maze.exit[0]},"
                   f"{maze.exit[1]}\n{path_str}\n")
    except:
        file.close()  # hata olursa dosyayı kapatıyoruz.

