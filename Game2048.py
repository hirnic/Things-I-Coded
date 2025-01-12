import random
import tkinter as tk
import math

# The most important part of the game!
score = 0
# This is the grid of numerical values. For each index x in Grid, use (x//4,x%4) to find the coordinates.
Grid = [0 for i in range(16)]

# This generates a random square.
def generate_square(grid):
    new_grid = grid
    grid_free = [i for i in range(16) if new_grid[i] == 0]
    index = random.choice(grid_free)
    p = random.uniform(0, 1)
    x = 2
    if p > 0.9:
        x = 4
    new_grid[index] = x
    return new_grid

# This tests the loss condition
def loss_condition(grid):
    global score
    old_score = score
    if 0 in grid:
        return False
    elif (grid == grid_slide(grid, 'Left') and grid == grid_slide(grid, 'Right')
          and grid == grid_slide(grid, 'Up') and grid == grid_slide(grid, 'Down')):
        return True
    else:
        score = old_score
        return False

# Initialize the window
root = tk.Tk()
root.title("2-To-The-Power-Of-Eleven_Version 1")
width, height = 398, 448
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

# Function to draw a pixel on the canvas
def draw_pixel(x, y, color):
    canvas.create_rectangle(x, y, x + 1, y + 1, outline=color, fill=color)

# Draw a line on the canvas
def draw_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        draw_pixel(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Draw a rectangle on the canvas
def draw_rectangle(x1, y1, x2, y2, color):
    canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)

# This makes the black screen
def make_blackground():
    draw_rectangle(0, 50, 400, 450, 'black')

# This makes the grid lines
def make_gridlines():
    # Vertical gridlines
    draw_line(100, 50, 100, 450, 'gray')
    draw_line(200, 50, 200, 450, 'gray')
    draw_line(300, 50, 300, 450, 'gray')
    # Horizontal gridlines
    draw_line(0, 150, 400, 150, 'gray')
    draw_line(0, 250, 400, 250, 'gray')
    draw_line(0, 350, 400, 350, 'gray')

# Makes the black background with grey gridlines
def make_background():
    make_blackground()
    make_gridlines()

# This is the list of colors of the numerical values of the squares
def colorizer(n):
    colors = ['maroon', 'purple', 'yellow', 'cyan', 'red2', 'blue2',
              'light coral', 'dark green', 'green yellow', 'honeydew2', 'navy', 'orange']
    return colors[n]

# This updates the score
def update_score():
    canvas.create_text(200, 25, text="Score: " + str(score), font=("Courier New", 16), fill="black")

