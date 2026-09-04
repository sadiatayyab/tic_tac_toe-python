"""
Ultimate Tic Tac Toe — Python Tkinter Edition
------------------------------------------------
Features:
- Human vs Human
- Human vs AI
- AI vs AI with Start / Pause / Resume
- Easy, Medium, Hard (Minimax) AI
- Dark / Light themes
- Responsive Canvas board
- Scoreboard, draws, total games, streak tracking
- Winning tiles become green
- Keyboard support
- Professional menu bar
- How to Play and About dialogs

Run:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


# =============================================================================
# Constants
# =============================================================================

APP_TITLE = "Ultimate Tic Tac Toe — Python Tkinter Edition"

FONT = "Segoe UI"
DISPLAY_FONT = "Georgia"

WINDOW_WIDTH = 1220
WINDOW_HEIGHT = 820
MIN_WIDTH = 1080
MIN_HEIGHT = 720

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

MODE_HUMAN = "Human vs Human"
MODE_AI = "Human vs AI"
MODE_AI_AI = "AI vs AI"

DIFFICULTIES = ("Easy", "Medium", "Hard")

AI_SPEEDS = {
    "Very Fast": 180,
    "Fast": 380,
    "Normal": 750,
    "Slow": 1250,
}


# =============================================================================
# Theme Manager
# =============================================================================


class ThemeManager:
    """Centralized dark/light theme manager."""

    THEMES = {
        "Dark": {
            "bg": "#08111F",
            "header": "#0A1626",
            "surface": "#0F1E32",
            "surface_2": "#14283F",
            "input": "#13263B",
            "border": "#244361",
            "border_soft": "#1A334D",
            "nav": "#102238",
            "nav_hover": "#183653",
            "text": "#EAF3FB",
            "muted": "#96AABD",
            "accent": "#4E9BD4",
            "accent_soft": "#214A6B",
            "primary": "#1C6FAA",
            "primary_hover": "#2784C5",
            "secondary": "#17314A",
            "secondary_hover": "#204563",
            "danger": "#A8444D",
            "danger_hover": "#C65560",
            "disabled": "#1B2835",
            "x": "#78BBEE",
            "o": "#F18A9B",
            "win": "#2F9B6F",
            "win_light": "#56B88B",
            "win_text": "#FFFFFF",
            "draw": "#CDA85B",
            "draw_tile": "#2C2A24",
            "board": "#0B192A",
            "board_highlight": "#1B4161",
            "tile": "#102941",
            "tile_hover": "#1A3D5E",
            "tile_pressed": "#245276",
            "tile_outline": "#234563",
            "tile_shadow": "#040A11",
            "mark_shadow": "#07111C",
        },
        "Light": {
            "bg": "#EEF4F8",
            "header": "#F9FCFE",
            "surface": "#FFFFFF",
            "surface_2": "#F5F9FC",
            "input": "#F4F8FB",
            "border": "#BBD0DE",
            "border_soft": "#D4E1EA",
            "nav": "#EDF4F8",
            "nav_hover": "#D8E8F2",
            "text": "#182939",
            "muted": "#60798C",
            "accent": "#317AAD",
            "accent_soft": "#D6E8F4",
            "primary": "#347DAC",
            "primary_hover": "#4D94C2",
            "secondary": "#DCEAF2",
            "secondary_hover": "#C8DCE8",
            "danger": "#C35A63",
            "danger_hover": "#D56E77",
            "disabled": "#D8E0E5",
            "x": "#2E7EB5",
            "o": "#C85D70",
            "win": "#4A9C71",
            "win_light": "#6AB98B",
            "win_text": "#FFFFFF",
            "draw": "#AB8742",
            "draw_tile": "#F2E9D3",
            "board": "#E4EFF6",
            "board_highlight": "#C5DDEA",
            "tile": "#F9FCFE",
            "tile_hover": "#E6F1F8",
            "tile_pressed": "#D5E8F3",
            "tile_outline": "#B7CFDE",
            "tile_shadow": "#BCCDD8",
            "mark_shadow": "#D7E1E8",
        },
    }

    def __init__(self):
        self.current_theme = "Dark"

    @property
    def colors(self):
        return self.THEMES[self.current_theme]

    def set_theme(self, theme_name):
        if theme_name in self.THEMES:
            self.current_theme = theme_name


# =============================================================================
# Game Engine
# =============================================================================


class GameEngine:
    """Pure Tic Tac Toe game logic. No GUI code."""

    def __init__(self):
        self.reset_board("X")

    @staticmethod
    def other_player(player):
        return "O" if player == "X" else "X"

    @staticmethod
    def check_board(board):
        """
        Returns:
            (winner, winning_cells)

        winner may be:
            "X", "O", "Draw", or None
        """
        for line in WINNING_LINES:
            a, b, c = line

            if board[a] and board[a] == board[b] == board[c]:
                return board[a], line

        if "" not in board:
            return "Draw", None

        return None, None

    def reset_board(self, starter="X"):
        self.board = [""] * 9
        self.current_player = starter
        self.starting_player = starter

        self.winner = None
        self.winning_cells = None
        self.game_over = False

        self.last_move = None
        self.history = []

    def get_available_moves(self):
        return [index for index, value in enumerate(self.board) if value == ""]

    def make_move(self, index):
        """
        Try to place a mark.

        Returns:
            success, player_or_none, message
        """
        if self.game_over:
            return False, None, "This round has already finished."

        if not isinstance(index, int) or index < 0 or index > 8:
            return False, None, "Invalid board cell."

        if self.board[index] != "":
            return False, None, "Cell already occupied."

        player = self.current_player

        self.board[index] = player
        self.history.append((index, player))
        self.last_move = index

        winner, winning_cells = self.check_board(self.board)

        if winner:
            self.winner = winner
            self.winning_cells = winning_cells
            self.game_over = True
        else:
            self.current_player = self.other_player(player)

        return True, player, ""

    def rebuild_from_history(self, history):
        """
        Rebuild the engine after Undo.
        """
        starter = self.starting_player
        self.reset_board(starter)

        for index, _player in history:
            self.make_move(index)


# =============================================================================
# Score Manager
# =============================================================================


class ScoreManager:
    """Tracks scores and basic match statistics."""

    def __init__(self):
        self.reset_scores()

    def reset_scores(self):
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.total_games = 0

        self.current_streak_symbol = None
        self.current_streak_count = 0
        self.best_streak = 0

    def record_result(self, result):
        self.total_games += 1

        if result == "X":
            self.x_wins += 1
            self._update_streak("X")

        elif result == "O":
            self.o_wins += 1
            self._update_streak("O")

        elif result == "Draw":
            self.draws += 1
            self.current_streak_symbol = None
            self.current_streak_count = 0

    def revert_result(self, result):
        """
        Used by Undo after a completed round.
        It safely decreases the visible score.
        """
        self.total_games = max(0, self.total_games - 1)

        if result == "X":
            self.x_wins = max(0, self.x_wins - 1)

        elif result == "O":
            self.o_wins = max(0, self.o_wins - 1)

        elif result == "Draw":
            self.draws = max(0, self.draws - 1)

        self.current_streak_symbol = None
        self.current_streak_count = 0

    def _update_streak(self, symbol):
        if self.current_streak_symbol == symbol:
            self.current_streak_count += 1
        else:
            self.current_streak_symbol = symbol
            self.current_streak_count = 1

        self.best_streak = max(self.best_streak, self.current_streak_count)


# =============================================================================
# AI System
# =============================================================================


class TicTacToeAI:
    """
    AI logic separated from GUI.

    Easy:
        Random valid move.

    Medium:
        Win > block > center > corners > random.

    Hard:
        Minimax with alpha-beta pruning.
    """

    def get_move(self, board, player, difficulty):
        available = self.get_available_moves(board)

        if not available:
            return None

        if difficulty == "Easy":
            return self.easy_move(board)

        if difficulty == "Medium":
            return self.medium_move(board, player)

        return self.hard_move(board, player)

    @staticmethod
    def get_available_moves(board):
        return [index for index, value in enumerate(board) if value == ""]

    def easy_move(self, board):
        return random.choice(self.get_available_moves(board))

    def medium_move(self, board, player):
        opponent = GameEngine.other_player(player)
        available = self.get_available_moves(board)

        # 1. Winning move
        for move in available:
            test_board = board[:]
            test_board[move] = player
            winner, _ = GameEngine.check_board(test_board)

            if winner == player:
                return move

        # 2. Block opponent's winning move
        for move in available:
            test_board = board[:]
            test_board[move] = opponent
            winner, _ = GameEngine.check_board(test_board)

            if winner == opponent:
                return move

        # 3. Center
        if 4 in available:
            return 4

        # 4. Corners
        corners = [0, 2, 6, 8]
        open_corners = [move for move in corners if move in available]

        if open_corners:
            return random.choice(open_corners)

        # 5. Any remaining cell
        return random.choice(available)

    def hard_move(self, board, player):
        """
        Minimax chooses the best possible move.
        It prefers quicker wins and delays losses where possible.
        """
        best_score = -float("inf")
        best_move = None
        cache = {}

        # Move order makes Hard mode feel more natural
        preferred_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        available = self.get_available_moves(board)

        ordered_moves = [move for move in preferred_order if move in available]

        for move in ordered_moves:
            test_board = board[:]
            test_board[move] = player

            score = self.minimax(
                board=test_board,
                current_turn=GameEngine.other_player(player),
                ai_player=player,
                depth=0,
                alpha=-float("inf"),
                beta=float("inf"),
                cache=cache,
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, board, current_turn, ai_player, depth, alpha, beta, cache):
        winner, _ = GameEngine.check_board(board)

        if winner == ai_player:
            return 10 - depth

        if winner == GameEngine.other_player(ai_player):
            return depth - 10

        if winner == "Draw":
            return 0

        key = (tuple(board), current_turn, ai_player)

        if key in cache:
            return cache[key]

        available = self.get_available_moves(board)

        if current_turn == ai_player:
            best_score = -float("inf")

            for move in available:
                board[move] = current_turn

                score = self.minimax(
                    board,
                    GameEngine.other_player(current_turn),
                    ai_player,
                    depth + 1,
                    alpha,
                    beta,
                    cache,
                )

                board[move] = ""

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        else:
            best_score = float("inf")

            for move in available:
                board[move] = current_turn

                score = self.minimax(
                    board,
                    GameEngine.other_player(current_turn),
                    ai_player,
                    depth + 1,
                    alpha,
                    beta,
                    cache,
                )

                board[move] = ""

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        cache[key] = best_score
        return best_score


# =============================================================================
# Canvas Helpers
# =============================================================================


def mix_colors(color_1, color_2, amount):
    """Blend two #RRGGBB colours."""
    rgb_1 = [int(color_1[index : index + 2], 16) for index in (1, 3, 5)]
    rgb_2 = [int(color_2[index : index + 2], 16) for index in (1, 3, 5)]

    return "#%02x%02x%02x" % tuple(
        int(rgb_1[index] + (rgb_2[index] - rgb_1[index]) * amount) for index in range(3)
    )


