import tkinter as tk
import numpy as np
# === Global Parameters ===
board_size      = 600   # Board size (pixels)
tile_size       = 15    # Tile size (pixels)
num_tiles_row   = int(board_size/tile_size) # Ratio of tiles to board

running         = True  # Main loop flag
interval        = 60    # time interval per temportal step
frequency       = 30    # Set between 0 and 99 

count           = 0     # Number of steps taken

# === Functions ===
def initialise():
    global new_matrix
    # Generate the 'Inner' matrix
    raw = np.zeros((num_tiles_row,num_tiles_row))
    for i in range (0,num_tiles_row):
        for j in range (0,num_tiles_row):
            if (np.random.randint(100) > 100-frequency):
                raw[i][j] = 1
            else:
                raw[i][j] = 0
    # Move into a larger matrix, with an extra layer, to avoid out of bounds.
    new_matrix = np.full((num_tiles_row+2,num_tiles_row+2),2)
    for i in range (0,num_tiles_row):
        for j in range (0,num_tiles_row):
            new_matrix[i+1,j+1] = raw[i,j]

    return new_matrix

# Function : Randomise the tile values, dependant on frequency proability
def random():
    global new_matrix, prev_matrix, area_matrix, count
    # Assign values to grid, based on probability
    for i in range (1,num_tiles_row+1):
        for j in range (1,num_tiles_row+1):
            if (np.random.randint(100) > 100-frequency):
                new_matrix[i][j] = 1
            else:
                new_matrix[i][j] = 0
    # reset matrices
    prev_matrix = np.zeros(new_matrix.shape)
    area_matrix = np.copy(new_matrix)
    # Reset step count
    count = 0
    print('matrix randomly set.')
    update_tiles(new_matrix,prev_matrix,area_matrix)

# Function : Reset tile values to 0
def reset():
    global new_matrix, prev_matrix, area_matrix, count
    # reset matrices
    new_matrix  = np.zeros(new_matrix.shape)
    prev_matrix = np.zeros(new_matrix.shape)
    area_matrix = np.copy(new_matrix)
    # Reset step count
    count = 0
    print('matrix reset.')
    update_tiles(new_matrix,prev_matrix,area_matrix)

 # Function : Toggle a tile manually
def toggle_tile(event):
    global new_matrix, prev_matrix, area_matrix, tile_size
    y = int(event.x / tile_size)
    x = int(event.y / tile_size)
    # Flip tile logic
    if(new_matrix[x+1][y+1] == 0):
        new_matrix[x+1][y+1] = 1
    else:
        if(new_matrix[x+1][y+1] == 1):
            new_matrix[x+1][y+1] = 0
    # Update GUI
    update_tiles(new_matrix,prev_matrix,area_matrix) 
    print('Tile toggle:', (x,y))

# Funtion : Enable algorithm loop
def start():
    global running
    running = True

# Function : Disable algorithm loop
def stop():
    global running
    running = False

# Function : If running, perform a temporal step
def time_step():
    if running:
        global new_matrix, prev_matrix, area_matrix
        new_matrix = calculate_matrix(new_matrix,prev_matrix,area_matrix)
    # Call the function in succession (recursively)   
    root.after(interval,time_step)      

# Function : Determine the matrix values after one temporal step
def calculate_matrix(input,prev,area):
        global count
        # Copy matrix statically
        temp = np.copy(input)
        prev = np.copy(input)
        neighbour_matrix = np.zeros((num_tiles_row,num_tiles_row))
        # Per tile, check neighbours for activation 
        for i in range(1,num_tiles_row+1):
            for j in range(1,num_tiles_row+1):
                neighbour_count = 0
                if(input[i-1][j-1] == 1):
                    neighbour_count += 1
                if(input[i][j-1] == 1):
                    neighbour_count += 1
                if(input[i+1][j-1] == 1):
                    neighbour_count += 1
                if(input[i-1][j] == 1):
                    neighbour_count += 1
                if(input[i+1][j] == 1):
                    neighbour_count += 1
                if(input[i-1][j+1] == 1):
                    neighbour_count += 1
                if(input[i][j+1] == 1):
                    neighbour_count += 1
                if(input[i+1][j+1] == 1):
                    neighbour_count += 1
                neighbour_matrix[i-1,j-1] = neighbour_count
                # Apply Conway's rules
                if(neighbour_count  < 2 or neighbour_count > 3 and new_matrix[i][j] == 1):
                    temp[i][j] = 0
                if (neighbour_count == 3 and new_matrix[i][j] == 0):
                    temp[i][j] = 1
                    area[i][j] = 1         

        count += 1
        print(count)
        # Update GUI
        update_tiles(temp,prev,area)

        return temp



# Function : Update and draw tile values
def update_tiles(input,prev,area):
    # Refresh Canvas
    c.delete(tk.ALL)
    # Draw tiles dependant of activation
    for i in range (0,num_tiles_row):
        for j in range (0,num_tiles_row):
            tile_coord = 0 + j*tile_size ,0 + i*tile_size ,tile_size + j*tile_size ,tile_size + i*tile_size
            # Area tiles
            if(inh.get()):
                if area[i+1][j+1] == 1:
                    c.create_rectangle(tile_coord, fill='blue')
            if input[i+1][j+1] == 0:
                # Trail tiles
                if(trail.get() and inh.get() == 0):
                    if prev[i+1][j+1] == 1:
                        c.create_rectangle(tile_coord, fill='red')
            else:
                # Active tiles
                c.create_rectangle(tile_coord, fill='orange')
            # Area tiles
            if(inh.get()):
                if (area[i+1][j+1] == 1 and input[i+1][j+1] == 0):
                    c.create_rectangle(tile_coord, fill='blue')
                    # Area and Trail tiles
                    if(trail.get()):
                        if prev[i+1][j+1] == 1:
                            c.create_rectangle(tile_coord, fill='red')

# GUI variables
root = tk.Tk()
root.title('Conway\'s Game Of Life (Cellular Automaton)')
c = tk.Canvas(root,width=board_size, height=board_size, background = 'black')
btn_random = tk.Button(root, text='Random', command=random)
btn_reset = tk.Button(root, text='Reset', command=reset)
btn_run = tk.Button(root, text='Run', command=start)
btn_stop = tk.Button(root, text='Stop', command=stop)
trail = tk.IntVar()
chk_trail = tk.Checkbutton(root,text='Enable Trail',var=trail)
inh = tk.IntVar()
chk_area = tk.Checkbutton(root,text='Enable Area',var=inh)

# Prepare GUI component layout
c.pack()
btn_random.pack(side=tk.LEFT, expand = tk.YES)
btn_run.pack(side=tk.RIGHT, expand = tk.YES)
btn_reset.pack(side=tk.LEFT, expand = tk.YES)
btn_stop.pack(side=tk.LEFT, expand = tk.YES)
chk_trail.pack()
chk_area.pack()
c.bind("<Button-1>", toggle_tile)

# Initialise Matrices
new_matrix = initialise()
prev_matrix = np.zeros(new_matrix.shape)
area_matrix = np.copy(new_matrix)

# BEGIN PROGRAM
update_tiles(new_matrix,prev_matrix,area_matrix)
root.after(interval, time_step)
root.mainloop()