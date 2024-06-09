# Pac-Man Game with Minimax and Alpha-Beta Pruning

This Python script implements a simple Pac-Man game using the Minimax algorithm with alpha-beta pruning. Pac-Man navigates a grid, trying to collect food while avoiding ghosts. The game features basic grid initialization, utility evaluation, and Minimax decision-making to move Pac-Man and ghosts.

## Getting Started

### Prerequisites

- Python 3.x

### Running the Script

1. Clone the repository:
    ```bash
    git clone https://github.com/maryamjbr/Pacman.git
    cd Pacman
    ```

2. Run the script:
    ```bash
    python packman.py
    ```

## How It Works

### Game Grid

The game grid is a 9x18 matrix where:
- `#` represents walls
- `.` represents food
- ` ` represents empty spaces
- `P` represents Pac-Man
- `G` and `g` represent ghosts

### Initialization

- The game grid is initialized with walls, food, Pac-Man's starting position, and ghosts.
- Walls are placed in predefined positions to create a maze-like structure.
- Ghosts are placed at specific positions on the grid.

### Utility Evaluation

- The utility of a move is calculated based on the distance to the nearest food, the presence of food, empty spaces, and the proximity of ghosts.
- The utility function aims to maximize the score for Pac-Man by moving towards food and away from ghosts.

### Minimax Algorithm

- The `minimax_move` function implements the Minimax algorithm with alpha-beta pruning to decide Pac-Man's next move.
- The algorithm recursively evaluates potential moves for Pac-Man and ghosts, trying to maximize Pac-Man's score while minimizing the ghosts' effectiveness.
- Pac-Man and ghosts take turns to move, with Pac-Man trying to maximize the score and ghosts trying to minimize it.

### Ghost Movement

- Ghosts move randomly within the grid, avoiding walls and each other.
- Ghosts' positions are updated in each turn, and they can potentially end the game if they collide with Pac-Man.

### Main Game Loop

- The game loop continuously updates the grid, moves Pac-Man using the Minimax algorithm, and moves the ghosts.
- The game checks for collisions between Pac-Man and ghosts, game completion (all food eaten), and prints the grid state and score.

## Example Game Grid

The game starts with the following grid setup:

```
P . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . .
. . . . # . . . . G . . . # . . . .
. . . . # # # # # # # # # # . . . .
. . . . # . . . g . . . . # . . . .
. . . . # . . . . . . . . # . . . .
. . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . .
```

## Output

The script prints the game grid, updates it after each move, and displays the current score. The game ends when Pac-Man collides with a ghost or all food is collected.


