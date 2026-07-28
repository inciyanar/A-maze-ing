import random
from maze_ing import Maze


class Render():
    """
    Manages terminal screen layout resets and processes
    map matrix blocks into colorful ANSI structures.
    Attributes:
        theme (dict): Stored color mapping tokens.
    """
    def __init__(self) -> None:
        """Initializes Render colors using default theme values."""
        self.theme: dict[str, str] = {
            "WALL": "\033[38;5;105m██\033[0m",
            "ENTRY": "\033[105m  \033[0m",
            "EXIT": "\033[106m  \033[0m",
            "PATH": "\033[48;5;210m  \033[0m",
            "FT_42": "\033[48;5;121m  \033[0m"
        }

    def random_theme(self) -> None:
        """
        Generates random color codes across elements to produce a fresh active
        visual profile.
        """
        wall_color: int = random.randint(16, 231)
        entry_color: int = random.randint(16, 231)
        exit_color: int = random.randint(16, 231)
        path_color: int = random.randint(16, 231)
        ft_color: int = random.randint(16, 231)
        self.theme = {
                "WALL": f"\033[38;5;{wall_color}m██\033[0m",
                "ENTRY": f"\033[48;5;{entry_color}m  \033[0m",
                "EXIT": f"\033[48;5;{exit_color}m  \033[0m",
                "PATH": f"\033[48;5;{path_color}m  \033[0m",
                "FT_42": f"\033[48;5;{ft_color}m  \033[0m"
            }

    def render(self, maze: Maze, show_path: bool = True) -> None:
        """
        Clears the current screen terminal window space and prints
        the structured map matrix layout.
        Args:
            maze (Maze): Maze instance carrying full live layout records.
            show_path (bool): Visibility flag toggle for solution trail
            rendering blocks.
        """
        W_WALL: str = self.theme["WALL"]
        BG_ENTRY: str = self.theme["ENTRY"]
        BG_EXIT: str = self.theme["EXIT"]
        BG_PATH: str = self.theme["PATH"]
        BG_42: str = self.theme["FT_42"]
        W_EMPTY: str = "  "
        ft_cells = maze.ft_cell
        buf_w: int = maze.width * 2 + 1
        buf_h: int = maze.height * 2 + 1
        found_paths = maze.find_solution_ways()
        solutions = set(found_paths[0])
        render_list: list[list[str]] = [[W_WALL for _ in range(buf_h)]
                                        for _ in range(buf_w)]
        for x in range(maze.width):
            for y in range(maze.height):
                cell = maze.grid[x][y]
                rx = 2 * x + 1
                ry = 2 * y + 1
                if (x, y) == maze.entry:
                    render_list[rx][ry] = BG_ENTRY
                elif (x, y) == maze.exit:
                    render_list[rx][ry] = BG_EXIT
                elif show_path and (x, y) in solutions:
                    render_list[rx][ry] = BG_PATH
                elif cell in ft_cells:
                    render_list[rx][ry] = BG_42
                else:
                    render_list[rx][ry] = W_EMPTY
                if cell.walls["NORTH"] == 0 and ry - 1 >= 0:
                    if (show_path
                            and (x, y) in solutions
                            and (x, y - 1) in solutions):
                        render_list[rx][ry - 1] = BG_PATH
                    else:
                        render_list[rx][ry - 1] = W_EMPTY
                if cell.walls["SOUTH"] == 0 and ry + 1 < buf_h:
                    if (show_path
                            and (x, y) in solutions
                            and (x, y + 1) in solutions):
                        render_list[rx][ry + 1] = BG_PATH
                    else:
                        render_list[rx][ry + 1] = W_EMPTY
                if cell.walls["WEST"] == 0 and rx - 1 >= 0:
                    if (show_path
                            and (x, y) in solutions
                            and (x - 1, y) in solutions):
                        render_list[rx - 1][ry] = BG_PATH
                    else:
                        render_list[rx - 1][ry] = W_EMPTY
                if cell.walls["EAST"] == 0 and rx + 1 < buf_w:
                    if (show_path
                            and (x, y) in solutions
                            and (x + 1, y) in solutions):
                        render_list[rx + 1][ry] = BG_PATH
                    else:
                        render_list[rx + 1][ry] = W_EMPTY
        for ry in range(buf_h):
            print("".join([render_list[rx][ry] for rx in range(buf_w)]))
