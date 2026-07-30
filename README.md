_This project has been created as part of the 42 curriculum by edpolat, incyanar._

# A_maze_ing

## Description

**A_maze_ing** is a fun Python 3 program that makes and solves mazes. It reads the settings from a configuration file (config.txt) to build each maze. Then, it shows the maze directly on your terminal screen using colorful text. Finally, it uses smart search algorithms to find the shortest and best path from the start to the exit.

### Algorithm Explaination

The `generate(maze)` function creates the maze step by step. In order it checks for errors, breaks walls, fixes stuck cells, and finds the solution path.

- **`maze.ft_write()`**: Places the custom `42` signs onto the map grid.
- **Entry & Exit Check**: The code checks if the `ENTRY` or `EXIT` coordinates are on top of a `42` sign. If they are on the same spot, the program stops and throws a simple error.

- **`maze.create_guaranteed_path()`**: This function creates a clear path from the start to the end. Because of this, the maze is **always solvable** from the beginning.

- **`maze.random_broker()`**: This breaks random walls around the map to make the maze look more natural and random.

Depending on the setting in the config file, the code follows one of two ways:

#### If `maze.perfect == True` (Perfect Maze)
A perfect maze means there are no loops and there is only one correct way to go from start to finish.
1. **`maze.perfect_maker()`**: This loop runs until all circles and extra loops are deleted.

2. **`maze.fix_isolated_cells()`**: After removing the loops, the code checks the whole map using a search algorithm (BFS). If a cell is completely trapped behind four walls, it breaks one wall to connect it to the rest of the maze.

#### If `maze.perfect == False` (Imperfect Maze)
An imperfect maze means players can use different paths, loops, or shortcuts to reach the exit.
1. **Keeping the Loops**: The code skips `perfect_maker()`, so all the random loops stay in the maze.

2. **`maze.fix_isolated_cells()`**: It immediately fixes completely trapped cells so that every single area on the map can be reached.

- **Warning Messages**: If something goes wrong or changes during generation, it prints a message on the terminal.

- **`maze.find_solution_ways()`**: Finally, the program calculates the correct path from start to finish and sends it to the screen to draw the green/pink line.

## Instructions

### Running the Project
1. Clone or navigate to the project directory.
2. The program reads a file named `config.txt` to build the maze. Create a file named `config.txt` in your project folder and write it like this:

	```text
	WIDTH = 9
	HEIGHT = 7
	ENTRY = 2, 5
	EXIT = 0, 0
	OUTPUT_FILE = output.txt
	PERFECT = True
	SEED = 42
	```

	WIDTH / HEIGHT: The size of the maze grid (number of columns and rows).

	ENTRY: The starting point coordinates (x, y).

	EXIT: The ending point coordinates (x, y).

	OUTPUT_FILE: The name of the text file where the maze layout will be saved.

	PERFECT: Write True to make a maze with only one correct way. Write False to allow extra loops and shortcuts.

	SEED (Optional): This line is not required. If you write a number here, the program will generate the exact same maze every time (good for testing). If you delete this line, the maze will be completely new and random every time you run the code.

3. Execute the main script and config file from your terminal:
   ```bash
   python3 a_maze_ing.py config.txt
   ````

### Feature

1. **Re-generate a new maze:** Generates a brand-new randomized maze using the same configuration rules.
2. **Show/Hide path from entry to exit:** Toggles the solution path visibility on the map using distinctive colored cells.
3. **Rotate maze colors:** Instantly cycles through different wall and background color themes.
4. **Quit:** Safely exits the application.

## Using the Maze Generator as a Library

The maze generation logic is reusable outside of this CLI project: it lives in
its own standalone module, `maze_ing.py`, and is published as an installable
package named `mazegen` (see `mazegen-1.0.0-py3-none-any.whl` /
`mazegen-1.0.0.tar.gz` at the root of this repository, built from
`pyproject.toml`).

### Install it in another project

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic example

```python
from maze_ing import Maze, generate

# Instantiate a maze
maze = Maze(width=20, height=20, entry=(0, 0), exit=(19, 19), perfect=True)

# Build the walls and get the list of solution paths
paths = generate(maze)
```

### Custom parameters (size, seed, mode)

The `Maze` constructor accepts:

- `width`, `height` (`int`): the grid size, in cells.
- `entry`, `exit` (`tuple[int, int]`): the `(x, y)` start/end coordinates.
- `perfect` (`bool`): `True` for a single-path perfect maze, `False` for a
  Pac-Man-style playable board with loops.
- `seed` (`int`, optional): pass the same seed to get the exact same maze
  again (reproducibility).

```python
maze = Maze(width=12, height=9, entry=(0, 0), exit=(11, 8),
            perfect=False, seed=42)
paths = generate(maze)
```

### Accessing the generated structure and the solution

`generate()` mutates `maze.grid` in place and returns every solution path it
found (entry to exit). The structure is not the same format as the output
file — it is a live grid of `Cell` objects you can inspect directly:

```python
paths = generate(maze)

# Access at least a solution: a list of (x, y) coordinates, entry to exit
shortest_solution = paths[0]
print(shortest_solution)