def rounded_rectangle_points(x1, y1, x2, y2, radius):
    radius = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)

    return [
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]


def canvas_round_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    return canvas.create_polygon(
        rounded_rectangle_points(x1, y1, x2, y2, radius),
        smooth=True,
        **kwargs,
    )


# =============================================================================
# Custom Hover Button
# =============================================================================


class ThemedButton(tk.Label):
    """A modern custom Label-based button with hover and pressed states."""

    def __init__(
        self,
        app,
        parent,
        text,
        command,
        variant="secondary",
        font_size=9,
        padx=14,
        pady=8,
    ):
        super().__init__(
            parent,
            text=text,
            font=(FONT, font_size, "bold"),
            padx=padx,
            pady=pady,
            cursor="hand2",
            bd=0,
            relief="flat",
        )

        self.app = app
        self.command = command
        self.variant = variant

        self.enabled = True
        self.active = False
        self.hovered = False
        self.pressed = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self.app.button_widgets.append(self)
        self.apply_theme()

    def set_text(self, text):
        self.config(text=text)

    def set_active(self, active):
        self.active = active
        self.apply_theme()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.hovered = False
        self.pressed = False
        self.apply_theme()

    def _on_enter(self, _event):
        if self.enabled:
            self.hovered = True
            self.apply_theme()

    def _on_leave(self, _event):
        self.hovered = False
        self.pressed = False
        self.apply_theme()

    def _on_press(self, _event):
        if self.enabled:
            self.pressed = True
            self.apply_theme()

    def _on_release(self, _event):
        was_pressed = self.pressed
        self.pressed = False
        self.apply_theme()

        if self.enabled and was_pressed:
            self.command()

    def apply_theme(self):
        if not self.winfo_exists():
            return

        background, foreground = self.app.get_button_colors(
            self.variant,
            self.hovered,
            self.pressed,
            self.active,
            self.enabled,
        )

        self.config(
            bg=background,
            fg=foreground,
            cursor="hand2" if self.enabled else "arrow",
        )


# =============================================================================
# Responsive Board Canvas
# =============================================================================


