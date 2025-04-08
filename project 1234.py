import random

# Grid Initialization
def init_grid(size):
    return [[" " for _ in range(size)] for _ in range(size)]

# Print the Grid
def print_grid(grid):
    size = len(grid)
    for row in grid:
        print("|", " | ".join(row), "|")
        print("-" * (size * 4 - 1))

# Get Grid Size Based on Difficulty
def choose_grid_size():
    while True:
        try:
            level = int(input(
                "Choose Difficulty Level:\n"
                "1. Classic mode (3x3 without Toss)\n"
                "2. Easy mode (3x3 with Toss)\n"
                "3. Medium (4x4 without Toss)\n"
                "4. Hard mode (5x5 without Toss)\n"
                "Enter your choice (1/2/3/4): "
            ))
            
            if level == 1:
                return 3, "classic"
            elif level == 2:
                return 3, "easy"
            elif level == 3:
                return 4, "medium"
            elif level == 4:
                return 5, "hard"
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Enter a number (1, 2, 3, or 4).")

# Toggle Player Turn
def player_turn(turn_player1):
    return not turn_player1

# Write in Cell
def write_cell(cell, player_symbol, grid):
    size = len(grid)
    cell -= 1
    i, j = divmod(cell, size)
    grid[i][j] = player_symbol

# Check if Cell is Free
def free_cell(cell, grid):
    size = len(grid)
    cell -= 1
    i, j = divmod(cell, size)
    return grid[i][j] == " "

# Check for Win
def win_check(player_symbol, grid):
    size = len(grid)
    
    # Check rows and columns
    for i in range(size):
        if all(grid[i][j] == player_symbol for j in range(size)) or \
           all(grid[j][i] == player_symbol for j in range(size)):
            return True

    # Check diagonals
    if all(grid[i][i] == player_symbol for i in range(size)) or \
       all(grid[i][size - 1 - i] == player_symbol for i in range(size)):
        return True
    
    return False

# Check if Grid is Full
def is_full(grid):
    return all(cell != " " for row in grid for cell in row)

# Toss Function
def toss(player_name):
    while True:
        choice = input(f"\n{player_name}, choose Heads or Tails (H/T): ").strip().lower()
        if choice in ['h', 't']:
            break
        print("Invalid choice. Choose 'H' for Heads or 'T' for Tails.")
    
    toss_result = random.choice(['h', 't'])
    print(f"Toss result: {'Heads' if toss_result == 'h' else 'Tails'}")
    
    if choice == toss_result:
        print("You won the toss! You get to play your turn first.")
        return True
    else:
        print("You lost the toss. The opponent goes first.")
        return False

# Challenge Question before Move
def challenge_question():
    questions = [
        ("5 + 7", "12"), ("9 × 3", "27"), ("Half of 100", "50"), ("Square root of 36", "6"),
        ("A triangle with sides 3 cm, 4 cm, and 5 cm is a right triangle (Yes/No)", "Yes"),
        ("Boiling point of water in Celsius", "101"), ("Example of a planet", "Mars"),
        ("Plants release __ during photosynthesis", "oxygen"), ("Main source of energy for Earth", "The Sun"),
        ("Largest organ in the human body", "Skin"), ("Binary representation of 5", "101"),
        ("HTML stands for", "HyperText Markup Language"), ("Example of a basic programming language", "Python"),
        ("An algorithm is", "step-by-step procedure"), ("A loop in programming is", "repeating instructions"),
        ("Capital of India", "New Delhi"), ("Largest ocean", "Pacific"), ("Example of a European country", "France"),
        ("Indian state known for backwaters", "Kerala"), ("Color of the sky during the day", "Blue"),
        ("Father of the Nation in India", "Mahatma Gandhi"), ("Example of an animal that can fly", "Bird"),
        ("Sport with a bat and ball", "Cricket"), ("King of fruits in India", "Mango")
    ]
    question, answer = random.choice(questions)
    user_answer = input(f"Answer this to make your move: {question}? ").strip()
    return user_answer.lower() == answer.lower()

# AI Move (Random Valid Move)
def ai_move(grid, ai_symbol):
    size = len(grid)
    empty_cells = [i * size + j + 1 for i in range(size) for j in range(size) if grid[i][j] == " "]
    return random.choice(empty_cells) if empty_cells else None

# Game Start
print("Welcome to Tic-Tac-Toe with Toss!")
mode = input("Do you want to play against another player (P) or AI (A)? ").strip().lower()
player1 = input("Enter Player 1's name: ")
while True:
    player1_symbol = input(f"{player1}, choose your symbol (X/O): ").strip().upper()
    if player1_symbol in ['X', 'O']:
        break
    print("Invalid choice. Choose either 'X' or 'O'.")

if mode == "p":
    player2 = input("Enter Player 2's name: ")
    player2_symbol = 'O' if player1_symbol == 'X' else 'X'
else:
    player2 = "AI"
    player2_symbol = 'O' if player1_symbol == 'X' else 'X'

# Select Grid Size and Mode
grid_size, game_mode = choose_grid_size()
grid = init_grid(grid_size)

# Toss if Easy Mode
turn_player1 = True
if game_mode == "easy":
    turn_player1 = toss(player1)

game_active = True
winner = None

# Main Game Loop
while game_active:
    print_grid(grid)
    
    if turn_player1 or mode == "p":
        current_player = player1 if turn_player1 else player2
        player_symbol = player1_symbol if turn_player1 else player2_symbol
    else:
        current_player = "AI"
        player_symbol = player2_symbol
        cell = ai_move(grid, player_symbol)
        print(f"AI chooses cell {cell}")
    
    if current_player != "AI":
        if not challenge_question():
            print(f"Wrong answer! {current_player} loses this turn.")
            turn_player1 = player_turn(turn_player1)
            continue
        cell = int(input(f"{current_player}'s turn ({player_symbol}). Enter cell: "))
    
    if 1 <= cell <= grid_size**2 and free_cell(cell, grid):
        write_cell(cell, player_symbol, grid)
        if win_check(player_symbol, grid):
            winner = current_player
            game_active = False
            break
        if is_full(grid):
            game_active = False
            break
        turn_player1 = player_turn(turn_player1)

print_grid(grid)
print(f"🎉 {winner} wins! 🎉" if winner else "It's a draw! 🤝")