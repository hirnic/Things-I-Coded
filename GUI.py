import tkinter as tk
import random

# Set up the window
window = tk.Tk()
window.title("Catch the Collectibles")
window.geometry("600x600")  # Updated geometry

# Canvas for game
canvas = tk.Canvas(window, width=600, height=500, bg="white")
canvas.pack()

# Number of lanes (10 horizontal lanes)
num_lanes = 10
lane_height = 500 // num_lanes  # Height of each lane

# Game variables
player_width = 30
player_height = 30
player_lane = 5  # Start at the middle lane (lane 5)

collectibles = []
collectible_width = 20
collectible_height = 20
collectible_speed = 5
score = 0

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


class Player:
    def __init__(self):
        self.x1 = 50
        self.x2 = 50 + player_width
        self.y1 = player_lane * lane_height
        self.y2 = player_lane * lane_height + player_height
        self.lane = 5
        self.width = player_width
        self.height = player_height
        self.id = canvas.create_rectangle(50, 5 * lane_height, 50 + player_width,
                                player_lane * lane_height + player_height, fill="blue")

    def move(self, event):
        lane_diff = 0
        if event.keysym == 'Up' and self.lane > 0:
            lane_diff = -1
            self.lane -= 1  # Move up one lane
        elif event.keysym == 'Down' and self.lane < num_lanes - 1:
            lane_diff = 1
            self.lane += 1  # Move down one lane
        elif event.keysym in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            lane_diff = int(event.keysym) - self.lane
            self.lane = int(event.keysym)  # Move directly to a specified lane
        for i in range(1, 7):
            self.y1 = (self.lane - lane_diff * (1 - i / 6)) * lane_height
            self.y2 = (self.lane - lane_diff * (1 - i / 6)) * lane_height + self.height
            canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)
            canvas.update()
            canvas.after(10)


# Here we have a class for collectibles. It is just a canvas rectangle, but it also has a price associated with it.
class Collectible:
    def __init__(self, price, lane):
        y1 = lane * lane_height + 5
        self.price = price
        self.lane = lane
        self.x1 = 600
        self.x2 = 600 + collectible_width
        self.y1 = y1
        self.y2 = y1 + collectible_height

        def rgb_to_hex(r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'

        self.id = canvas.create_rectangle(600, y1, 600 + collectible_width, y1 + collectible_height,
                                          fill=rgb_to_hex(2*price**2, int(255/(2*price**2)), 0))

    def move(self):
        self.x1 -= collectible_speed
        self.x2 -= collectible_speed
        canvas.move(self.id, -collectible_speed, 0)

    def check_collision(self):
        if (player.x1 + player.width > self.x1 > player.x1 - collectible_width and
                (player.lane + 1) * lane_height > self.y1 > player.lane * lane_height - collectible_height):
            return True
        return False


# Function to create new collectibles
def create_collectible():
    lane = random.randint(0, num_lanes - 1)  # Random lane for collectible
    price_tag = random.randint(1, 100)
    if price_tag < 33:
        collectibles.append(Collectible(1, lane))
    elif price_tag < 66:
        collectibles.append(Collectible(5, lane))
    else:
        collectibles.append(Collectible(10, lane))
    canvas.after(1000, create_collectible)


# Function to move collectibles
def move_collectibles():
    global score
    for collectible in collectibles[:]:
        collectible.move()  # Move left

        # Check if the collectible is off screen
        if collectible.x2 < 0:
            canvas.delete(collectible.id)
            collectibles.remove(collectible)

        # Check for collision with player
        if collectible.check_collision():
            canvas.delete(collectible.id)
            collectibles.remove(collectible)
            score += collectible.price
            # Update score label
            score_label.config(text=f"Score: {score}")

    # Schedule the next move
    window.after(60, move_collectibles)


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

    # Create the player
    player = Player()
    score_label.pack()  # Display score


    # Bind keys for movement
    window.bind("<Up>", player.move)
    window.bind("<Down>", player.move)
    for i in range(10):
        window.bind(str(i), player.move)

    # Start the game loop
    create_collectible()
    move_collectibles()


# Create Main Menu
main_menu_frame = tk.Frame(window)

# Add a "Play" button
play_button = tk.Button(main_menu_frame, text="Play", font=("Helvetica", 20), command=start_game)
play_button.pack(pady=20)

# Add the main menu frame to the window
main_menu_frame.pack()


# Start the Tkinter event loop
window.mainloop()
