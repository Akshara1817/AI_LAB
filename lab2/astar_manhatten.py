def astar(start, goal):
    # Convert inputs to immutable tuples so they can be stored in sets/dicts
    start_tuple = tuple(tuple(row) for row in start)
    goal_tuple = tuple(tuple(row) for row in goal)
    
    frontier = [(start_tuple, 0)]
    explored = set()
    
    def find(matrix, target):
        for row_idx, row in enumerate(matrix):
            if target in row:
                col_idx = row.index(target)
                return (row_idx, col_idx)
        return None

    def md(curr, goal, tile):
        pos1 = find(curr, tile)
        pos2 = find(goal, tile)
        if not pos1 or not pos2:
            return 0
        return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

    def pq(frontier_list):
        f = {}
        for state, level in frontier_list:
            g = level
            h = 0
            # Flatten the state matrix to get individual tile values
            for row in state:
                for tile in row:
                    if tile != -1:  # Skip the empty space for Manhattan Distance
                        h += md(state, goal_tuple, tile)
            f[state] = g + h
            
        states_keys = list(f.keys())
        min_state = states_keys[0]
        min_f = f[min_state]
        
        for state in f:
            if f[state] < min_f:
                min_f = f[state]
                min_state = state
                
        for state, level in frontier_list:
            if state == min_state:
                return min_state, level

    def expand(node, action):
        matrix = [list(row) for row in node]
        i, j = -1, -1
        for r in range(len(matrix)):
            if -1 in matrix[r]:
                i, j = r, matrix[r].index(-1)
                break
                
        # Perform directional swaps in place
        if action == 0 and i > 0:
            matrix[i][j], matrix[i-1][j] = matrix[i-1][j], matrix[i][j]
        elif action == 1 and i < len(matrix) - 1:
            matrix[i][j], matrix[i+1][j] = matrix[i+1][j], matrix[i][j]
        elif action == 2 and j > 0:
            matrix[i][j], matrix[i][j-1] = matrix[i][j-1], matrix[i][j]
        elif action == 3 and j < len(matrix) - 1:
            matrix[i][j], matrix[i][j+1] = matrix[i][j+1], matrix[i][j]
            
        return tuple(tuple(row) for row in matrix)

    while frontier:
        current_state, current_level = pq(frontier)
        if current_state == goal_tuple:
            print(f"Goal reached at level {current_level}!")
            return current_state
            
        frontier = [item for item in frontier if item[0] != current_state]
        explored.add(current_state)
        
        for action in range(4):
            neighbor = expand(current_state, action)
            if neighbor != current_state and neighbor not in explored:
                in_frontier = False
                for idx, (f_state, f_level) in enumerate(frontier):
                    if f_state == neighbor:
                        in_frontier = True
                        if current_level + 1 < f_level:
                            frontier[idx] = (neighbor, current_level + 1)
                        break
                if not in_frontier:
                    frontier.append((neighbor, current_level + 1))
                    
    print("No solution found.")
    return None

# "-1" represents the blank/empty space


# The target configuration (Fixed string types to integers)
start_board = [
    [2, 8, 3],
    [1, 6, 4],
    [-1, 7, 5]
]

# The target configuration
goal_board = [
    [1, 2, 3],
    [8, -1, 4],
    [7, 6, 5]
]
# Run the algorithm
result = astar(start_board, goal_board)

# Print the resulting configuration matrix neatly
if result:
    print("\nFinal State Matrix:")
    for row in result:
        print(row)