class BoardCanvas(tk.Canvas):
    """Custom Canvas Tic Tac Toe board with hover, pressed, and win animation."""

    def __init__(self, app, parent):
        super().__init__(
            parent,
            width=560,
            height=480,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )

        self.app = app

        self.board_x = 0
        self.board_y = 0
        self.board_size = 0
        self.cell_size = 0
        self.cell_boxes = []

        self.hover_index = None
        self.pressed_index = None
        self.selected_index = None

        self.animating_index = None
        self.animation_progress = 1.0
        self.animation_token = 0
        self.animation_job = None

        self.win_pulse_on = False

        self.bind("<Configure>", self._on_resize)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_resize(self, _event):
        self.after_idle(self.redraw)

    def cancel_animations(self):
        self.animation_token += 1

        if self.animation_job:
            try:
                self.after_cancel(self.animation_job)
            except Exception:
                pass

        self.animation_job = None
        self.animating_index = None
        self.animation_progress = 1.0
        self.win_pulse_on = False

    def redraw(self):
        colors = self.app.colors
        engine = self.app.engine

        self.delete("all")

        width = max(200, self.winfo_width())
        height = max(200, self.winfo_height())

        # Keep board centered and square.
        self.board_size = max(200, min(width - 24, height - 24))
        self.board_x = (width - self.board_size) / 2
        self.board_y = (height - self.board_size) / 2

        # Board background card.
        board_outline = colors["border"]

        if engine.game_over and engine.winner == "Draw":
            board_outline = colors["draw"]

        if engine.game_over and engine.winner in ("X", "O"):
            board_outline = colors["win"]

        canvas_round_rect(
            self,
            self.board_x + 3,
            self.board_y + 5,
            self.board_x + self.board_size + 3,
            self.board_y + self.board_size + 5,
            24,
            fill=colors["tile_shadow"],
            outline="",
        )

        canvas_round_rect(
            self,
            self.board_x,
            self.board_y,
            self.board_x + self.board_size,
            self.board_y + self.board_size,
            24,
            fill=colors["board"],
            outline=board_outline,
            width=2,
        )

        # Simulated glass highlight.
        self.create_line(
            self.board_x + 28,
            self.board_y + 12,
            self.board_x + self.board_size - 28,
            self.board_y + 12,
            fill=mix_colors(colors["board"], "#FFFFFF", 0.14),
            width=1,
        )

        inner_padding = max(14, self.board_size * 0.045)
        gap = max(8, self.board_size * 0.026)

        self.cell_size = (self.board_size - (inner_padding * 2) - (gap * 2)) / 3

        self.cell_boxes = []

        for index in range(9):
            row, column = divmod(index, 3)

            x1 = self.board_x + inner_padding + column * (self.cell_size + gap)
            y1 = self.board_y + inner_padding + row * (self.cell_size + gap)

            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self.cell_boxes.append((x1, y1, x2, y2))

            is_winning = engine.winning_cells and index in engine.winning_cells

            is_draw_state = engine.game_over and engine.winner == "Draw"

            fill = colors["tile"]
            outline = colors["tile_outline"]
            outline_width = 1

            if is_draw_state:
                fill = colors["draw_tile"]
                outline = colors["draw"]

            if is_winning:
                fill = colors["win_light"] if self.win_pulse_on else colors["win"]
                outline = colors["win_light"]
                outline_width = 2

            elif index == self.pressed_index:
                fill = colors["tile_pressed"]
                outline = colors["accent"]
                outline_width = 2

            elif index == self.hover_index:
                fill = colors["tile_hover"]
                outline = colors["accent"]
                outline_width = 2

            elif index == self.selected_index and engine.board[index] == "":
                fill = colors["tile_hover"]
                outline = colors["accent"]
                outline_width = 2

            elif index == engine.last_move:
                outline = colors["x"] if engine.board[index] == "X" else colors["o"]
                outline_width = 2

            # Tile shadow.
            canvas_round_rect(
                self,
                x1 + 2,
                y1 + 4,
                x2 + 2,
                y2 + 4,
                15,
                fill=colors["tile_shadow"],
                outline="",
            )

            # Tile itself.
            canvas_round_rect(
                self,
                x1,
                y1,
                x2,
                y2,
                15,
                fill=fill,
                outline=outline,
                width=outline_width,
            )

            # Soft reflection line.
            self.create_line(
                x1 + 14,
                y1 + 3,
                x2 - 14,
                y1 + 3,
                fill=mix_colors(fill, "#FFFFFF", 0.12),
                width=1,
            )

        # Draw winning combination under marks.
        if engine.winning_cells:
            first = engine.winning_cells[0]
            last = engine.winning_cells[-1]

            x1, y1 = self.cell_center(first)
            x2, y2 = self.cell_center(last)

            self.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=mix_colors(colors["win_text"], colors["win"], 0.35),
                width=max(3, int(self.cell_size * 0.026)),
                capstyle="round",
            )

        # Draw all marks.
        for index, mark in enumerate(engine.board):
            if mark:
                progress = 1.0

                if index == self.animating_index:
                    progress = self.animation_progress

                self.draw_mark(index, mark, progress)

        # Keyboard selection border.
        if (
            self.selected_index is not None
            and engine.board[self.selected_index] == ""
            and not engine.game_over
        ):
            x1, y1, x2, y2 = self.cell_boxes[self.selected_index]

            canvas_round_rect(
                self,
                x1 - 4,
                y1 - 4,
                x2 + 4,
                y2 + 4,
                18,
                fill="",
                outline=colors["accent"],
                width=2,
            )

    def draw_mark(self, index, mark, progress=1.0):
        colors = self.app.colors
        engine = self.app.engine

        x1, y1, x2, y2 = self.cell_boxes[index]
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        size = self.cell_size * 0.27
        width = max(7, int(self.cell_size * 0.115))

        is_winning = engine.winning_cells and index in engine.winning_cells

        if is_winning:
            color = colors["win_text"]
        else:
            color = colors["x"] if mark == "X" else colors["o"]

        shadow = colors["mark_shadow"]

        if mark == "X":
            first_part = min(1.0, progress * 2)
            second_part = max(0.0, progress * 2 - 1)

            # First X stroke shadow.
            self.create_line(
                center_x - size,
                center_y - size,
                center_x - size + (size * 2 * first_part),
                center_y - size + (size * 2 * first_part),
                fill=shadow,
                width=width + 4,
                capstyle="round",
            )

            self.create_line(
                center_x - size,
                center_y - size,
                center_x - size + (size * 2 * first_part),
                center_y - size + (size * 2 * first_part),
                fill=color,
                width=width,
                capstyle="round",
            )

            if second_part > 0:
                self.create_line(
                    center_x + size,
                    center_y - size,
                    center_x + size - (size * 2 * second_part),
                    center_y - size + (size * 2 * second_part),
                    fill=shadow,
                    width=width + 4,
                    capstyle="round",
                )

                self.create_line(
                    center_x + size,
                    center_y - size,
                    center_x + size - (size * 2 * second_part),
                    center_y - size + (size * 2 * second_part),
                    fill=color,
                    width=width,
                    capstyle="round",
                )

        else:
            extent = -359.9 * progress

            if progress < 0.99:
                self.create_arc(
                    center_x - size,
                    center_y - size,
                    center_x + size,
                    center_y + size,
                    start=90,
                    extent=extent,
                    style="arc",
                    outline=shadow,
                    width=width + 4,
                )

                self.create_arc(
                    center_x - size,
                    center_y - size,
                    center_x + size,
                    center_y + size,
                    start=90,
                    extent=extent,
                    style="arc",
                    outline=color,
                    width=width,
                )

            else:
                self.create_oval(
                    center_x - size,
                    center_y - size,
                    center_x + size,
                    center_y + size,
                    outline=shadow,
                    width=width + 4,
                )

                self.create_oval(
                    center_x - size,
                    center_y - size,
                    center_x + size,
                    center_y + size,
                    outline=color,
                    width=width,
                )

    def cell_center(self, index):
        x1, y1, x2, y2 = self.cell_boxes[index]
        return (x1 + x2) / 2, (y1 + y2) / 2

    def get_cell_at(self, x, y):
        for index, (x1, y1, x2, y2) in enumerate(self.cell_boxes):
            if x1 <= x <= x2 and y1 <= y <= y2:
                return index

        return None

    def _on_motion(self, event):
        index = self.get_cell_at(event.x, event.y)

        if (
            index is not None
            and self.app.can_human_move()
            and self.app.engine.board[index] == ""
        ):
            if self.hover_index != index:
                self.hover_index = index
                self.redraw()
        else:
            if self.hover_index is not None:
                self.hover_index = None
                self.redraw()

    def _on_leave(self, _event):
        if self.hover_index is not None or self.pressed_index is not None:
            self.hover_index = None
            self.pressed_index = None
            self.redraw()

    def _on_press(self, event):
        index = self.get_cell_at(event.x, event.y)

        if index is None:
            return

        if not self.app.can_human_move():
            return

        if self.app.engine.board[index] != "":
            self.app.show_notice(
                "Cell already occupied",
                "Choose any empty tile to continue.",
                self.app.colors["draw"],
            )
            return

        self.pressed_index = index
        self.selected_index = index
        self.redraw()

    def _on_release(self, event):
        index = self.get_cell_at(event.x, event.y)
        pressed = self.pressed_index

        self.pressed_index = None
        self.redraw()

        if index is not None and pressed == index:
            self.app.human_move(index)

    def select_keyboard_cell(self, index):
        if not self.app.can_human_move():
            return

        if self.app.engine.board[index] != "":
            self.app.show_notice(
                "Cell already occupied",
                "Select an empty board position.",
                self.app.colors["draw"],
            )
            return

        self.selected_index = index
        self.hover_index = None
        self.redraw()

        self.app.show_notice(
            f"Cell {index + 1} selected",
            "Press Enter or Space to place your mark.",
            self.app.colors["accent"],
        )

    def play_selected_cell(self):
        if self.selected_index is None:
            return

        index = self.selected_index

        if self.app.engine.board[index] == "":
            self.app.human_move(index)

    def animate_move(self, index, done_callback):
        self.animation_token += 1
        token = self.animation_token

        self.animating_index = index
        self.animation_progress = 0.0

        start_time = time.perf_counter()
        duration = 0.18

        def animation_frame():
            if token != self.animation_token:
                return

            elapsed = time.perf_counter() - start_time
            progress = min(1.0, elapsed / duration)

            # Ease-out animation.
            self.animation_progress = 1 - (1 - progress) ** 3
            self.redraw()

            if progress < 1.0:
                self.animation_job = self.after(16, animation_frame)
            else:
                self.animating_index = None
                self.animation_progress = 1.0
                self.animation_job = None
                self.redraw()
                done_callback()

        animation_frame()

    def start_win_pulse(self):
        self.animation_token += 1
        token = self.animation_token

        self.win_pulse_on = False

        def pulse(step=0):
            if token != self.animation_token:
                return

            if not self.app.engine.game_over:
                return

            self.win_pulse_on = not self.win_pulse_on
            self.redraw()

            if step < 6:
                self.after(180, lambda: pulse(step + 1))
            else:
                self.win_pulse_on = False
                self.redraw()

        self.after(100, pulse)


