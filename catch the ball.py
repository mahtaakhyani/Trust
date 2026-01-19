import tkinter as tk
import random
import os
from datetime import datetime

# Game Setup
root = tk.Tk()
root.title("Surprise Ball Game")
canvas = tk.Canvas(root, width=400, height=500, bg="white")
canvas.pack()

# Game state
game_state = "start"  # start, playing, paused_anxiety, won, lost

# Game state variables
bar = None
balls = []  # List of active balls: [canvas_id, speed, x_pos]
base_ball_speed = 5.0
next_ball_delay = 0
consecutive_catches = 0
consecutive_misses = 0
score = 0
score_text = None
num_balls = 1  # Number of balls to spawn
ball_spawn_delays = []  # Track delays for multiple balls

# Movement state tracking
moving_left = False
moving_right = False
bar_speed = 8

# Anxiety and data tracking
anxiety_data = []  # List of anxiety measurements
current_speed_stats = {}  # Track stats for current speed: {speed: float, caught: int, missed: int}
all_speed_stats = []  # List of all speed periods with stats
previous_speed = 5.0
previous_num_balls = 1
anxiety_response = None
anxiety_scale_var = None

def reset_game():
    """Reset all game variables to initial state"""
    global bar, balls, base_ball_speed, next_ball_delay
    global consecutive_catches, consecutive_misses, score, num_balls, game_state
    global ball_spawn_delays, anxiety_data, current_speed_stats, all_speed_stats
    global previous_speed, previous_num_balls
    
    canvas.delete("all")
    bar = None
    balls = []
    base_ball_speed = 5.0
    next_ball_delay = random.randint(10, 30)
    consecutive_catches = 0
    consecutive_misses = 0
    score = 0
    num_balls = 1
    ball_spawn_delays = []
    game_state = "playing"
    anxiety_data = []
    current_speed_stats = {"speed": 5.0, "caught": 0, "missed": 0}
    all_speed_stats = []
    previous_speed = 5.0
    previous_num_balls = 1

def show_start_screen():
    """Display the start screen with rules"""
    global game_state
    game_state = "start"
    canvas.delete("all")
    
    # Title
    canvas.create_text(200, 100, text="Catch the Ball!", fill="black", font=("Arial", 24, "bold"))
    
    # Rules
    rules = [
        "Rules:",
        "• Use LEFT/RIGHT arrows to move",
        "• Catch balls to earn points",
        "• Faster balls = more points",
        "• After 3 catches: speed changes randomly",
        "• After 3 misses: speed decreases",
        "• After 10 catches: another ball appears!",
        "• Win at 1000 points",
        "• Lose at -10 points",
        "• You'll be asked about anxiety",
        "  after each change"
    ]
    
    y_pos = 160
    for rule in rules:
        canvas.create_text(200, y_pos, text=rule, fill="black", font=("Arial", 11))
        y_pos += 22
    
    # Start button
    start_btn = tk.Button(root, text="Start the Game", command=start_game, 
                          font=("Arial", 14), bg="green", fg="white", width=15, height=2)
    canvas.create_window(200, 420, window=start_btn)

def start_game():
    """Initialize and start the game"""
    show_anxiety_screen()
    reset_game()
    initialize_game()

def initialize_game():
    """Set up the game elements"""
    global bar, score_text
    
    # Create bar
    bar = canvas.create_rectangle(150, 470, 250, 480, fill="blue")
    
    # Create score text
    score_text = canvas.create_text(100, 20, text=f"Score: {score} | Speed: {base_ball_speed:.1f}", fill="black")
    
    # Bind keys
    root.bind("<KeyPress-Left>", start_move_left)
    root.bind("<KeyRelease-Left>", stop_move_left)
    root.bind("<KeyPress-Right>", start_move_right)
    root.bind("<KeyRelease-Right>", stop_move_right)
    root.focus_set()
    
    # Start game loop
    game_loop()

