# GameOfLife
A simplistic cellular automaton similuator used to implement the rules from Conway's Game Of Life.

To learn more about Conway's Game of Life, check out this link: http://www.conwaylife.com/wiki/Conway%27s_Game_of_Life

**Dependancies**
* numpy - https://docs.scipy.org/doc/numpy/user/install.html
* Python 3+ (3.5.2 used during development) - https://www.python.org/downloads/
* Tkinter - https://tkdocs.com/tutorial/install.html

**Utilities**
* Manual Tile Input - User tile selection via mouse input
* Random Selection - Alternative random selection based on probability (see `frequency`)
* Trail Tiles - Set tiles that were active last step as *Red*, to create a 'burning' effect
* Area Tiles - Set inactive tiles previously occupied at any point *Blue*, showing traversed areas (Note: this minorly reduces simulation tick speed)

**Program Variables**
* `board_size` - Size of rendering canvas (pixels)
* `tile_size` - Size of each tile (pixels) (Note: for optimal use, make sure `board_size` / `tile_size` is an integer resulting in a factor of `board_size`)
* `interval` - Temporal step value (default: 40 ms)
* `frequency` - the chance of generating a tile when using the Random Selection method (default 30, 30% active tile rate)
