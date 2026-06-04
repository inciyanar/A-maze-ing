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


(Bunu bizim için ekledim, readme den sileriz sonra)
Hangi durumlarda error döndürüyoruz?
- Argüman sayısı eksikse veya fazlaysa
	Error. Your program must be run with the python3 a_maze_ing.py

- Giriş çıkış koordinatları 42 yazısının üzerine gelirse (ValueError)
	Error: Entry coordinates cannot be on the 42 sign.
	Error: Exit coordinates cannot be on the 42 sign.

- Runtime hatası için otomatik error
	Error: {error}", file=sys.stderr

- Config dosyası bulamazsa (FileNotFoundError)
	Error: Config file not found: '{self.config_path}'

- Config içinde geçersiz syntax olursa (ValueError)
	Error in [dosya_yolu]: Invalid syntax on line -> '[satır_içeriği]' (Missing '=')

- Config içindeki parametreler eksikse (KeyError)
	Configuration Error: Mandatory key '[eksik olan şey]' is missing!

- Config içinde girilen sayılar tam sayı olmazsa (ValueError)
	Configuration Error: WIDTH and HEIGHT must be integers!

- Config içinde girilen sayılar negatif veya 0 olursa (ValueError)
	Configuration Error: Maze dimensions must be greater than 0!

- Config içinde exit enrty kooridnatlarında format hatası varsa (ValueError)
	Configuration Error: ENTRY and EXIT must be in 'x,y' integer format!

- Config içinde entry ve exit maze dışında ise (ValueError)
	Configuration Error: EXIT coordinates are out of maze bounds!
	Configuration Error: ENTRY coordinates are out of maze bounds!

- Config içinde Perfet Boole değilse (ValueError)
	Configuration Error: PERFECT must be bool!

- Config içinde Seed tam sayı değilse (ValueError)
	Configuration Error: SEED must be an integer!

- 42 yazısı ekrana sığmazsa
	Error: Maze is too small to fit the 42 sign !!!! MAZE BASTIRDIĞIMIZ SENARYODA FIRLATTIĞIMIZ TEK ERROR O SEBEPLE A_MAZE_İNG İÇİNDE


YAPILACAKLAR
- Yorumları kaldır
- Flake8 ve mypy kontrolleri
- Fonskiyon tanımlamalarımız türkçe onları ingilizce yapmak lazım



