import random
import os
import time
# Constants
ROWS, COLS = 9, 18
WALL = "#"
FOOD = "."
EMPTY = " "
PACMAN = "P"
GHOSTS = ["G","g"]
visited = [ [ False for x in range(COLS)] for x in range(ROWS) ]
visited[0][0]=True
# Initialize the game grid
def initialize_grid():
    grid = [[FOOD for _ in range(COLS)] for _ in range(ROWS)]
    grid[0][0] = PACMAN  # Pac-Man's starting position
    # Place ghosts randomly
    for j in range (4,14):
        grid[4][j]=WALL
    for j in range(3, 6):
        grid[j][4] = WALL
        grid[j][13] = WALL
    r=0
    for ghost in GHOSTS:
        grid[3+r][9] = ghost
        r+=2
    return grid

# Print the game grid
def print_grid(grid):
    for row in grid:
        print(" ".join(row))
    print("\n")

# Evaluate the utility of Pac-Man's move
from collections import deque

def calculate_distance_to_food(grid, start_r, start_c):
    # Directions: up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Function to check if a cell is within the grid and not a wall
    def is_valid(r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != WALL

    # Initialize a queue for BFS and add the starting position
    queue = deque([(start_r, start_c, 0)])  # (row, col, distance)

    # Set to keep track of visited cells
    visited1 = set([(start_r, start_c)])

    while queue:
        r, c, dist = queue.popleft()

        # Return the distance if food is found
        if grid[r][c] == FOOD:
            return dist

        # Explore all possible directions
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc

            if is_valid(new_r, new_c) and (new_r, new_c) not in visited1:
                visited1.add((new_r, new_c))
                queue.append((new_r, new_c, dist + 1))

    # Return a large number if no food is found
    return float('inf')


def calculate_distance_to_ghosts(grid, start_r, start_c,g):
    # Directions: up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Function to check if a cell is within the grid and not a wall
    def is_valid(r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] != WALL

    # Initialize a queue for BFS and add the starting position
    queue = deque([(start_r, start_c, 0)])  # (row, col, distance)

    # Set to keep track of visited cells
    visited1 = set([(start_r, start_c)])

    while queue:
        r, c, dist = queue.popleft()

        # Return the distance if a ghost is found
        if grid[r][c]==g:
            return dist

        # Explore all possible directions
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc

            if is_valid(new_r, new_c) and (new_r, new_c) not in visited1:
                visited1.add((new_r, new_c))
                queue.append((new_r, new_c, dist + 1))

    # Return a large number if no ghost is found
    return float('inf')


def utility(grid, r, c):
    ghost_penalty = 0
    score=0
    if grid[r][c]==FOOD:
        score+=9
    elif grid[r][c]==EMPTY:
        score-=50
    elif grid[r][c] in GHOSTS:
        score-=1000
    food_distance = calculate_distance_to_food(grid, r, c)
    food_bonus =max(30 - food_distance,0) # Decrease bonus with distance

    for ghost in GHOSTS:
        distance= calculate_distance_to_ghosts(grid, r,c,ghost)
        if 0 < distance <= 4:
            ghost_penalty -= 800 / distance
        # print(distance,"ghost")

    return food_bonus + ghost_penalty+score


# # Minimax algorithm for Pac-Man's move
def minimax_move(grid, r, c, depth=0,turn=0):
    visited2= [row[:] for row in visited]

    if depth == 1 :
        return utility(grid, r, c)
    if turn==0:  # Pac-Man's turn
        best_score = -float("inf")
        new_score=0
        for new_r, new_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
                temp_grid = [row[:] for row in grid]
                tmp_food=temp_grid[new_r][new_c]
                temp_grid[new_r][new_c] = PACMAN
                temp_grid[r][c]=EMPTY
                visited2[new_r][new_c]=True
                if tmp_food==FOOD:
                    new_score+=100


                score = minimax_move(temp_grid, new_r, new_c, depth,1)
                score+=new_score

                visited2[new_r][new_c]=False
                # print(visited2)
                temp_grid[new_r][new_c]=tmp_food
                temp_grid[r][c]=PACMAN


                if score > best_score:
                    best_score = score
                    best_move = (new_r, new_c)
        return best_move if depth==0 else best_score
    elif turn==1:  # Ghosts' turn
        worst_score = float("inf")
        try:
            gr, gc = [(i, row.index("G")) for i, row in enumerate(grid) if "G" in row][0]
            for new_r, new_c in [(gr + 1, gc), (gr - 1, gc), (gr, gc + 1), (gr, gc - 1)]:
                if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
                    temp_grid = [row[:] for row in grid]
                    tmp_food = temp_grid[new_r][new_c]
                    temp_grid[new_r][new_c] = "G"
                    if visited2[gr][gc]==False:
                        temp_grid[gr][gc]=FOOD
                    else:
                        temp_grid[gr][gc] = EMPTY

                    score = minimax_move(temp_grid, r, c, depth, 2)
                    temp_grid[gr][gc] = "G"
                    temp_grid[new_r][new_c] = tmp_food
                    worst_score = min(worst_score, score)
        except:
            score = minimax_move(grid, r, c, depth ,2)
            worst_score = min(worst_score, score)

        return worst_score
    elif turn==2:  # Ghosts' turn
        worst_score = float("inf")
        try:
            gr, gc = [(i, row.index("g")) for i, row in enumerate(grid) if "g" in row][0]
            for new_r, new_c in [(gr + 1, gc), (gr - 1, gc), (gr, gc + 1), (gr, gc - 1)]:
                if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
                    temp_grid = [row[:] for row in grid]
                    tmp_food = temp_grid[new_r][new_c]
                    temp_grid[new_r][new_c] = "g"
                    if visited2[gr][gc]==False:
                        temp_grid[gr][gc]=FOOD
                    else:
                        temp_grid[gr][gc] = EMPTY
                    score = minimax_move(temp_grid, r, c, depth+1, 0)
                    temp_grid[gr][gc] = "g"
                  
                    temp_grid[new_r][new_c] = tmp_food
                    worst_score = min(worst_score, score)
        except:
            score = minimax_move(grid, r, c, depth+1 ,0)
            worst_score = min(worst_score, score)

        return worst_score



# Move ghosts randomly
def move_ghost(grid, ghost):
    r, c = [(i, row.index(ghost)) for i, row in enumerate(grid) if ghost in row][0]
    moves = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    random.shuffle(moves)
    for new_r, new_c in moves:
        if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL :
            if (grid[new_r][new_c]!="g" and grid[new_r][new_c]!="G"):
                if visited[r][c]==True:
                    grid[r][c] = EMPTY
                else:
                    grid[r][c] = FOOD
                grid[new_r][new_c] = ghost
                break
    return

# Main game loop
def play_game():
    grid = initialize_grid()
    pacman_row, pacman_col = 0, 0
    score = 0
    turn=0
    while True:

        if turn%3==0:
            new_row, new_col = minimax_move(grid, pacman_row, pacman_col,0)
            # Update Pac-Man's position and score
            if (new_row, new_col) != (pacman_row, pacman_col):
                if grid[new_row][new_col]=="G" or grid[new_row][new_col]=="g":
                    print(f"Game Over! You lost! Score: {score}")
                    break
                else:
                    if grid[new_row][new_col]==FOOD:
                        score += 9
                    else:
                        score-=1
                    grid[pacman_row][pacman_col] = EMPTY
                    pacman_row, pacman_col = new_row, new_col
                    grid[new_row][new_col] = PACMAN
                    # print(new_row,new_col)
                    # print(visited)

                    visited[new_row][new_col]=True
                    # print(visited)


            turn+=1
            print(score)
            print_grid(grid)


        # Move ghosts
        if turn%3==1:
            move_ghost(grid,"G")

            turn+=1
            # print_grid(grid)

        if turn%3==2:
            move_ghost(grid,"g")

            turn+=1
            # print_grid(grid)

        time.sleep(0.01)
        os.system("cls")


        # Check if Pac-Man encounters a ghost
        if grid[pacman_row][pacman_col] in GHOSTS:
            print(f"Game Over! You lost! Score: {score}")
            break

        # Check if all dots are eaten
        if not any(FOOD in row for row in grid):
            print(f"You win! Score: {score}")
            break

play_game()




# Minimax algorithm for Pac-Man's move with alpha-beta pruning
# def minimax_move(grid, r, c, depth=0, turn=0, alpha=float('-inf'), beta=float('inf')):
#     visited2 = [row[:] for row in visited]
    
#     if depth == 2:
#         return utility(grid, r, c)
    
#     if turn == 0:  # Pac-Man's turn
#         best_score = -float("inf")
#         new_score = 0
        
#         for new_r, new_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
#             if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
#                 temp_grid = [row[:] for row in grid]
#                 tmp_food = temp_grid[new_r][new_c]
#                 temp_grid[r][c]=EMPTY
#                 temp_grid[new_r][new_c] = PACMAN
#                 visited2[new_r][new_c] = True
                
#                 if tmp_food == FOOD:
#                     new_score += 60

#                 score = minimax_move(temp_grid, new_r, new_c, depth, 1, alpha, beta)
#                 score += new_score

#                 visited2[new_r][new_c] = False
#                 temp_grid[new_r][new_c] = tmp_food
#                 temp_grid[r][c] = PACMAN

#                 if score > best_score:
#                     best_score = score
#                     best_move = (new_r, new_c)
                
#                 alpha = max(alpha, best_score)
#                 if alpha >= beta:
#                     break
        
#         return best_move if depth == 0 else best_score
    
#     elif turn == 1:  # Ghosts' turn
#         worst_score = float("inf")
        
#         try:
#             gr, gc = [(i, row.index("G")) for i, row in enumerate(grid) if "G" in row][0]
            
#             for new_r, new_c in [(gr + 1, gc), (gr - 1, gc), (gr, gc + 1), (gr, gc - 1)]:
#                 if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
#                     temp_grid = [row[:] for row in grid]
#                     tmp_food = temp_grid[new_r][new_c]
#                     temp_grid[new_r][new_c] = "G"
                    
#                     if visited2[gr][gc] == False:
#                         temp_grid[gr][gc] = FOOD
#                     else:
#                         temp_grid[gr][gc] = EMPTY

#                     score = minimax_move(temp_grid, r, c, depth, 2, alpha, beta)
                    
#                     temp_grid[gr][gc] = "G"
#                     temp_grid[new_r][new_c] = tmp_food
#                     worst_score = min(worst_score, score)
                    
#                     beta = min(beta, worst_score)
#                     if beta <= alpha:
#                         break
                    
#         except:
#             score = minimax_move(grid, r, c, depth, 2, alpha, beta)
#             worst_score = min(worst_score, score)

#         return worst_score
    
#     elif turn == 2:  # Ghosts' turn
#         worst_score = float("inf")
        
#         try:
#             gr, gc = [(i, row.index("g")) for i, row in enumerate(grid) if "g" in row][0]
            
#             for new_r, new_c in [(gr + 1, gc), (gr - 1, gc), (gr, gc + 1), (gr, gc - 1)]:
#                 if 0 <= new_r < ROWS and 0 <= new_c < COLS and grid[new_r][new_c] != WALL:
#                     temp_grid = [row[:] for row in grid]
#                     tmp_food = temp_grid[new_r][new_c]
#                     temp_grid[new_r][new_c] = "g"
                    
#                     if visited2[gr][gc] == False:
#                         temp_grid[gr][gc] = FOOD
#                     else:
#                         temp_grid[gr][gc] = EMPTY

#                     score = minimax_move(temp_grid, r, c, depth + 1, 0, alpha, beta)
                    
#                     temp_grid[gr][gc] = "g"
#                     temp_grid[new_r][new_c] = tmp_food
#                     worst_score = min(worst_score, score)
                    
#                     beta = min(beta, worst_score)
#                     if beta <= alpha:
#                         break
                    
#         except:
#             score = minimax_move(grid, r, c, depth + 1, 0, alpha, beta)
#             worst_score = min(worst_score, score)

#         return worst_score