def show_anxiety_screen():
    """Display anxiety measurement screen"""
    global game_state, anxiety_scale_var, anxiety_response
    game_state = "paused_anxiety"
    anxiety_response = None
    
    # Store ball positions before overlay
    ball_positions = []
    for ball_data in balls:
        coords = canvas.coords(ball_data[0])
        if coords:
            ball_positions.append(coords)
        else:
            ball_positions.append(None)
    
    # Create overlay with tag
    canvas.create_rectangle(0, 0, 400, 500, fill="lightgray", stipple="gray50", tags="anxiety_overlay")
    
    # Question
    canvas.create_text(200, 150, text="How much anxiety do you feel", 
                      fill="black", font=("Arial", 16, "bold"), tags="anxiety_overlay")
    canvas.create_text(200, 180, text="right now in your body?", 
                      fill="black", font=("Arial", 16, "bold"), tags="anxiety_overlay")
    
    # Scale labels
    canvas.create_text(200, 230, text="0 = Not anxious at all", fill="black", font=("Arial", 12), tags="anxiety_overlay")
    canvas.create_text(200, 260, text="5 = Really anxious", fill="black", font=("Arial", 12), tags="anxiety_overlay")
    
    # Scale variable
    anxiety_scale_var = tk.IntVar(value=0)
    
    # Scale buttons
    button_frame = tk.Frame(root)
    canvas.create_window(200, 320, window=button_frame, tags="anxiety_overlay")
    
    for i in range(6):
        btn = tk.Radiobutton(button_frame, text=str(i), variable=anxiety_scale_var, 
                            value=i, font=("Arial", 14), width=3, height=2,
                            indicatoron=False, selectcolor="lightblue")
        btn.pack(side=tk.LEFT, padx=5)
    
    # Submit button
    def submit_anxiety():
        global anxiety_response, game_state, current_speed_stats
        anxiety_response = anxiety_scale_var.get()
        # Store current speed stats before moving to next
        if current_speed_stats["caught"] > 0 or current_speed_stats["missed"] > 0:
            all_speed_stats.append(current_speed_stats.copy())
        anxiety_data.append({
            "anxiety_level": anxiety_response,
            "speed": base_ball_speed,
            "num_balls": num_balls,
            "timestamp": datetime.now().isoformat()
        })
        # Reset current stats for new speed period
        current_speed_stats["speed"] = base_ball_speed
        current_speed_stats["caught"] = 0
        current_speed_stats["missed"] = 0
        game_state = "playing"
        # Remove only the overlay
        canvas.delete("anxiety_overlay")
        # Restore ball positions if needed
        for i, ball_data in enumerate(balls):
            if i < len(ball_positions) and ball_positions[i] is not None:
                canvas.coords(ball_data[0], *ball_positions[i])
        game_loop()
    
    submit_btn = tk.Button(root, text="Submit", command=submit_anxiety,
                          font=("Arial", 12), bg="green", fg="white", width=10, height=2)
    canvas.create_window(200, 400, window=submit_btn, tags="anxiety_overlay")

def check_for_anxiety_question():
    """Check if we need to show anxiety question (after speed or ball count change)"""
    global previous_speed, previous_num_balls
    
    if base_ball_speed != previous_speed or num_balls != previous_num_balls:
        previous_speed = base_ball_speed
        previous_num_balls = num_balls
        show_anxiety_screen()
        return True
    return False

def show_win_screen():
    """Display the win screen"""
    global game_state
    game_state = "won"
    save_results()
    canvas.delete("all")
    
    canvas.create_text(200, 200, text="You Win!", fill="green", font=("Arial", 30, "bold"))
    canvas.create_text(200, 250, text=f"Final Score: {score}", fill="black", font=("Arial", 16))
    
    # Buttons
    play_again_btn = tk.Button(root, text="Play Again", command=start_game,
                               font=("Arial", 12), bg="green", fg="white", width=12, height=2)
    quit_btn = tk.Button(root, text="Quit", command=root.quit,
                         font=("Arial", 12), bg="red", fg="white", width=12, height=2)
    
    canvas.create_window(200, 320, window=play_again_btn)
    canvas.create_window(200, 380, window=quit_btn)

def show_lose_screen():
    """Display the lose screen"""
    global game_state
    game_state = "lost"
    save_results()
    canvas.delete("all")
    
    canvas.create_text(200, 200, text="You Lost!", fill="red", font=("Arial", 30, "bold"))
    canvas.create_text(200, 250, text=f"Final Score: {score}", fill="black", font=("Arial", 16))
    
    # Buttons
    play_again_btn = tk.Button(root, text="Play Again", command=start_game,
                               font=("Arial", 12), bg="green", fg="white", width=12, height=2)
    quit_btn = tk.Button(root, text="Quit", command=root.quit,
                         font=("Arial", 12), bg="red", fg="white", width=12, height=2)
    
    canvas.create_window(200, 320, window=play_again_btn)
    canvas.create_window(200, 380, window=quit_btn)

def save_results():
    """Save results to a file with timestamp"""
    # Create results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(results_dir, f"{timestamp}.py")
    
    # Prepare results dictionary
    results = {
        "game_end_time": datetime.now().isoformat(),
        "final_score": score,
        "anxiety_measurements": anxiety_data,
        "speed_periods": all_speed_stats
    }
    
    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Game Results\n")
        f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
        f.write("results = ")
        f.write(str(results))
        f.write("\n")

def start_move_left(event):
    global moving_left
    if game_state == "playing":
        moving_left = True

def stop_move_left(event):
    global moving_left
    moving_left = False

def start_move_right(event):
    global moving_right
    if game_state == "playing":
        moving_right = True

def stop_move_right(event):
    global moving_right
    moving_right = False

