import sys
from pars_ing import ConfigParser
from maze_ing import Maze, generate
from output_file_helpers import write_output_file
from render import Render


def run_maze_render(maze: Maze) -> None:
    """
    Dökümandaki Chapter V kurallarına birebir uyumlu interaktif menü döngüsü.
    """
    show_path: bool = True
    renderer = Render()
    current_maze = maze
    while True:
        print("\033[H\033[J", end="")
        renderer.render(current_maze, show_path)
        # menü
        print("\nA-Maze-ing======")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice: str = input("Choice? (1-4): ").strip()
        
        if choice == "1":
            if maze.seed is None:
                # 1. Senaryo: Eğer config'de seed YOKSA, gerçek rastgelelik (None) ver
                next_seed = None
            else:
                # 2. Senaryo: Eğer config'de seed VARSA, o orijinal seed'i tekrar ver (Eski harita basılsın)
                next_seed = maze.seed
            current_maze = Maze(
                                width=current_maze.width,
                                height=current_maze.height,
                                entry=current_maze.entry,
                                exit=current_maze.exit,
                                perfect=current_maze.perfect,
                                seed= next_seed
                            )
            final_paths = generate(current_maze)
            while not final_paths:
                final_paths = generate(current_maze)
        elif choice == "2":
            # Çözüm yolunu açar veya kapatır
            show_path = not show_path
        elif choice == "3":
            # Render sınıfının içindeki renk durumunu (state) rastgele günceller
            renderer.random_theme()
        elif choice == "4":
            print("\nQuitting the application.")
            break

def main() -> None:
    """
    Programın ana yürütücü gövdesi. Komut satırı argümanlarını denetler ve akışı başlatır.
    """
    # 1. Komut satırı argüman kontrolü (Zorunlu kural)
    if len(sys.argv) != 2:
        sys.stderr.write("Error. Your program must be run with the python3 a_maze_ing.py "
              "config.txt")
        sys.exit(1)

    config_file: str = sys.argv[1]

    try:
        # config parse'ı
        parser = ConfigParser(config_file)
        parser.parsing()
        parser.check_data()

        # veri çekme
        width: int = parser.data["WIDTH"]
        height: int = parser.data["HEIGHT"]
        entry: tuple[int, int] = parser.data["ENTRY"]
        maze_exit: tuple[int, int] = parser.data["EXIT"]
        perfect: bool = parser.data["PERFECT"]
        output_file: str = parser.data["OUTPUT_FILE"]
        seed_val = parser.data.get("SEED")
        # labirent generate
        maze = Maze(width=width, height=height, entry=entry, exit=maze_exit, perfect=perfect, seed=seed_val)
        final_paths = generate(maze)

        while not final_paths:
            final_paths = generate(maze)

        # output file'a yazma
        write_output_file(output_file, maze, final_paths[0])

        # Render için fonksiyon yazılacak
        run_maze_render(maze)
    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()