# Here we style the square with Grid index n
def make_brick(n):
    if Grid[n] != 0:
        color = colorizer(int(math.log2(Grid[n]) - 1))
        x1 = 1 + (n % 4) * 100
        y1 = 51 + (n // 4) * 100
        x2 = 99 + (n % 4) * 100
        y2 = 149 + (n // 4) * 100
        draw_rectangle(x1, y1, x2, y2, color)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=Grid[n], font=("Arial", 40), fill="black")

# Populates the grid with the squares from Grid
def populate():
    for n in range(16):
        make_brick(n)

# This is the loss screen
def lose_screen():
    draw_rectangle(100, 100, 300, 350, 'white')
    canvas.create_text(200, 175, width=200, anchor="center", text="You Lose!", font=("Courier New", 40), fill="black")
    button1.config(state=tk.NORMAL)
    button2.config(state=tk.NORMAL)

# This function animates a block moving from initial position in the specified direction by one block
def slide_animation(grid, drxn, init):
    x1 = 1 + (init % 4) * 100
    y1 = 51 + (init // 4) * 100
    x2 = 99 + (init % 4) * 100
    y2 = 149 + (init // 4) * 100
    if drxn == 'Left':
        color = colorizer(int(math.log2(grid[init - 1]) - 1))
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 - 100
        x2 = x2 - 100
        draw_rectangle(x1, y1, x2, y2, color)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=grid[init - 1], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Right':
        color = colorizer(int(math.log2(grid[init + 1]) - 1))
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 + 100
        x2 = x2 + 100
        draw_rectangle(x1, y1, x2, y2, color)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=grid[init + 1], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Up':
        color = colorizer(int(math.log2(grid[init - 4]) - 1))
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 - 100
        y2 = y2 - 100
        draw_rectangle(x1, y1, x2, y2, color)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=grid[init - 4], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Down':
        color = colorizer(int(math.log2(grid[init + 4]) - 1))
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 + 100
        y2 = y2 + 100
        draw_rectangle(x1, y1, x2, y2, color)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=grid[init + 4], font=("Arial", 40), fill="black")
        canvas.update()

# This function animates a block moving from initial position in the specified direction by one block
def collision_animation(drxn, init):
    color1, color2 = 'black', 'black'
    if Grid[init] != 0:
        color1 = colorizer(int(math.log2(Grid[init]) - 1))
        color2 = colorizer(int(math.log2(Grid[init])))
    x1 = 1 + (init % 4) * 100
    y1 = 51 + (init // 4) * 100
    x2 = 99 + (init % 4) * 100
    y2 = 149 + (init // 4) * 100
    if drxn == 'Left':
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 - 50
        x2 = x2 - 50
        draw_rectangle(x1, y1, x2, y2, color1)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 - 50
        x2 = x2 - 50
        draw_rectangle(x1, y1, x2, y2, color2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=2*Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Right':
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 + 50
        x2 = x2 + 50
        draw_rectangle(x1, y1, x2, y2, color1)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
        draw_rectangle(x1, y1, x2, y2, 'black')
        x1 = x1 + 50
        x2 = x2 + 50
        draw_rectangle(x1, y1, x2, y2, color2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=2*Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Up':
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 - 50
        y2 = y2 - 50
        draw_rectangle(x1, y1, x2, y2, color1)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 - 50
        y2 = y2 - 50
        draw_rectangle(x1, y1, x2, y2, color2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=2*Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
    if drxn == 'Down':
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 + 50
        y2 = y2 + 50
        draw_rectangle(x1, y1, x2, y2, color1)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=Grid[init], font=("Arial", 40), fill="black")
        canvas.update()
        draw_rectangle(x1, y1, x2, y2, 'black')
        y1 = y1 + 50
        y2 = y2 + 50
        draw_rectangle(x1, y1, x2, y2, color2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=2*Grid[init], font=("Arial", 40), fill="black")
        canvas.update()

# Slides the grid in the specified direction
def grid_slide(grid, drxn):
    new_grid = grid.copy()
    global score
    for number in range(4):
        for k in range(3):
            if drxn == 'Left':
                for i in range(3):
                    if new_grid[4*number + i] == 0:
                        new_grid[4*number + i], new_grid[4*number + i + 1] = new_grid[4*number + i + 1], 0
                        if new_grid[4*number + i] != 0:
                            slide_animation(new_grid, drxn, 4 * number + i + 1)
                    elif new_grid[4*number + i] == new_grid[4*number + i + 1]:
                        new_grid[4*number + i], new_grid[4*number + i + 1] = 2 * new_grid[4 * number + i], 0
                        score += new_grid[4*number + i]
                        collision_animation(drxn, 4*number + i+1)
            elif drxn == 'Right':
                for i in range(3, 0, -1):
                    if new_grid[4 * number + i] == 0:
                        new_grid[4 * number + i], new_grid[4 * number + i - 1] = new_grid[4 * number + i - 1], 0
                        if new_grid[4*number + i] != 0:
                            slide_animation(new_grid, drxn, 4 * number + i-1)
                    elif new_grid[4 * number + i] == new_grid[4 * number + i - 1]:
                        new_grid[4 * number + i], new_grid[4 * number + i - 1] = 2 * new_grid[4 * number + i], 0
                        score += new_grid[4 * number + i]
                        collision_animation(drxn, 4 * number + i - 1)
            elif drxn == 'Up':
                for i in range(3):
                    if new_grid[number + 4 * i] == 0:
                        new_grid[number + 4 * i], new_grid[number + 4 * (i + 1)] = new_grid[number + 4 * (i + 1)], 0
                        if new_grid[number + 4*i] != 0:
                            slide_animation(new_grid, drxn,  number + 4 *(i + 1))
                    elif new_grid[number + 4 * i] == new_grid[number + 4 * (i + 1)]:
                        new_grid[number + 4 * i], new_grid[number + 4 * (i + 1)] = 2 * new_grid[number + 4 * i], 0
                        collision_animation(drxn, number + 4 *(i + 1))
                        score += new_grid[number + 4 * i]
            elif drxn == 'Down':
                for i in range(3, 0, -1):
                    if new_grid[number + 4 * i] == 0:
                        new_grid[number + 4 * i], new_grid[number + 4 * (i - 1)] = new_grid[number + 4 * (i - 1)], 0
                        if new_grid[number + 4 * i] != 0:
                            slide_animation(new_grid, drxn,  number + 4 *(i - 1))
                    elif new_grid[number + 4 * i] == new_grid[number + 4 * (i - 1)]:
                        new_grid[number + 4 * i], new_grid[number + 4 * (i - 1)] = 2 * new_grid[number + 4 * i], 0
                        collision_animation(drxn, number + 4 * (i - 1))
                        score += new_grid[number + 4 * i]
    if new_grid != grid:
        new_grid = generate_square(new_grid)
    return new_grid

# This is what the arrow keys activate
def key_slide(event):
    root.unbind("<Left>")
    root.unbind("<Right>")
    root.unbind("<Up>")
    root.unbind("<Down>")
    global Grid
    # old_grid = Grid.copy()
    Grid = grid_slide(Grid, event.keysym)
    #
    canvas.delete("all")
    update_score()
    make_background()
    populate()
    root.bind("<Left>", key_slide)
    root.bind("<Right>", key_slide)
    root.bind("<Up>", key_slide)
    root.bind("<Down>", key_slide)
    if loss_condition(Grid):
        lose_screen()

# This starts a new game
def new_game():
    global Grid
    Grid = [0 for _ in range(16)]
    generate_square(Grid)
    generate_square(Grid)
    make_background()
    update_score()
    populate()
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.NORMAL)

# This opens the main menu
def main_menu():
    canvas.delete('all')
    canvas.create_text(200, 150, width=350, anchor="center", text="Welcome to 2048!",
                       font=("Courier New", 40), fill="black")
    canvas.create_text(200, 300, width=350, anchor="center",
                       text='After pressing "New Game," just use the arrow keys to move the blocks. around.'
                            ' The goal is to get a 2048 tile. Good luck!',
                       font=("Courier New", 20), fill="black")

# This quits the game
def Quit():
    main_menu()
    button2.config(state=tk.DISABLED)
    button1.config(state=tk.NORMAL)

# Bind arrow keys
root.bind("<Left>", key_slide)
root.bind("<Right>", key_slide)
root.bind("<Up>", key_slide)
root.bind("<Down>", key_slide)

# Here are the New Game and Quit buttons
button1 = tk.Button(root, text="New Game", command=new_game)
button1.place(x=1, y=25)
button2 = tk.Button(root, text="Quit", command=Quit, state=tk.DISABLED)
button2.place(x=350, y=25)

# Run the main event loop
main_menu()
root.mainloop()