# Access the generated structure: one Cell object per (x, y)
cell = maze.grid[0][0]
print(cell.walls)            # e.g. {'NORTH': 1, 'EAST': 0, 'SOUTH': 1, 'WEST': 0}
print(cell.get_hex_value())  # hexadecimal wall encoding for that single cell
```

`1` means the wall on that side is closed, `0` means it is open — matching
the bit layout described in the "Configuration file format" section below.

## Algorithms

### Guaranteed-path carving + randomized wall braiding

Maze generation does **not** use a single full depth-first spanning tree over
the whole grid. Instead it combines two separate randomized passes:

1. **`create_guaranteed_path()`** — a randomized walk from the entry cell
   towards the exit cell only. It repeatedly picks a random unvisited
   neighbor and breaks the wall to it; when it gets stuck (no unvisited
   neighbor left), it backtracks to the previous cell on that same path and
   tries another direction, stack-style, exactly like a local DFS — but it
   stops as soon as it reaches the exit, so it only carves *one* path, not
   every cell in the grid.
2. **`random_broker()`** — afterwards scans every interior cell independently
   and randomly breaks 0–2 of its walls (each candidate break is checked
   against the "no 3x3 open area" rule via `checker_3x3` and reverted if it
   would violate it). This is what actually gives the rest of the grid its
   structure, its loops, and its branching — the guaranteed path from step 1
   is just one thread inside it.
3. **`fix_isolated_cells()`** then BFS-repairs any cell `random_broker()`
   happened to leave stranded, so the grid is fully connected before the
   perfect/playable branch runs.

We chose this two-phase approach over a single DFS spanning tree because it
decouples the two things the subject asks for independently:
- **Guaranteed solvability**, satisfied unconditionally by step 1 before
  anything else touches the grid — the entry→exit path exists regardless of
  what the braiding step does afterward.
- **Loop density and dead-end control**, handled by step 2 scanning *every*
  cell with an independent random chance, which gives a more even spread of
  loops across the whole grid than a classic DFS carve (which tends to
  produce one dominant winding corridor with sparse side branches). That
  matters directly for the playable (Pac-Man) mode's "at least two
  independent routes, rare dead-ends" requirement.
- Both steps in this pipeline (`create_guaranteed_path()` and
  `random_broker()`) simply skip any cell reserved for the "42" sign, so the
  sign is preserved for free without a separate exclusion pass.

Depending on `PERFECT`, the pipeline then either removes the extra loops
(`perfect_maker()`, for `PERFECT=True`) or actively opens up remaining
dead-ends (`fix_isolated_cells_nonper()`, for the default `PERFECT=False`
Pac-Man mode) — see the "Algorithm Explaination" section above for the exact
step-by-step order.

### BFS-based solution pathfinding

Finding the shortest path from entry to exit (and, more generally, checking
whether the maze is still a single connected region) uses breadth-first
search over the open passages.

We chose BFS specifically because it explores level by level, so the first
time it reaches the exit cell, that path is guaranteed to be the **shortest**
one — which matters for two things:
- The path written to the output file (as a direction string) should be a
  genuine shortest route, not just *any* route DFS happens to stumble into.
- Detecting whether more than one distinct route exists between entry and
  exit (used to validate perfect vs. playable mode) is more predictable with
  BFS's queue-based traversal than with a recursive DFS, which can revisit
  the same region in inconsistent orders across runs.

BFS also doubles as our general reachability check elsewhere in the project
(e.g. verifying no cell is left isolated from the main region after braiding),
since it explores the entire connected component from a single starting cell
in one pass.

## Resources

The following resources were used for understanding python syntax, optimizations, Breadth-first search (BFS) algorithm, Depth-First Search (DFS) algorithm, data types, visualization and python key words.

- https://www.geeksforgeeks.org/python/deque-in-python/
- https://docs.python.org/3/library/collections.html
- https://youtu.be/HZ5YTanv5QE?si=ag_CzuCbB_PmoNXK
- https://youtu.be/cS-198wtfj0?si=_mLon9xBZDVaKJ7p
- https://www.geeksforgeeks.org/python/python-syntax/
- https://www.w3schools.com/python/ref_list_pop.asp
- https://thequeenbeebs.medium.com/python-basics-the-random-module-54ce1baba373
- https://pythontutor.com/
-

## AI Usage

In this project AI has been used for:

- Understanding python syntax
- Generating tests
- Fixing bugs (such as timeout errors)
- Writing docstrings
- Writing README

## Roles of the members

### edpolat
- Parsing from the config file
- Rendering
- Package build
- Configuration, Cell and Maze objects
### incyanar: 
- DFS algorithm of the maze
- Pathfinding and generation algorithm
- Configuration
- Cell and Maze objects

## License

This project is distributed under the MIT License — see [LICENSE.md](LICENSE.md)
at the root of this repository for the full text. MIT was chosen specifically
because the maze generator (`maze_ing.py`, packaged as `mazegen`) is meant to
be reused: it explicitly allows any later project to import, modify, and
redistribute this code, as long as the original copyright notice is kept.
