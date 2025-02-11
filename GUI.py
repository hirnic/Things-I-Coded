import tkinter as tk
import random

# Set up the window
window = tk.Tk()
window.title("Catch the Collectibles")
window.geometry("600x600")  # Updated geometry

# Canvas for game
canvas = tk.Canvas(window, width=600, height=500, bg="white")
canvas.pack()

# Game variables
player_width = 30
player_height = 30
player_x = 50
player_lane = 5  # Start at the middle lane (lane 5)
player_speed = 1

collectibles = []
collectible_width = 20
collectible_height = 20
collectible_speed = 5

score = 0

# Number of lanes (10 horizontal lanes)
num_lanes = 10
lane_height = 500 // num_lanes  # Height of each lane

# Create the player square
player = None  # Initially, no player square

# Score label
score_label = tk.Label(window, text="Score: 0", font=("Helvetica", 16))
laneLabels = {"lane0": tk.Label(window, text="0", font=("Helvetica", 16)),
              "lane1": tk.Label(window, text="1", font=("Helvetica", 16)),
              "lane2": tk.Label(window, text="2", font=("Helvetica", 16)),
              "lane3": tk.Label(window, text="3", font=("Helvetica", 16)),
              "lane4": tk.Label(window, text="4", font=("Helvetica", 16)),
              "lane5": tk.Label(window, text="5", font=("Helvetica", 16)),
              "lane6": tk.Label(window, text="6", font=("Helvetica", 16)),
              "lane7": tk.Label(window, text="7", font=("Helvetica", 16)),
              "lane8": tk.Label(window, text="8", font=("Helvetica", 16)),
              "lane9": tk.Label(window, text="9", font=("Helvetica", 16))
              }

# Function to move the player
def move_player(event):
    global player_lane
    if event.keysym == 'Up' and player_lane > 0:
        player_lane -= 1  # Move up one lane
    elif event.keysym == 'Down' and player_lane < num_lanes - 1:
        player_lane += 1  # Move down one lane
    # Update player position based on lane
    elif event.keysym in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        player_lane = int(event.keysym)
    player_y = player_lane * lane_height
    canvas.coords(player, player_x, player_y, player_x + player_width, player_y + player_height)


# Here we are going to make a class for the collectibles. It is just a canvas rectangle, but it also has a number associated with it.
# class Collectible:
#     def __init__(self, price, lane, x, y):
#         self.price = price
#         self.lane = lane
#         self.x = x
#         self.y = y
#         self.id = canvas.create_rectangle(x, y, x + collectible_width, y + collectible_height, fill="red")
#
#     def move(self):
#         self.x -= collectible_speed
#         canvas.move(self, -collectible_speed, 0)
#
#     def check_collision(self):
#         if (self.x < player_x + player_width and self.x > player_x and
#                 self.y < (player_lane + 1) * lane_height and self.y > player_lane * lane_height):
#             return True
#         return False


# Function to create new collectibles
def create_collectible():
    x = 600  # Start off screen
    lane = random.randint(0, num_lanes - 1)  # Random lane for collectible
    y = lane * lane_height + 5
    collectible = canvas.create_rectangle(x, y, x + collectible_width, y + collectible_height, fill="red")
    collectibles.append(collectible)


# Function to move collectibles
def move_collectibles():
    global score
    for collectible in collectibles[:]:
        canvas.move(collectible, -collectible_speed, 0)  # Move left
        x1, y1, x2, y2 = canvas.coords(collectible)

        # Check if the collectible is off screen
        if x2 < 0:
            canvas.delete(collectible)
            collectibles.remove(collectible)

        # Check for collision with player
        if (x1 < player_x + player_width and x2 > player_x and
                y1 < (player_lane + 1) * lane_height and y2 > player_lane * lane_height):
            canvas.delete(collectible)
            collectibles.remove(collectible)
            score += 1
            # Update score label
            score_label.config(text=f"Score: {score}")


# Game loop
def game_loop():
    # Create new collectibles every 1000ms
    if random.randint(1, 30) == 1:
        create_collectible()

    move_collectibles()
    window.after(40, game_loop)


def printKey(event):
    print("pressed", event.keysym)


# Function to start the game
def start_game():
    global player, score
    score = 0
    score_label.config(text=f"Score: {score}")

    for i in range(10):
        laneLabels["lane" + str(i)].place(x=10, y=i * 50)

    # Remove the main menu elements
    main_menu_frame.pack_forget()

    # Create the player square
    player_y = player_lane * lane_height
    player = canvas.create_rectangle(player_x, player_y, player_x + player_width, player_y + player_height, fill="blue")
    score_label.pack()  # Display score

    # Bind keys for movement
    window.bind("<Up>", move_player)
    window.bind("<Down>", move_player)
    for i in range(10):
        window.bind(str(i), move_player)
    # window.bind("<Key>", printKey)

    # Start the game loop
    game_loop()


# Create Main Menu
main_menu_frame = tk.Frame(window)

# Add a "Play" button
play_button = tk.Button(main_menu_frame, text="Play", font=("Helvetica", 20), command=start_game)
play_button.pack(pady=20)

# Add the main menu frame to the window
main_menu_frame.pack()


# Start the Tkinter event loop
window.mainloop()
