import itertools
import tkinter as tk
from tkinter import messagebox

# Constants
BOARD_SIZE = 3

# Create the game board
board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Create the main window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Get the original background color for use in the dark mode toggle
original_bg = window.cget("bg")

# Function to start a new game
def new_game():
    """
    Resets the game board and updates the GUI.
    """
    global board
    board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    update_board_gui()

    # Clear the memo dict
    memo.clear()

# Function to toggle dark mode
def toggle_dark_mode():
    """
    Toggles the dark mode of the GUI.
    """
    current_bg = window.cget("bg")
    if current_bg == original_bg:
        window.configure(bg="#1f1f1f")  # Dark gray background
        for row in buttons:
            for button in row:
                button.configure(
                    bg="#333333",
                    fg="#ffffff",
                    activebackground="#333333",
                    activeforeground="#ffffff",
                )  # Dark gray button with white text
    else:
        window.configure(bg=original_bg)
        for row in buttons:
            for button in row:
                button.configure(
                    bg=original_bg,
                    fg="#000000",
                    activebackground=original_bg,
                    activeforeground="#000000",
                )  # Original background with black text

# Function to make a move
def make_move(row, col):
    """
    Makes a move on the game board and updates the GUI.
    Checks for a win or tie after the move.
    """
    if board[row][col] == " ":
        board[row][col] = "X"
        update_board_gui()
        if check_winner("X"):
            end_game("X")
        else:
            ai_move()
            if check_winner("O"):
                end_game("O")
            elif is_board_full():
                end_game("tie")

# Function for AI move
def ai_move():
    """
    Makes a move for the AI player using the minimax algorithm.
    Updates the game board and GUI.
    """
    best_score = float("-inf")
    best_move = None
    for i, j in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)):
        if board[i][j] == " ":
            board[i][j] = "O"
            score = minimax(board, 0, False, float("-inf"), float("inf"))
            board[i][j] = " "
            if score > best_score:
                best_score = score
                best_move = (i, j)
    if best_move is not None:
        row, col = best_move
        board[row][col] = "O"
        update_board_gui()


# Function to check for a win or tie
def check_line(char, *args):
    """
    Checks if all the cells in a line contain the same character.
    """
    return all(cell == char for cell in args)

# Function to evaluate the score of a board state
def evaluate(board):
    """
    Evaluates the score of a board state.
    Returns -1 if X wins, 1 if O wins, and 0 for a tie or no winner.
    """
    for i in range(BOARD_SIZE):
        if check_line("X", *board[i]) or check_line(
            "X", *[board[j][i] for j in range(BOARD_SIZE)]
        ):
            return -1
        if check_line("O", *board[i]) or check_line(
            "O", *[board[j][i] for j in range(BOARD_SIZE)]
        ):
            return 1
    if check_line("X", *[board[i][i] for i in range(BOARD_SIZE)]) or check_line(
        "X", *[board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)]
    ):
        return -1
    if check_line("O", *[board[i][i] for i in range(BOARD_SIZE)]) or check_line(
        "O", *[board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)]
    ):
        return 1
    return 0

# Create a dictionary to store memoized scores
memo = {}

# Function for minimax algorithm with alpha-beta pruning and memoization
def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning and memoization.
    Returns the best score for the current board state.
    """
    score = evaluate(board)
    if score != 0:
        return score
    if is_board_full():
        return 0

    # Generate a unique key for the current board state
    key = tuple(tuple(row) for row in board)

    # Check if the score for the current board state is already memoized
    if key in memo:
        return memo[key]

    best_score = float("-inf") if is_maximizing else float("inf")

    possible_moves = [
        (i, j)
        for i, j in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE))
        if board[i][j] == " "
    ]

    # Sort the possible moves based on their potential scores
    possible_moves.sort(key=lambda move: get_move_score(move, is_maximizing), reverse=is_maximizing)

    for move in possible_moves:
        i, j = move
        board[i][j] = "O" if is_maximizing else "X"
        score = minimax(board, depth + 1, not is_maximizing, alpha, beta)
        board[i][j] = " "
        if is_maximizing:
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(score, best_score)
            beta = min(beta, best_score)
        if beta <= alpha:
            break

    # Memoize the score for the current board state
    memo[key] = best_score

    return best_score

# Function to get the score of a move
def get_move_score(move, is_maximizing):
    """
    Returns the score of a move for the minimax algorithm.
    """
    i, j = move
    board[i][j] = "O" if is_maximizing else "X"
    score = evaluate(board)
    board[i][j] = " "
    return score

# Function to check if the board is full
def is_board_full():
    """
    Checks if the game board is full.
    """
    return all(" " not in row for row in board)

# Function to check if there is a winner
def check_winner(player):
    """
    Checks if a player has won the game.
    """
    for i in range(BOARD_SIZE):
        if check_line(player, *board[i]) or check_line(
            player, *[board[j][i] for j in range(BOARD_SIZE)]
        ):
            return True
    return check_line(player, *[board[i][i] for i in range(BOARD_SIZE)]) or check_line(
        player, *[board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)]
    )

# Function to update the board GUI
def update_board_gui():
    """
    Updates the GUI to reflect the current game board.
    """
    for i, j in itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)):
        buttons[i][j].config(
            text=board[i][j], state=tk.DISABLED if board[i][j] != " " else tk.NORMAL
        )

# Function to end the game
def end_game(result):
    """
    Ends the game and displays the result in a message box.
    """
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)
    if result == "tie":
        messagebox.showinfo("Game Over!", "It's a tie!")
    else:
        messagebox.showinfo("Game Over!", f"{result} wins!")

# Create the menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create the "Game" menu
game_menu = tk.Menu(menu_bar, tearoff=0)
game_menu.add_command(label="New Game", command=new_game)
game_menu.add_separator()
game_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="Game", menu=game_menu)

# Create the "Design" menu
design_menu = tk.Menu(menu_bar, tearoff=0)
design_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
menu_bar.add_cascade(label="Design", menu=design_menu)

# Create the buttons for the game board
buttons = []
for i in range(BOARD_SIZE):
    row = []
    for j in range(BOARD_SIZE):
        button = tk.Button(
            window,
            text=" ",
            width=3,
            height=1,
            font=("Century Gothic", 18),
            command=lambda i=i, j=j: make_move(i, j),
        )
        button.grid(row=i + 1, column=j, padx=0.5, pady=0.5)
        row.append(button)
    buttons.append(row)

# Start the game
window.mainloop()
