# Read the graph from a file and construct it
graph = {}  # Dictionary to store the graph
num_colors = 0  # Number of colors available

# Read the graph from the file
with open('gc_1.txt') as file:
    for line in file:
        line = line.strip()  # Remove leading and trailing whitespace
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue
        if line.startswith('colors'):
            num_colors = int(line.split('=')[1].strip())  # Extract the number of colors
        else:
            # Extract vertices from the line
            v1, v2 = map(int, line.split(','))
            # Add vertices to the graph
            graph.setdefault(v1, set()).add(v2)
            graph.setdefault(v2, set()).add(v1)

# Initialize the queue for pending constraints
constraint_queue = [(v1, v2) for v1 in graph for v2 in graph[v1]]

# Initialize the initial state where no node is colored yet
initial_state = {}

# Function to check if the current state is valid
def is_valid_state(state):
    for node in state:
        for neighbor in graph[node]:
            if neighbor in state and state[neighbor] == state[node]:
                return False
    return True

# Function to perform constraint propagation using AC3 algorithm
def ac3_algorithm(queue, domains):
    while queue:
        v1, v2 = queue.pop(0)
        if remove_inconsistent_values(v1, v2, domains):
            if not domains[v1]:
                return False
            for neighbor in graph[v1]:
                if neighbor != v2:
                    queue.append((neighbor, v1))
    return True

# Function to remove inconsistent values
def remove_inconsistent_values(v1, v2, domains):
    removed = False
    for value in domains[v1]:
        if not any(value != d for d in domains[v2]):
            domains[v1].remove(value)
            removed = True
    return removed

# Function to search the solution space
def search_solution(state, domains, heuristic):
    if len(state) == len(graph):
        return state
    node = min(set(graph.keys()) - set(state), key=lambda n: heuristic(n, state, domains))
    for color in domains[node]:
        new_state = state.copy()
        new_domains = domains.copy()
        new_state[node] = color
        new_domains[node] = [color]
        if is_valid_state(new_state) and ac3_algorithm(constraint_queue[:], new_domains):
            result = search_solution(new_state, new_domains, heuristic)
            if result is not None:
                return result
    return None

# Initialize the color domains
color_domains = {node: list(range(num_colors)) for node in graph}

# Heuristic 1: Minimum Remaining Values
def min_remaining_values(node, state, domains):
    return len(domains[node])

# Heuristic 2: Minimum Constraint Values
def min_constraint_values(node, state, domains):
    count = 0
    for neighbor in graph[node]:
        if neighbor in state and state[neighbor] in domains[node]:
            count += 1
    return count

# Heuristic 3: Combined Heuristic
def combined_heuristic(node, state, domains):
    return min_remaining_values(node, state, domains) * min_constraint_values(node, state, domains)

# Choose the heuristic function
chosen_heuristic = combined_heuristic

# Start searching the solution space
solution_result = search_solution(initial_state, color_domains, chosen_heuristic)

# Print the solution if found
if solution_result is not None:
    print("Solution found:")
    for node, color in solution_result.items():
        print(f"Node {node} is colored with {color}")
else:
    print("No solution found")