def game_loop():
    global score, base_ball_speed, next_ball_delay
    global consecutive_catches, consecutive_misses, num_balls, game_state
    global moving_left, moving_right, current_speed_stats
    
    if game_state != "playing":
        return
    
    
    # Handle continuous bar movement
    if bar:
        if moving_left and canvas.coords(bar)[0] > 0:
            canvas.move(bar, -bar_speed, 0)
        if moving_right and canvas.coords(bar)[2] < 400:
            canvas.move(bar, bar_speed, 0)
    
    # Handle ball spawning with delays for multiple balls
    # Process any pending spawn delays
    for i in range(len(ball_spawn_delays) - 1, -1, -1):
        ball_spawn_delays[i] -= 1
        if ball_spawn_delays[i] <= 0:
            # Spawn a ball
            ball_x = random.randint(0, 380)
            ball_id = canvas.create_oval(ball_x, 0, ball_x + 20, 20, fill="red")
            balls.append([ball_id, base_ball_speed, ball_x])
            ball_spawn_delays.pop(i)
    
    # Check if we need to start spawning new balls
    if len(balls) < num_balls and next_ball_delay > 0:
        next_ball_delay -= 1
        root.after(20, game_loop)
        return
    
    # Start spawning balls with delays between them
    if len(balls) < num_balls and next_ball_delay == 0:
        balls_to_spawn = num_balls - len(balls)
        for i in range(balls_to_spawn):
            if i == 0:
                # First ball spawns immediately
                ball_x = random.randint(0, 380)
                ball_id = canvas.create_oval(ball_x, 0, ball_x + 20, 20, fill="red")
                balls.append([ball_id, base_ball_speed, ball_x])
            else:
                # Subsequent balls have delays (20-40 frames = 400-800ms)
                ball_spawn_delays.append(random.randint(20, 40))
        next_ball_delay = random.randint(10, 50)
    
    # Move active balls
    balls_to_remove = []
    bar_pos = canvas.coords(bar) if bar else []
    speed_changed = False
    balls_changed = False
    
    for ball_data in balls:
        ball_id, ball_speed, _ = ball_data
        canvas.move(ball_id, 0, ball_speed)
        ball_pos = canvas.coords(ball_id)
        
        # Check if ball hits the bar (caught)
        if bar and len(bar_pos) >= 4 and ball_pos[3] >= 470 and ball_pos[2] > bar_pos[0] and ball_pos[0] < bar_pos[2]:
            # Track consecutive catches and reset misses
            consecutive_catches += 1
            consecutive_misses = 0
            current_speed_stats["caught"] += 1
            
            # After 10 consecutive catches, add another ball
            if consecutive_catches == 10:
                num_balls += 1
                consecutive_catches = 0
                balls_changed = True
            
            # After 3, 6, or 9 consecutive catches, change speed randomly
            elif consecutive_catches % 3 == 0:
                speed_change = random.uniform(-2.0, 2.5)
                base_ball_speed = max(2.0, min(base_ball_speed + speed_change, 12.0))
                speed_changed = True
            
            # Scoring: 10 points per speed unit
            points_earned = int(ball_speed * 10)
            score += points_earned
            canvas.itemconfig(score_text, text=f"Score: {score} | Speed: {base_ball_speed:.1f}")
            canvas.delete(ball_id)
            balls_to_remove.append(ball_data)
            
            # Check win condition
            if score >= 1000:
                # Save final speed period stats
                if current_speed_stats["caught"] > 0 or current_speed_stats["missed"] > 0:
                    all_speed_stats.append(current_speed_stats.copy())
                show_win_screen()
                return
        
        # Check if ball hits the ground (missed)
        elif ball_pos[3] >= 500:
            # Track consecutive misses and reset catches
            consecutive_misses += 1
            consecutive_catches = 0
            current_speed_stats["missed"] += 1
            
            # After 3 consecutive misses, randomly decrease speed
            if consecutive_misses >= 3:
                speed_decrease = random.uniform(0.5, 2.0)
                base_ball_speed = max(2.0, base_ball_speed - speed_decrease)
                speed_changed = True
                consecutive_misses = 0
            
            # Scoring: lose 5 points per speed unit
            points_lost = int(ball_speed * 5)
            score -= points_lost
            canvas.itemconfig(score_text, text=f"Score: {score} | Speed: {base_ball_speed:.1f}")
            canvas.delete(ball_id)
            balls_to_remove.append(ball_data)
            
            # Check lose condition
            if score <= -10:
                # Save final speed period stats
                if current_speed_stats["caught"] > 0 or current_speed_stats["missed"] > 0:
                    all_speed_stats.append(current_speed_stats.copy())
                show_lose_screen()
                return
    
    # Remove caught/missed balls
    for ball_data in balls_to_remove:
        if ball_data in balls:
            balls.remove(ball_data)
    
    # Update speeds for remaining balls
    for ball_data in balls:
        ball_data[1] = base_ball_speed
    
    # Check if we need to show anxiety question
    if speed_changed or balls_changed:
        # Save current speed period stats before showing anxiety
        if current_speed_stats["caught"] > 0 or current_speed_stats["missed"] > 0:
            all_speed_stats.append(current_speed_stats.copy())
        check_for_anxiety_question()
        return
    
    root.after(20, game_loop)

# Show start screen initially
show_start_screen()
root.mainloop()
