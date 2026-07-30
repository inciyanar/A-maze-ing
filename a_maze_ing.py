import sys
from pars_ing import ConfigParser
from maze_ing import Maze, generate
from output_file_helpers import write_output_file
from render import Render


def run_maze_render(maze: Maze, output_file: str) -> None:
    """
    Handles the interactive menu loop for rendering and managing the maze.

    Allows the user to re-generate the maze, toggle path visibility,
    rotate terminal colors, or quit the application.

    Args:
        maze (Maze): The current maze instance to interact with.
        output_file (str): The path to the file where new mazes will be saved.
    """
    show_path: bool = True
    renderer = Render()
    current_maze = maze
    while True:
        renderer.render(current_maze, show_path)
        if current_maze.warning_message:
            print(f"\n\033[33m{current_maze.warning_message}\033[0m")
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice: str = input("Choice? (1-4): ").strip()
        if choice == "1":
            if current_maze.seed is None:
                next_seed = None
            else:
                next_seed = current_maze.seed
            current_maze = Maze(
                                width=current_maze.width,
                                height=current_maze.height,
                                entry=current_maze.entry,
                                exit=current_maze.exit,
                                perfect=current_maze.perfect,
                                seed=next_seed
                            )
            final_paths: list[list[tuple[int, int]]] = []
            max_attempts = 50
            attempts = 0
            while not final_paths and attempts < max_attempts:
                final_paths = generate(current_maze)
                attempts += 1

            if not final_paths:
                raise RuntimeError(
                    "Error: Could not generate a valid maze with a path "
                    "between entry and exit after maximum attempts. Try "
                    "increasing the maze dimensions."
                    )
            write_output_file(output_file, current_maze, final_paths[0])
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            renderer.random_theme()
        elif choice == "4":
            print("\nQuitting the application.")
            break


def main() -> None:
    """
    The main entry point of the maze application.
    Parses command-line arguments, initializes the configuration parser,
    validates setup data, generates the initial maze, triggers the renderer.
    """
    if len(sys.argv) != 2:
        sys.stderr.write("Error. Your program must be run with the python3 "
                         "a_maze_ing.py <config.txt>")
        sys.exit(1)
    config_file: str = sys.argv[1]
    try:
        parser = ConfigParser(config_file)
        parser.parsing()
        parser.check_data()
        width: int = parser.data["WIDTH"]
        height: int = parser.data["HEIGHT"]
        entry: tuple[int, int] = parser.data["ENTRY"]
        maze_exit: tuple[int, int] = parser.data["EXIT"]
        perfect: bool = parser.data["PERFECT"]
        output_file: str = parser.data["OUTPUT_FILE"]
        seed_val = parser.data.get("SEED")
        maze = Maze(width=width, height=height, entry=entry, exit=maze_exit,
                    perfect=perfect, seed=seed_val)
        if maze.grid[entry[0]][entry[1]] in maze.ft_cell:
            raise ValueError(
                "Configuration Error: ENTRY coordinates fall on a '42' "
                "sign cell, which must stay fully closed."
            )
        if maze.grid[maze_exit[0]][maze_exit[1]] in maze.ft_cell:
            raise ValueError(
                "Configuration Error: EXIT coordinates fall on a '42' "
                "sign cell, which must stay fully closed."
            )
        final_paths = generate(maze)

        while not final_paths:
            final_paths = generate(maze)
        write_output_file(output_file, maze, final_paths[0])
        run_maze_render(maze, output_file)
    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
