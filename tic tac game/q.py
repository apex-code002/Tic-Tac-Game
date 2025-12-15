

import tkinter as tk
from tkinter import messagebox
import math


def check_winner(board, player):
    win_patterns = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_patterns)


def is_draw(board):
    return " " not in board


def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]



def minimax(board, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = "X"
            score = minimax(board, True)
            board[move] = " "
            best_score = min(best_score, score)
        return best_score


def computer_move(board):
    best_score = -math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = "O"
        score = minimax(board, False)
        board[move] = " "
        if score > best_score:
            best_score = score
            best_move = move
    return best_move



class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe – Advanced Python Project")
        self.board = [" "] * 9
        self.buttons = []
        self.single_player = True
        self.create_menu()
        self.create_board()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Single Player", command=self.set_single)
        game_menu.add_command(label="Two Player", command=self.set_two)
        game_menu.add_separator()
        game_menu.add_command(label="Restart", command=self.reset_game)
        game_menu.add_command(label="Exit", command=self.root.quit)

    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(9):
            btn = tk.Button(frame, text=" ", font=("Arial", 24), width=5, height=2,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def on_click(self, index):
        if self.board[index] != " ":
            return

        self.make_move(index, "X")
        if self.check_game_over("X"):
            return

        if self.single_player:
            ai_index = computer_move(self.board)
            self.make_move(ai_index, "O")
            self.check_game_over("O")

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)

    def check_game_over(self, player):
        if check_winner(self.board, player):
            messagebox.showinfo("Game Over", f"{player} wins!")
            self.reset_game()
            return True
        if is_draw(self.board):
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [" "] * 9
        for btn in self.buttons:
            btn.config(text=" ")

    def set_single(self):
        self.single_player = True
        self.reset_game()

    def set_two(self):
        self.single_player = False
        self.reset_game()



if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
3