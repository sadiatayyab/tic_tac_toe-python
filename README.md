#  Ultimate Tic Tac Toe — Python Tkinter Edition

A modern and interactive **Ultimate Tic Tac Toe desktop application** developed using **Python and Tkinter** as part of my **Python Internship at Skillify**.

The project focuses on building a professional desktop GUI while implementing game logic, AI decision-making, user interaction, themes, animations, and game statistics.

---

## Project Overview

This application provides a complete Tic Tac Toe gaming experience with multiple game modes and difficulty levels.

Players can compete against another human, challenge an AI opponent, or watch two AI players compete against each other.

The application uses **Tkinter** for the graphical user interface and Python for the underlying game engine and AI logic.

---

## Features

### Game Modes

* **Human vs Human**
* **Human vs AI**
* **AI vs AI**
* Start, Pause, and Resume AI matches

### AI Difficulty Levels

The application provides three AI difficulty levels:

*  **Easy** — Random valid moves
*  **Medium** — Uses strategic decisions such as:
  * Winning moves
  * Blocking opponent moves
  * Center preference
  * Corner preference
*  **Hard** — Uses the **Minimax algorithm with Alpha-Beta pruning**

###  User Interface

* Modern desktop interface
* Dark Theme
* Light Theme
* Responsive game board
* Hover effects
* Pressed button effects
* Winning tile animations
* Animated X and O marks
* Professional menu bar
* Status and notification messages

###  Game Statistics

The application keeps track of:

* X wins
* O wins
* Draws
* Total games
* Current winning streak
* Best winning streak

###  Keyboard Support

Players can interact with the board using the keyboard.

* Number keys **1–9** select board positions
* **Enter / Space** can be used to place a mark

###  Game Controls

* New Round
* Restart Round
* New Match
* Undo
* Reset Score
* Start AI
* Pause AI
* Resume AI
* Quit

###  Additional Features

* How to Play dialog
* About dialog
* Game configuration panel
* Custom themed buttons
* Responsive Canvas-based board
* Winning combination highlighting

---

##  Technologies Used

| Technology                      | Purpose                          |
| ------------------------------- | -------------------------------- |
| **Python**                      | Core programming language        |
| **Tkinter**                     | Desktop GUI development          |
| **ttk**                         | Styled GUI components            |
| **Canvas**                      | Custom game board and animations |
| **Minimax Algorithm**           | Hard-level AI                    |
| **Alpha-Beta Pruning**          | Optimizing Minimax               |
| **Object-Oriented Programming** | Application architecture         |

The project uses Python's built-in GUI capabilities and does not require external GUI frameworks.

---

##  Project Architecture

The application is organized into separate logical components:

### `ThemeManager`

Handles:

* Dark theme
* Light theme
* Application colors
* Theme switching

### `GameEngine`

Responsible for:

* Board management
* Player turns
* Move validation
* Winner detection
* Draw detection
* Move history
* Undo functionality

### `ScoreManager`

Responsible for:

* Player scores
* Draw statistics
* Total games
* Winning streaks
* Best streak tracking

### `TicTacToeAI`

Contains the AI logic:

* Easy AI
* Medium AI
* Hard AI
* Minimax
* Alpha-Beta pruning

### `BoardCanvas`

Responsible for:

* Drawing the game board
* Rendering X and O
* Hover effects
* Click handling
* Keyboard selection
* Move animations
* Winning animations

### `MainApplication`

Controls:

* Main application window
* Menus
* Game configuration
* GUI layout
* Themes
* Game controls
* Communication between game components

---

##  Project Structure

```text
TicTacToe/
│
├── main.py
└── README.md
    
```

> The main application is contained in `main.py`.

---

##  Requirements

Before running the application, make sure you have:

* Python 3.x
* Tkinter

Tkinter is normally included with standard Python installations on Windows.

You can verify Python installation using:

```bash
python --version
```

---

##  How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/sadiatayyab/tic_tac_toe-python.git
```

### 2. Open the Project Folder

```bash
cd TicTacToe
```

### 3. Run the Application

```bash
python main.py
```

The Ultimate Tic Tac Toe application will launch in a desktop window.

---

##  How to Play

### Human vs Human

1. Select **Human vs Human**.
2. Player X starts the game.
3. Players take turns selecting empty cells.
4. The first player to complete a winning combination wins.

### Human vs AI

1. Select **Human vs AI**.
2. Choose your side: **X or O**.
3. Select the AI difficulty.
4. Make your move.
5. The AI automatically responds.

### AI vs AI

1. Select **AI vs AI**.
2. Choose the difficulty for X.
3. Choose the difficulty for O.
4. Select the AI speed.
5. Click **START**.
6. Use **PAUSE** or **RESUME** whenever needed.

---

##  AI Implementation

The project implements three different AI approaches.

### Easy AI

The Easy AI selects a random available cell.

### Medium AI

The Medium AI follows a simple strategic priority:

```text
1. Try to win
2. Block the opponent
3. Choose the center
4. Choose a corner
5. Choose any available cell
```

### Hard AI

The Hard AI uses the **Minimax algorithm with Alpha-Beta pruning** to evaluate possible moves and select the best move.

The implementation also uses move ordering and caching to improve decision-making performance.

---

##  Themes

The application includes two built-in themes:

###  Dark Theme

Designed for a modern gaming-style interface with dark backgrounds and contrasting text.

###  Light Theme

Provides a bright interface with lighter surfaces and backgrounds.

Users can switch between themes from the application menu or header controls.

---

##  Statistics

The scoreboard tracks:

```text
X Wins
O Wins
Draws
Total Games
Current Streak
Best Streak
```

This allows players to track their performance across multiple rounds.

---

##  Skills Demonstrated

This project helped me strengthen my understanding of:

* Python programming
* Object-Oriented Programming
* Tkinter GUI development
* Event-driven programming
* Canvas-based graphics
* Game development concepts
* Artificial Intelligence fundamentals
* Minimax algorithm
* Alpha-Beta pruning
* Data structures
* State management
* Keyboard and mouse events
* GUI animations
* Responsive UI design
* Debugging and problem solving

---

##  Internship Project

**Internship:** Python Internship
**Organization:** Skillify
**Project:** Ultimate Tic Tac Toe — Python Tkinter Edition

This project was developed as part of my Python internship to gain practical experience in Python programming, GUI development, application design, and problem-solving.

---

##  Future Improvements

Possible future improvements include:

* Online multiplayer mode
* Player profiles
* Persistent statistics
* Sound effects
* Background music
* More AI difficulty levels
* Custom board sizes
* Game history
* Save and load functionality
* Executable `.exe` distribution
* Improved accessibility features

---



##  Author

**Sadia Tayyab**

Python Intern at **Skillify**

---

##  Acknowledgement

I would like to thank **Skillify** for providing the internship opportunity and allowing me to improve my practical Python development skills through hands-on projects.

---

##  License

This project was created for educational and internship purposes.