# =============================================================================
# Main Application
# =============================================================================


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        self.theme_manager = ThemeManager()
        self.engine = GameEngine()
        self.score_manager = ScoreManager()
        self.ai = TicTacToeAI()

        self.button_widgets = []
        self.frame_registry = []
        self.label_registry = []
        self.canvas_registry = []

        self.style = ttk.Style(self)

        # Game configuration variables
        self.mode_var = tk.StringVar(value=MODE_HUMAN)
        self.human_side_var = tk.StringVar(value="X")
        self.human_ai_difficulty_var = tk.StringVar(value="Hard")

        self.x_ai_difficulty_var = tk.StringVar(value="Hard")
        self.o_ai_difficulty_var = tk.StringVar(value="Medium")
        self.ai_speed_var = tk.StringVar(value="Normal")

        # Match state
        self.round_number = 1
        self.starting_player = "X"

        self.busy = False
        self.ai_thinking = False
        self.ai_running = False
        self.ai_paused = False

        self.round_token = 0
        self.ai_after_job = None
        self.notice_token = 0

        self.setup_visible = True

        self.build_menu()
        self.build_ui()
        self.apply_theme("Dark")

        self.start_round(
            starter="X",
            increment_round=False,
        )

        self.bind_all("<Key>", self.on_key_press, add="+")

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def colors(self):
        return self.theme_manager.colors

    # -------------------------------------------------------------------------
    # Theme helpers
    # -------------------------------------------------------------------------

    def create_frame(self, parent, background_role, border_role=None, **kwargs):
        frame = tk.Frame(parent, **kwargs)
        frame.configure(bg=self.colors[background_role])

        if border_role:
            frame.configure(
                highlightthickness=1,
                highlightbackground=self.colors[border_role],
            )

        self.frame_registry.append((frame, background_role, border_role))

        return frame

    def create_label(
        self,
        parent,
        text,
        background_role="surface",
        foreground_role="text",
        **kwargs,
    ):
        label = tk.Label(parent, text=text, **kwargs)

        label.configure(
            bg=self.colors[background_role],
            fg=self.colors[foreground_role],
        )

        self.label_registry.append((label, background_role, foreground_role))

        return label

    def register_canvas(self, canvas, background_role):
        self.canvas_registry.append((canvas, background_role))

    def get_button_colors(
        self,
        variant,
        hovered=False,
        pressed=False,
        active=False,
        enabled=True,
    ):
        c = self.colors

        if not enabled:
            return c["disabled"], c["muted"]

        if variant == "primary":
            background = c["primary_hover"] if hovered or pressed else c["primary"]
            foreground = "#FFFFFF"

        elif variant == "danger":
            background = c["danger_hover"] if hovered or pressed else c["danger"]
            foreground = "#FFFFFF"

        elif variant == "nav":
            background = c["nav_hover"] if hovered or pressed or active else c["nav"]
            foreground = c["text"]

        elif variant == "toggle":
            if active:
                background = c["primary"]
                foreground = "#FFFFFF"
            else:
                background = (
                    c["secondary_hover"] if hovered or pressed else c["secondary"]
                )
                foreground = c["text"]

        else:
            background = c["secondary_hover"] if hovered or pressed else c["secondary"]
            foreground = c["text"]

        return background, foreground

    # -------------------------------------------------------------------------
    # Menu
    # -------------------------------------------------------------------------

    def build_menu(self):
        self.menubar = tk.Menu(self, tearoff=0)
        self.menu_list = []

        # Game menu
        game_menu = tk.Menu(self.menubar, tearoff=0)
        game_menu.add_command(label="New Round", command=self.new_round)
        game_menu.add_command(label="Restart Round", command=self.restart_round)
        game_menu.add_command(label="New Match", command=self.new_match)
        game_menu.add_separator()
        game_menu.add_command(label="Reset Score", command=self.reset_scores_confirm)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.destroy)

        self.menubar.add_cascade(label="Game", menu=game_menu)
        self.menu_list.append(game_menu)

        # Mode menu
        mode_menu = tk.Menu(self.menubar, tearoff=0)

        mode_menu.add_command(
            label="Human vs Human",
            command=lambda: self.set_mode_from_menu(MODE_HUMAN),
        )

        mode_menu.add_command(
            label="Human vs AI",
            command=lambda: self.set_mode_from_menu(MODE_AI),
        )

        mode_menu.add_command(
            label="AI vs AI",
            command=lambda: self.set_mode_from_menu(MODE_AI_AI),
        )

        self.menubar.add_cascade(label="Mode", menu=mode_menu)
        self.menu_list.append(mode_menu)

        # Theme menu
        theme_menu = tk.Menu(self.menubar, tearoff=0)

        theme_menu.add_command(
            label="Dark Theme",
            command=lambda: self.apply_theme("Dark"),
        )

        theme_menu.add_command(
            label="Light Theme",
            command=lambda: self.apply_theme("Light"),
        )

        self.menubar.add_cascade(label="Theme", menu=theme_menu)
        self.menu_list.append(theme_menu)

        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)

        help_menu.add_command(
            label="How to Play",
            command=self.show_how_to_play,
        )

        help_menu.add_command(
            label="About",
            command=self.show_about,
        )

        self.menubar.add_cascade(label="Help", menu=help_menu)
        self.menu_list.append(help_menu)

        self.config(menu=self.menubar)

    # -------------------------------------------------------------------------
    # Main UI
    # -------------------------------------------------------------------------

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ========================= Header =========================
        self.header = self.create_frame(
            self,
            "header",
            height=78,
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        self.header.grid_propagate(False)

        self.header_left = self.create_frame(
            self.header,
            "header",
        )
        self.header_left.pack(
            side="left",
            padx=(22, 14),
            pady=12,
        )

        self.logo_canvas = tk.Canvas(
            self.header_left,
            width=42,
            height=42,
            bd=0,
            highlightthickness=0,
        )
        self.logo_canvas.pack(side="left", padx=(0, 11))
        self.register_canvas(self.logo_canvas, "header")

        title_block = self.create_frame(
            self.header_left,
            "header",
        )
        title_block.pack(side="left")

        self.app_title_label = self.create_label(
            title_block,
            "ULTIMATE TIC TAC TOE",
            "header",
            "text",
            font=(FONT, 16, "bold"),
        )
        self.app_title_label.pack(anchor="w")

        self.app_subtitle_label = self.create_label(
            title_block,
            "PYTHON TKINTER EDITION",
            "header",
            "muted",
            font=(FONT, 7, "bold"),
        )
        self.app_subtitle_label.pack(anchor="w", pady=(1, 0))

        self.header_actions = self.create_frame(
            self.header,
            "header",
        )
        self.header_actions.pack(
            side="right",
            padx=18,
            pady=18,
        )

        self.setup_button = ThemedButton(
            self,
            self.header_actions,
            "GAME SETUP",
            self.toggle_setup_panel,
            variant="nav",
            font_size=8,
            padx=12,
            pady=7,
        )
        self.setup_button.pack(side="left", padx=4)

        self.dark_theme_button = ThemedButton(
            self,
            self.header_actions,
            "DARK",
            lambda: self.apply_theme("Dark"),
            variant="toggle",
            font_size=8,
            padx=11,
            pady=7,
        )
        self.dark_theme_button.pack(side="left", padx=3)

        self.light_theme_button = ThemedButton(
            self,
            self.header_actions,
            "LIGHT",
            lambda: self.apply_theme("Light"),
            variant="toggle",
            font_size=8,
            padx=11,
            pady=7,
        )
        self.light_theme_button.pack(side="left", padx=3)

        self.help_button = ThemedButton(
            self,
            self.header_actions,
            "HELP",
            self.show_how_to_play,
            variant="nav",
            font_size=8,
            padx=11,
            pady=7,
        )
        self.help_button.pack(side="left", padx=4)

        self.quit_button = ThemedButton(
            self,
            self.header_actions,
            "QUIT",
            self.destroy,
            variant="danger",
            font_size=8,
            padx=11,
            pady=7,
        )
        self.quit_button.pack(side="left", padx=(4, 0))

        self.header_divider = tk.Frame(self, height=1)
        self.header_divider.grid(
            row=0,
            column=0,
            sticky="sew",
        )
        self.frame_registry.append((self.header_divider, "border", None))

        # ========================= Body =========================
        self.body = self.create_frame(self, "bg")
        self.body.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, minsize=300)
        self.body.grid_columnconfigure(1, weight=1, minsize=450)
        self.body.grid_columnconfigure(2, minsize=280)

        self.build_configuration_panel()
        self.build_game_center()
        self.build_statistics_panel()

    # -------------------------------------------------------------------------
    # Configuration Panel
    # -------------------------------------------------------------------------

    def build_configuration_panel(self):
        self.config_panel = self.create_frame(
            self.body,
            "surface",
            "border",
            width=300,
        )
        self.config_panel.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(18, 8),
            pady=18,
        )
        self.config_panel.grid_propagate(False)

        self.config_title = self.create_label(
            self.config_panel,
            "GAME CONFIGURATION",
            "surface",
            "text",
            font=(FONT, 11, "bold"),
        )
        self.config_title.pack(
            anchor="w",
            padx=18,
            pady=(18, 2),
        )

        self.config_subtitle = self.create_label(
            self.config_panel,
            "Choose a mode and game settings.",
            "surface",
            "muted",
            font=(FONT, 8),
        )
        self.config_subtitle.pack(
            anchor="w",
            padx=18,
            pady=(0, 15),
        )

        self.mode_combo = self.create_combo_group(
            self.config_panel,
            "GAME MODE",
            self.mode_var,
            (MODE_HUMAN, MODE_AI, MODE_AI_AI),
            self.on_mode_changed,
        )

        self.make_separator(self.config_panel)

        # Human vs AI dynamic controls
        self.human_ai_frame = self.create_frame(
            self.config_panel,
            "surface",
        )

        self.human_side_combo = self.create_combo_group(
            self.human_ai_frame,
            "YOUR SIDE",
            self.human_side_var,
            ("X", "O"),
            self.on_human_side_changed,
        )

        self.human_difficulty_combo = self.create_combo_group(
            self.human_ai_frame,
            "AI DIFFICULTY",
            self.human_ai_difficulty_var,
            DIFFICULTIES,
            self.on_ai_setting_changed,
        )

        # AI vs AI dynamic controls
        self.ai_ai_frame = self.create_frame(
            self.config_panel,
            "surface",
        )

        self.x_ai_combo = self.create_combo_group(
            self.ai_ai_frame,
            "X AI DIFFICULTY",
            self.x_ai_difficulty_var,
            DIFFICULTIES,
            self.on_ai_setting_changed,
        )

        self.o_ai_combo = self.create_combo_group(
            self.ai_ai_frame,
            "O AI DIFFICULTY",
            self.o_ai_difficulty_var,
            DIFFICULTIES,
            self.on_ai_setting_changed,
        )

        self.speed_combo = self.create_combo_group(
            self.ai_ai_frame,
            "AI MOVE SPEED",
            self.ai_speed_var,
            tuple(AI_SPEEDS.keys()),
            self.on_ai_setting_changed,
        )

        self.ai_control_label = self.create_label(
            self.ai_ai_frame,
            "AI MATCH CONTROLS",
            "surface",
            "muted",
            font=(FONT, 8, "bold"),
        )
        self.ai_control_label.pack(
            anchor="w",
            pady=(15, 7),
        )

        self.ai_control_row = self.create_frame(
            self.ai_ai_frame,
            "surface",
        )
        self.ai_control_row.pack(fill="x")

        self.ai_start_button = ThemedButton(
            self,
            self.ai_control_row,
            "START",
            self.start_ai_match,
            variant="primary",
            font_size=8,
            padx=11,
            pady=8,
        )
        self.ai_start_button.pack(side="left", padx=(0, 5))

        self.ai_pause_button = ThemedButton(
            self,
            self.ai_control_row,
            "PAUSE",
            self.pause_ai_match,
            variant="secondary",
            font_size=8,
            padx=10,
            pady=8,
        )
        self.ai_pause_button.pack(side="left", padx=5)

        self.ai_resume_button = ThemedButton(
            self,
            self.ai_control_row,
            "RESUME",
            self.resume_ai_match,
            variant="secondary",
            font_size=8,
            padx=10,
            pady=8,
        )
        self.ai_resume_button.pack(side="left", padx=(5, 0))

        self.config_tip = self.create_label(
            self.config_panel,
            "",
            "surface",
            "muted",
            font=(FONT, 8),
            justify="left",
            wraplength=250,
        )
        self.config_tip.pack(
            side="bottom",
            anchor="w",
            fill="x",
            padx=18,
            pady=(12, 18),
        )

    def create_combo_group(
        self,
        parent,
        label_text,
        variable,
        values,
        callback,
    ):
        group = self.create_frame(parent, "surface")
        group.pack(fill="x", padx=18, pady=(0, 12))

        label = self.create_label(
            group,
            label_text,
            "surface",
            "muted",
            font=(FONT, 8, "bold"),
        )
        label.pack(anchor="w", pady=(0, 5))

        combo = ttk.Combobox(
            group,
            textvariable=variable,
            values=values,
            state="readonly",
            style="Ultimate.TCombobox",
            font=(FONT, 9),
            justify="left",
        )
        combo.pack(fill="x", ipady=4)

        combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: callback(),
        )

        return combo

    def make_separator(self, parent):
        separator = tk.Frame(parent, height=1)
        separator.pack(fill="x", padx=18, pady=(2, 14))
        self.frame_registry.append((separator, "border_soft", None))

    # -------------------------------------------------------------------------
    # Center Game Area
    # -------------------------------------------------------------------------

    def build_game_center(self):
        self.center_panel = self.create_frame(
            self.body,
            "bg",
        )
        self.center_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8,
            pady=18,
        )

        self.round_header = self.create_frame(
            self.center_panel,
            "bg",
        )
        self.round_header.pack(fill="x", pady=(0, 7))

        self.round_title = self.create_label(
            self.round_header,
            "CURRENT ROUND",
            "bg",
            "muted",
            font=(FONT, 8, "bold"),
        )
        self.round_title.pack(side="left")

        self.round_value = self.create_label(
            self.round_header,
            "ROUND 1",
            "bg",
            "accent",
            font=(FONT, 9, "bold"),
        )
        self.round_value.pack(side="right")

        self.board_hint = self.create_label(
            self.center_panel,
            "Click a cell, or use keys 1–9 and press Enter.",
            "bg",
            "muted",
            font=(FONT, 8),
        )
        self.board_hint.pack(pady=(0, 4))

        self.board_canvas = BoardCanvas(self, self.center_panel)

        self.board_canvas.pack(
            fill="both",
            expand=False,
            padx=4,
            pady=(0, 6),
        )

        # Reserve space for the status card and buttons below
        self.board_canvas.configure(height=300)

        self.register_canvas(self.board_canvas, "bg")

        # Status card
        self.status_card = self.create_frame(
            self.center_panel,
            "surface",
            "border",
            height=78,
        )

        self.status_card.pack(
            fill="x",
            padx=22,
            pady=(0, 12),
        )

        self.status_card.pack_propagate(False)

        self.status_title = self.create_label(
            self.status_card,
            "",
            "surface",
            "text",
            font=(DISPLAY_FONT, 16, "bold"),
        )

        self.status_title.pack(pady=(11, 0))

        self.status_subtitle = self.create_label(
            self.status_card,
            "",
            "surface",
            "muted",
            font=(FONT, 8),
        )

        self.status_subtitle.pack()
        
        # Status card
        self.status_card = self.create_frame(
            self.center_panel,
            "surface",
            "border",
            height=62,
        )
        self.status_card.pack(
            fill="x",
            padx=22,
            pady=(0, 8),
)

        self.status_card.pack_propagate(False)
        
        self.status_card.pack(fill="x", padx=22, pady=(0, 12))
        self.status_card.pack_propagate(False)

        self.status_title = self.create_label(
            self.status_card,
            "",
            "surface",
            "text",
            font=(DISPLAY_FONT, 16, "bold"),
        )
        self.status_title.pack(pady=(7, 0))

        self.status_subtitle = self.create_label(
            self.status_card,
            "",
            "surface",
            "muted",
            font=(FONT, 8),
        )
        self.status_subtitle.pack()

        # Action buttons
        self.action_row = self.create_frame(
            self.center_panel,
            "bg",
        )
        self.action_row.pack(pady=(0, 5))

        self.restart_button = ThemedButton(
            self,
            self.action_row,
            "RESTART ROUND",
            self.restart_round,
            variant="secondary",
            font_size=9,
            padx=16,
            pady=10,
        )
        self.restart_button.pack(side="left", padx=5)

        self.new_round_button = ThemedButton(
            self,
            self.action_row,
            "NEW ROUND",
            self.new_round,
            variant="primary",
            font_size=9,
            padx=18,
            pady=10,
        )
        self.new_round_button.pack(side="left", padx=5)

        self.undo_button = ThemedButton(
            self,
            self.action_row,
            "UNDO",
            self.undo_move,
            variant="secondary",
            font_size=9,
            padx=16,
            pady=10,
        )
        self.undo_button.pack(side="left", padx=5)

        self.reset_score_button = ThemedButton(
            self,
            self.action_row,
            "RESET SCORE",
            self.reset_scores_confirm,
            variant="danger",
            font_size=9,
            padx=16,
            pady=10,
        )
        self.reset_score_button.pack(side="left", padx=5)

    # -------------------------------------------------------------------------
    # Statistics / Scoreboard Panel
    # -------------------------------------------------------------------------

    def build_statistics_panel(self):
        self.stats_panel = self.create_frame(
            self.body,
            "surface",
            "border",
            width=280,
        )
        self.stats_panel.grid(
            row=0,
            column=2,
            sticky="ns",
            padx=(8, 18),
            pady=18,
        )
        self.stats_panel.grid_propagate(False)

        self.stats_title = self.create_label(
            self.stats_panel,
            "MATCH SCORE",
            "surface",
            "text",
            font=(FONT, 11, "bold"),
        )
        self.stats_title.pack(
            anchor="w",
            padx=18,
            pady=(18, 1),
        )

        self.stats_subtitle = self.create_label(
            self.stats_panel,
            "Scores remain while restarting rounds.",
            "surface",
            "muted",
            font=(FONT, 8),
        )
        self.stats_subtitle.pack(
            anchor="w",
            padx=18,
            pady=(0, 12),
        )

        self.score_canvas = tk.Canvas(
            self.stats_panel,
            width=250,
            height=125,
            bd=0,
            highlightthickness=0,
        )
        self.score_canvas.pack(
            fill="x",
            padx=14,
        )
        self.score_canvas.bind(
            "<Configure>",
            lambda _event: self.draw_scoreboard(),
        )
        self.register_canvas(self.score_canvas, "surface")

        self.stats_separator = tk.Frame(self.stats_panel, height=1)
        self.stats_separator.pack(
            fill="x",
            padx=18,
            pady=14,
        )
        self.frame_registry.append((self.stats_separator, "border_soft", None))

        self.match_details_title = self.create_label(
            self.stats_panel,
            "MATCH DETAILS",
            "surface",
            "text",
            font=(FONT, 10, "bold"),
        )
        self.match_details_title.pack(
            anchor="w",
            padx=18,
            pady=(0, 6),
        )

        self.details_canvas = tk.Canvas(
            self.stats_panel,
            width=250,
            height=285,
            bd=0,
            highlightthickness=0,
        )
        self.details_canvas.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14),
        )
        self.details_canvas.bind(
            "<Configure>",
            lambda _event: self.draw_match_details(),
        )
        self.register_canvas(self.details_canvas, "surface")

    # -------------------------------------------------------------------------
    # Theme application
    # -------------------------------------------------------------------------

    def apply_theme(self, theme_name):
        self.theme_manager.set_theme(theme_name)
        c = self.colors

        self.configure(bg=c["bg"])

        # ttk style
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Ultimate.TCombobox",
            fieldbackground=c["input"],
            background=c["input"],
            foreground=c["text"],
            bordercolor=c["border"],
            lightcolor=c["border"],
            darkcolor=c["border"],
            arrowcolor=c["text"],
            selectbackground=c["primary"],
            selectforeground="#FFFFFF",
        )

        self.style.map(
            "Ultimate.TCombobox",
            fieldbackground=[
                ("readonly", c["input"]),
            ],
            foreground=[
                ("readonly", c["text"]),
            ],
            selectbackground=[
                ("readonly", c["primary"]),
            ],
        )

        # Style menu widgets
        self.menubar.configure(
            bg=c["header"],
            fg=c["text"],
            activebackground=c["nav_hover"],
            activeforeground=c["text"],
            borderwidth=0,
        )

        for menu in self.menu_list:
            menu.configure(
                bg=c["surface"],
                fg=c["text"],
                activebackground=c["primary"],
                activeforeground="#FFFFFF",
                borderwidth=0,
            )

        # Frames
        for widget, background_role, border_role in self.frame_registry:
            if widget.winfo_exists():
                widget.configure(bg=c[background_role])

                if border_role:
                    widget.configure(highlightbackground=c[border_role])

        # Labels
        for widget, background_role, foreground_role in self.label_registry:
            if widget.winfo_exists():
                widget.configure(
                    bg=c[background_role],
                    fg=c[foreground_role],
                )

        # Canvases
        for canvas, background_role in self.canvas_registry:
            if canvas.winfo_exists():
                canvas.configure(bg=c[background_role])

        # Header theme buttons
        self.dark_theme_button.set_active(theme_name == "Dark")
        self.light_theme_button.set_active(theme_name == "Light")

        self.setup_button.set_active(self.setup_visible)

        # All hover buttons
        for button in self.button_widgets:
            button.apply_theme()

        self.draw_logo()
        self.update_dynamic_controls()
        self.refresh_ui()

    def draw_logo(self):
        c = self.colors
        canvas = self.logo_canvas

        canvas.delete("all")

        canvas_round_rect(
            canvas,
            2,
            2,
            40,
            40,
            11,
            fill=c["primary"],
            outline=c["accent"],
            width=1,
        )

        canvas.create_line(
            11,
            11,
            22,
            22,
            fill="#FFFFFF",
            width=3,
            capstyle="round",
        )

        canvas.create_line(
            22,
            11,
            11,
            22,
            fill="#FFFFFF",
            width=3,
            capstyle="round",
        )

        canvas.create_oval(
            23,
            22,
            34,
            33,
            outline=c["o"],
            width=3,
        )

    # -------------------------------------------------------------------------
    # Configuration callbacks
    # -------------------------------------------------------------------------

    def set_mode_from_menu(self, mode):
        self.mode_var.set(mode)
        self.on_mode_changed()

    def on_mode_changed(self):
        self.cancel_ai_turn()
        self.ai_running = False
        self.ai_paused = False

        self.starting_player = "X"
        self.update_dynamic_controls()

        self.start_round(
            starter="X",
            increment_round=True,
        )

    def on_human_side_changed(self):
        if self.mode_var.get() != MODE_AI:
            return

        self.cancel_ai_turn()
        self.starting_player = "X"

        self.start_round(
            starter="X",
            increment_round=True,
        )

    def on_ai_setting_changed(self):
        self.refresh_ui()

    def update_dynamic_controls(self):
        self.human_ai_frame.pack_forget()
        self.ai_ai_frame.pack_forget()

        mode = self.mode_var.get()

        if mode == MODE_AI:
            self.human_ai_frame.pack(
                fill="x",
                before=self.config_tip,
                pady=(0, 2),
            )

            self.config_tip.config(
                text=(
                    "Choose X or O. The AI will automatically "
                    "play its move after a short delay."
                )
            )

        elif mode == MODE_AI_AI:
            self.ai_ai_frame.pack(
                fill="x",
                before=self.config_tip,
                pady=(0, 2),
            )

            self.config_tip.config(
                text=(
                    "Choose difficulty and speed for both AIs. "
                    "Use Start, Pause, and Resume controls."
                )
            )

        else:
            self.config_tip.config(
                text=("Two players share the board and take turns placing X and O.")
            )

        self.update_ai_control_buttons()

    def toggle_setup_panel(self):
        self.setup_visible = not self.setup_visible

        if self.setup_visible:
            self.config_panel.grid()
        else:
            self.config_panel.grid_remove()

        self.setup_button.set_active(self.setup_visible)
        self.setup_button.set_text("HIDE SETUP" if self.setup_visible else "GAME SETUP")

        self.after(30, self.board_canvas.redraw)

    # -------------------------------------------------------------------------
    # Scoreboard / status updates
    # -------------------------------------------------------------------------

    def refresh_ui(self):
        self.update_round_header()
        self.update_status_panel()
        self.update_ai_control_buttons()
        self.draw_scoreboard()
        self.draw_match_details()
        self.board_canvas.redraw()

    def update_round_header(self):
        self.round_value.config(text=f"ROUND {self.round_number}")

    def update_status_panel(self):
        c = self.colors
        engine = self.engine
        mode = self.mode_var.get()

        if self.busy:
            title = "MOVE CONFIRMED"
            subtitle = "Updating the board..."
            color = c["accent"]

        elif engine.game_over:
            if engine.winner == "Draw":
                title = "IT'S A DRAW!"
                subtitle = "Every cell is filled. A balanced round."
                color = c["draw"]

            else:
                if engine.winner == "X":
                    title = "🎉 PLAYER A WINS!"
                    subtitle = "Amazing game! 🏆"
                    color = c["x"]
                else:
                    title = "🎉 PLAYER B WINS!"
                    subtitle = "Amazing game! 🏆"
                    color = c["o"]

        elif mode == MODE_AI_AI and self.ai_paused:
            title = "AI MATCH PAUSED"
            subtitle = (
                f"Next move belongs to {engine.current_player} AI. "
                "Press Resume to continue."
            )
            color = c["draw"]

        elif self.ai_thinking:
            if mode == MODE_AI_AI:
                difficulty = self.get_ai_difficulty(engine.current_player)

                title = f"{engine.current_player} AI IS THINKING..."
                subtitle = f"Difficulty: {difficulty}"
                color = c["accent"]

            else:
                title = "AI IS THINKING..."
                subtitle = "The computer is choosing its best move."
                color = c["accent"]

        elif mode == MODE_AI_AI:
            title = "AI MATCH READY"
            subtitle = "Press Start to begin the AI vs AI match."
            color = c["accent"]

        elif mode == MODE_AI:
            if engine.current_player == self.human_side_var.get():
                title = f"YOUR TURN — {engine.current_player}"
                subtitle = "Choose any available board cell."
                color = c["x"] if engine.current_player == "X" else c["o"]
            else:
                title = "AI IS READY"
                subtitle = "The AI will make its move shortly."
                color = c["accent"]

        else:
            title = f"{engine.current_player}'S TURN"
            subtitle = "Player X and Player O take turns placing marks on the board."
            color = c["x"] if engine.current_player == "X" else c["o"]

        self.status_card.config(
            highlightbackground=color,
        )

        self.status_title.config(
            text=title,
            fg=color,
        )

        self.status_subtitle.config(
            text=subtitle,
            fg=c["muted"],
        )

    def show_notice(self, title, subtitle, color):
        self.notice_token += 1
        token = self.notice_token

        self.status_card.config(highlightbackground=color)
        self.status_title.config(text=title, fg=color)
        self.status_subtitle.config(
            text=subtitle,
            fg=self.colors["muted"],
        )

        def clear_notice():
            if token == self.notice_token:
                self.update_status_panel()

        self.after(1500, clear_notice)

    def draw_scoreboard(self):
        canvas = self.score_canvas
        c = self.colors

        if not canvas.winfo_exists():
            return

        canvas.delete("all")

        width = max(250, canvas.winfo_width())
        height = max(120, canvas.winfo_height())

        padding = 4
        gap = 7
        card_width = (width - padding * 2 - gap * 2) / 3

        score_items = [
            ("X", self.score_manager.x_wins, c["x"]),
            ("DRAWS", self.score_manager.draws, c["draw"]),
            ("O", self.score_manager.o_wins, c["o"]),
        ]

        for index, (label, value, color) in enumerate(score_items):
            x1 = padding + index * (card_width + gap)
            y1 = 4
            x2 = x1 + card_width
            y2 = height - 5

            canvas_round_rect(
                canvas,
                x1,
                y1 + 3,
                x2,
                y2 + 3,
                11,
                fill=c["tile_shadow"],
                outline="",
            )

            canvas_round_rect(
                canvas,
                x1,
                y1,
                x2,
                y2,
                11,
                fill=c["surface_2"],
                outline=c["border_soft"],
                width=1,
            )

            canvas.create_text(
                (x1 + x2) / 2,
                y1 + 24,
                text=label,
                font=(FONT, 8, "bold"),
                fill=c["muted"],
            )

            canvas.create_text(
                (x1 + x2) / 2,
                y1 + 61,
                text=str(value),
                font=(FONT, 23, "bold"),
                fill=color,
            )

            if label == "DRAWS":
                canvas.create_text(
                    (x1 + x2) / 2,
                    y1 + 89,
                    text="MATCHES",
                    font=(FONT, 6, "bold"),
                    fill=c["muted"],
                )

    def draw_match_details(self):
        canvas = self.details_canvas
        c = self.colors

        if not canvas.winfo_exists():
            return

        canvas.delete("all")

        width = max(250, canvas.winfo_width())

        if self.engine.game_over:
            current_player = "Round complete"
        elif self.ai_thinking:
            current_player = f"{self.engine.current_player} AI thinking"
        else:
            current_player = self.engine.current_player

        mode = self.mode_var.get()

        if mode == MODE_AI:
            ai_info = (
                f"Human: {self.human_side_var.get()}  |  "
                f"AI: {self.human_ai_difficulty_var.get()}"
            )

        elif mode == MODE_AI_AI:
            ai_info = (
                f"X: {self.x_ai_difficulty_var.get()}  |  "
                f"O: {self.o_ai_difficulty_var.get()}"
            )

        else:
            ai_info = "Two human players"

        if self.score_manager.current_streak_symbol:
            streak = (
                f"{self.score_manager.current_streak_symbol} × "
                f"{self.score_manager.current_streak_count}"
            )
        else:
            streak = "No active streak"

        details = [
            ("Mode", mode),
            ("Round", str(self.round_number)),
            ("Total Games", str(self.score_manager.total_games)),
            ("Moves", str(len(self.engine.history))),
            ("Current Player", current_player),
            ("AI Setup", ai_info),
            ("Current Streak", streak),
            ("Best Streak", str(self.score_manager.best_streak)),
        ]

        y = 15

        for label, value in details:
            canvas.create_text(
                8,
                y,
                text=label.upper(),
                anchor="w",
                font=(FONT, 7, "bold"),
                fill=c["muted"],
            )

            canvas.create_text(
                width - 8,
                y,
                text=value,
                anchor="e",
                font=(FONT, 8, "bold"),
                fill=c["text"],
            )

            canvas.create_line(
                8,
                y + 13,
                width - 8,
                y + 13,
                fill=c["border_soft"],
                width=1,
            )

            y += 32

    # -------------------------------------------------------------------------
    # AI controls
    # -------------------------------------------------------------------------

    def update_ai_control_buttons(self):
        is_ai_ai = self.mode_var.get() == MODE_AI_AI
        round_active = not self.engine.game_over and not self.busy

        self.ai_start_button.set_enabled(
            is_ai_ai and round_active and not self.ai_running
        )

        self.ai_pause_button.set_enabled(
            is_ai_ai and round_active and self.ai_running and not self.ai_paused
        )

        self.ai_resume_button.set_enabled(
            is_ai_ai and round_active and self.ai_running and self.ai_paused
        )

    def start_ai_match(self):
        if self.mode_var.get() != MODE_AI_AI:
            return

        if self.engine.game_over:
            self.show_notice(
                "Round finished",
                "Start a new round before running the AIs again.",
                self.colors["draw"],
            )
            return

        if self.busy:
            return

        self.ai_running = True
        self.ai_paused = False

        self.schedule_next_automatic_turn()
        self.refresh_ui()

    def pause_ai_match(self):
        if self.mode_var.get() != MODE_AI_AI:
            return

        if self.busy:
            self.show_notice(
                "Please wait",
                "The current AI move is still being animated.",
                self.colors["draw"],
            )
            return

        if self.ai_running:
            self.ai_paused = True
            self.cancel_ai_turn()
            self.refresh_ui()

    def resume_ai_match(self):
        if self.mode_var.get() != MODE_AI_AI:
            return

        if self.engine.game_over:
            return

        if self.ai_running and self.ai_paused:
            self.ai_paused = False
            self.schedule_next_automatic_turn()
            self.refresh_ui()

    # -------------------------------------------------------------------------
    # Game controls
    # -------------------------------------------------------------------------

    def new_round(self):
        next_starter = GameEngine.other_player(self.starting_player)

        self.start_round(
            starter=next_starter,
            increment_round=True,
        )

    def restart_round(self):
        self.start_round(
            starter=self.starting_player,
            increment_round=False,
        )

    def new_match(self):
        confirmed = messagebox.askyesno(
            "New Match",
            (
                "Start a new match?\n\n"
                "This clears X wins, O wins, draws, and total games."
            ),
            parent=self,
        )

        if not confirmed:
            return

        self.score_manager.reset_scores()
        self.round_number = 1
        self.starting_player = "X"

        self.start_round(
            starter="X",
            increment_round=False,
        )

    def reset_scores_confirm(self):
        confirmed = messagebox.askyesno(
            "Reset Score",
            (
                "Reset the complete scoreboard?\n\n"
                "X wins, O wins, draws, total games, and streaks "
                "will be cleared."
            ),
            parent=self,
        )

        if not confirmed:
            return

        self.score_manager.reset_scores()
        self.refresh_ui()

        self.show_notice(
            "Scoreboard reset",
            "A new score history has started.",
            self.colors["accent"],
        )

    def start_round(self, starter="X", increment_round=False):
        self.cancel_ai_turn()
        self.board_canvas.cancel_animations()

        self.round_token += 1

        if increment_round:
            self.round_number += 1

        self.starting_player = starter

        self.busy = False
        self.ai_thinking = False
        self.ai_running = False
        self.ai_paused = False

        self.engine.reset_board(starter)

        self.board_canvas.hover_index = None
        self.board_canvas.pressed_index = None
        self.board_canvas.selected_index = None

        self.refresh_ui()

        # Human vs AI can automatically begin if AI starts first.
        if self.mode_var.get() == MODE_AI:
            self.schedule_next_automatic_turn()

    def undo_move(self):
        if self.busy:
            self.show_notice(
                "Please wait",
                "The current move animation is still running.",
                self.colors["draw"],
            )
            return

        if not self.engine.history:
            self.show_notice(
                "Nothing to undo",
                "No moves have been played in this round.",
                self.colors["draw"],
            )
            return

        self.cancel_ai_turn()
        self.board_canvas.cancel_animations()

        # If the match had finished, safely revert the recorded score.
        if self.engine.game_over and self.engine.winner:
            self.score_manager.revert_result(self.engine.winner)

        history = self.engine.history[:]

        # In Human vs AI mode undo both AI and human moves where possible.
        moves_to_remove = 1

        if self.mode_var.get() == MODE_AI and len(history) >= 2:
            moves_to_remove = 2

        for _ in range(moves_to_remove):
            if history:
                history.pop()

        self.engine.rebuild_from_history(history)

        self.busy = False
        self.ai_thinking = False
        self.ai_running = False
        self.ai_paused = False

        self.board_canvas.selected_index = None
        self.board_canvas.hover_index = None

        self.refresh_ui()

        if self.mode_var.get() == MODE_AI:
            self.schedule_next_automatic_turn()

    # -------------------------------------------------------------------------
    # Human and AI move handling
    # -------------------------------------------------------------------------

    def can_human_move(self):
        if self.engine.game_over:
            return False

        if self.busy or self.ai_thinking:
            return False

        mode = self.mode_var.get()

        if mode == MODE_AI_AI:
            return False

        if mode == MODE_AI:
            return self.engine.current_player == self.human_side_var.get()

        return True

    def human_move(self, index):
        if not self.can_human_move():
            self.show_notice(
                "Please wait",
                "It is not currently a human turn.",
                self.colors["draw"],
            )
            return

        self.attempt_move(index, from_ai=False)

    def attempt_move(self, index, from_ai=False):
        if self.busy:
            return

        if not from_ai and not self.can_human_move():
            return

        success, player, message = self.engine.make_move(index)

        if not success:
            self.show_notice(
                "Move unavailable",
                message,
                self.colors["draw"],
            )
            return

        self.busy = True
        self.ai_thinking = False

        self.board_canvas.selected_index = None
        self.board_canvas.hover_index = None

        token = self.round_token

        self.update_status_panel()
        self.draw_match_details()
        self.board_canvas.animate_move(
            index,
            lambda: self.after_move_animation(token),
        )

    def after_move_animation(self, token):
        if token != self.round_token:
            return

        self.busy = False

        if self.engine.game_over:
            self.complete_round()
        else:
            self.refresh_ui()
            self.schedule_next_automatic_turn()

    def complete_round(self):
        result = self.engine.winner

        self.ai_thinking = False

        if self.mode_var.get() == MODE_AI_AI:
            self.ai_running = False
            self.ai_paused = False

        self.score_manager.record_result(result)
        self.refresh_ui()

        if result in ("X", "O"):
            self.board_canvas.start_win_pulse()
            self.show_winner_popup(result)

        elif result == "Draw":
            self.show_winner_popup("Draw")

    def show_winner_popup(self, result):
        c = self.colors

        popup = tk.Toplevel(self)

        popup.overrideredirect(True)
        popup.transient(self)
        popup.configure(bg=c["bg"])

        width = 420
        height = 260
    
        self.update_idletasks()

        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + (self.winfo_height() - height) // 2

        popup.geometry(f"{width}x{height}+{x}+{y}")

        # ==========================================================
        # OUTER CARD
        # ==========================================================

        card = tk.Frame(
            popup,
            bg=c["surface"],
            highlightthickness=2,
            highlightbackground=c["win"],
        )

        card.pack(
            fill="both",
            expand=True,
            padx=3,
            pady=3,
        )

        # ==========================================================
        # WINNER CONTENT
        # ==========================================================

        if result == "X":
            winner = "PLAYER A"
            title = "WINS!"
            emoji = "🎉"
            color = c["x"]
            message = "What an amazing move! ⭐"

        elif result == "O":
            winner = "PLAYER B"
            title = "WINS!"
            emoji = "🎉"
            color = c["o"]
            message = "What an amazing move! ⭐"

        else:
            winner = "IT'S A"
            title = "DRAW!"
            emoji = "🤝"
            color = c["draw"]
            message = "That was a close one! ✨"

        # Top celebration
        tk.Label(
            card,
            text=emoji,
            font=("Segoe UI Emoji", 38),
            bg=c["surface"],
            fg=color,
        ).pack(pady=(18, 0))

        # Winner name
        tk.Label(
            card,
            text=winner,
            font=(DISPLAY_FONT, 20, "bold"),
            bg=c["surface"],
            fg=color,
        ).pack(pady=(2, 0))

        # WINS
        tk.Label(
            card,
            text=title,
            font=(DISPLAY_FONT, 17, "bold"),
            bg=c["surface"],
            fg=c["text"],
        ).pack()

        # Message
        tk.Label(
            card,
            text=message,
            font=(FONT, 10),
            bg=c["surface"],
            fg=c["muted"],
        ).pack(pady=(5, 12))

        # Continue button
        continue_btn = tk.Label(
            card,
            text="  ✨ CONTINUE  ",
            font=(FONT, 9, "bold"),
            bg=color,
            fg="#FFFFFF",
            padx=15,
            pady=7,
            cursor="hand2",
        )

        continue_btn.pack()

        continue_btn.bind(
            "<Button-1>",
            lambda event: popup.destroy()
        )
    
        # Hover effect
        def on_enter(event):
            continue_btn.config(
                bg=c["primary_hover"]
            )

        def on_leave(event):
            continue_btn.config(
                bg=color
            )

        continue_btn.bind("<Enter>", on_enter)
        continue_btn.bind("<Leave>", on_leave)

        # Automatically disappear
        popup.after(3500, popup.destroy)

    def schedule_next_automatic_turn(self):
        mode = self.mode_var.get()

        if self.engine.game_over or self.busy:
            return

        # Human vs AI
        if mode == MODE_AI:
            human_side = self.human_side_var.get()

            if self.engine.current_player != human_side:
                self.schedule_ai_turn(550)

        # AI vs AI
        elif mode == MODE_AI_AI:
            if self.ai_running and not self.ai_paused:
                speed = AI_SPEEDS.get(
                    self.ai_speed_var.get(),
                    AI_SPEEDS["Normal"],
                )
                self.schedule_ai_turn(speed)

    def schedule_ai_turn(self, delay):
        self.cancel_ai_turn()

        if self.engine.game_over:
            return

        token = self.round_token
        self.ai_thinking = True

        self.refresh_ui()

        def run_ai():
            self.ai_after_job = None

            if token != self.round_token:
                return

            if self.engine.game_over:
                return

            if self.mode_var.get() == MODE_AI_AI:
                if not self.ai_running or self.ai_paused:
                    return

            self.perform_ai_turn()

        self.ai_after_job = self.after(delay, run_ai)

    def cancel_ai_turn(self):
        self.round_token += 1

        if self.ai_after_job:
            try:
                self.after_cancel(self.ai_after_job)
            except Exception:
                pass

        self.ai_after_job = None
        self.ai_thinking = False

    def perform_ai_turn(self):
        if self.engine.game_over:
            self.ai_thinking = False
            return

        mode = self.mode_var.get()

        if mode == MODE_AI:
            if self.engine.current_player == self.human_side_var.get():
                self.ai_thinking = False
                return

        elif mode == MODE_AI_AI:
            if not self.ai_running or self.ai_paused:
                self.ai_thinking = False
                return

        else:
            self.ai_thinking = False
            return

        current_player = self.engine.current_player
        difficulty = self.get_ai_difficulty(current_player)

        move = self.ai.get_move(
            self.engine.board[:],
            current_player,
            difficulty,
        )

        self.ai_thinking = False

        if move is None or move not in self.engine.get_available_moves():
            self.show_notice(
                "AI move error",
                "The AI could not find a valid move.",
                self.colors["danger"],
            )
            return

        self.attempt_move(move, from_ai=True)

    def get_ai_difficulty(self, player):
        mode = self.mode_var.get()

        if mode == MODE_AI_AI:
            if player == "X":
                return self.x_ai_difficulty_var.get()

            return self.o_ai_difficulty_var.get()

        return self.human_ai_difficulty_var.get()

    # -------------------------------------------------------------------------
    # Keyboard controls
    # -------------------------------------------------------------------------

    def on_key_press(self, event):
        key = event.keysym.lower()

        # Avoid keyboard board actions while a dropdown is open.
        if isinstance(event.widget, ttk.Combobox):
            return

        if key == "r":
            self.restart_round()
            return

        if key == "t":
            if self.theme_manager.current_theme == "Dark":
                self.apply_theme("Light")
            else:
                self.apply_theme("Dark")
            return

        if key == "u":
            self.undo_move()
            return

        if key in ("return", "space"):
            self.board_canvas.play_selected_cell()
            return

        if key in "123456789":
            index = int(key) - 1
            self.board_canvas.select_keyboard_cell(index)

    # -------------------------------------------------------------------------
    # Dialogs
    # -------------------------------------------------------------------------

    def show_how_to_play(self):
        text = (
            "OBJECTIVE\n"
            "Place three matching marks in a row, column, or diagonal.\n\n"
            "GAME MODES\n"
            "• Human vs Human: Player X and Player O take turns.\n"
            "• Human vs AI: Choose whether you play as X or O.\n"
            "• AI vs AI: Select both AI difficulties and watch them play.\n\n"
            "AI DIFFICULTIES\n"
            "• Easy: Random valid moves.\n"
            "• Medium: Win, block, center, corners, then random.\n"
            "• Hard: Uses Minimax and plays optimally.\n\n"
            "KEYBOARD SHORTCUTS\n"
            "1–9: Select board cells.\n"
            "Enter / Space: Confirm selected cell.\n"
            "R: Restart current round.\n"
            "U: Undo.\n"
            "T: Toggle light/dark theme."
        )

        self.show_info_dialog(
            "How to Play",
            "Quick guide for Ultimate Tic Tac Toe",
            text,
        )

    def show_about(self):
        text = (
            "Ultimate Tic Tac Toe\n"
            "Python Tkinter Edition\n\n"
            "A polished desktop Tic Tac Toe game featuring:\n"
            "• Human vs Human\n"
            "• Human vs AI\n"
            "• AI vs AI\n"
            "• Easy, Medium, and Hard Minimax AI\n"
            "• Score tracking and match statistics\n"
            "• Dark and Light professional themes\n"
            "• Keyboard support and board animations\n\n"
            "Built with Python standard library and Tkinter only."
        )

        self.show_info_dialog(
            "About",
            "Modern desktop game made with Python + Tkinter",
            text,
        )

    def show_info_dialog(self, title, subtitle, body_text):
        c = self.colors

        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.configure(bg=c["bg"])
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        dialog_width = 560
        dialog_height = 470

        screen_x = (dialog.winfo_screenwidth() - dialog_width) // 2

        screen_y = (dialog.winfo_screenheight() - dialog_height) // 2

        dialog.geometry(f"{dialog_width}x{dialog_height}+{screen_x}+{screen_y}")

        outer = tk.Frame(
            dialog,
            bg=c["surface"],
            highlightthickness=1,
            highlightbackground=c["border"],
        )
        outer.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18,
        )

        tk.Label(
            outer,
            text=title.upper(),
            font=(DISPLAY_FONT, 20, "bold"),
            bg=c["surface"],
            fg=c["accent"],
        ).pack(pady=(24, 3))

        tk.Label(
            outer,
            text=subtitle,
            font=(FONT, 9),
            bg=c["surface"],
            fg=c["muted"],
        ).pack(pady=(0, 20))

        text_label = tk.Label(
            outer,
            text=body_text,
            font=(FONT, 10),
            bg=c["surface"],
            fg=c["text"],
            justify="left",
            anchor="nw",
            wraplength=480,
        )
        text_label.pack(
            fill="both",
            expand=True,
            padx=28,
        )

        close_label = tk.Label(
            outer,
            text="CLOSE",
            font=(FONT, 9, "bold"),
            bg=c["primary"],
            fg="#FFFFFF",
            padx=22,
            pady=9,
            cursor="hand2",
        )
        close_label.pack(pady=(18, 24))

        close_label.bind(
            "<Button-1>",
            lambda _event: dialog.destroy(),
        )

        close_label.bind(
            "<Enter>",
            lambda _event: close_label.config(bg=c["primary_hover"]),
        )

        close_label.bind(
            "<Leave>",
            lambda _event: close_label.config(bg=c["primary"]),
        )

        dialog.bind(
            "<Escape>",
            lambda _event: dialog.destroy(),
        )

    # -------------------------------------------------------------------------
    # Shutdown
    # -------------------------------------------------------------------------

    def destroy(self):
        try:
            self.cancel_ai_turn()
            self.board_canvas.cancel_animations()
        except Exception:
            pass

        super().destroy()


# =============================================================================
# Run Application
# =============================================================================

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
