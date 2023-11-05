from queue import PriorityQueue

class Node:
    def __init__(self, x, y, value):
        self.x, self.y, self.value = x, y, value
        self.explored, self.cost, self.astar_cost = False, 0, 0
        self.label = None  # Labeled number

    def __lt__(self, other):
        # Compare nodes based on f(n) with tie-breaking on labeled number
        if self.astar_cost == other.astar_cost:
            return self.label < other.label
        return self.astar_cost < other.astar_cost

    def manhattan(self, goal):
        x_distance = abs(self.x - goal.x)
        y_distance = abs(self.y - goal.y)
    
        # Moving southward has a cost of 1
        southward_distance = max(0, goal.y - self.y)
        # The remaining y_distance would be northward movement
        northward_distance = y_distance - southward_distance
    
        return 2 * x_distance + 1 * southward_distance + 3 * northward_distance





class Maze:
    def __init__(self, maze_array):
        self.matrix = [
            [Node(x, y, cell) for x, cell in enumerate(row)]
            for y, row in enumerate(maze_array)
        ]
        self.width, self.height = len(maze_array[0]), len(maze_array)
        self.explored_nodes = {}  # Store explored nodes in a dictionary

    def bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def print_maze(self):
        for row in self.matrix:
            print(" ".join(node.value for node in row))


def search_init(maze, entrance_node, exit_node):
    frontier = PriorityQueue()
    entrance_node = maze.matrix[entrance_node.y][entrance_node.x]
    entrance_node.explored, entrance_node.value, entrance_node.cost = True, "00", 0
    entrance_node.astar_cost = entrance_node.manhattan(exit_node)
    entrance_node.label = 0  # Initialize labeled number for entrance node
    frontier.put((entrance_node.astar_cost, entrance_node.label, entrance_node))

    if not maze.bounds(exit_node):
        print("Exit node coordinates are out of bounds.")
        return maze

    return astar_search(frontier, maze, entrance_node, exit_node, 1)


def astar_search(frontier, maze, start_node, exit_node, order):
    while not frontier.empty() and not maze.matrix[exit_node.y][exit_node.x].explored:
        _, _, current_node = frontier.get()
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        
        for dx, dy in moves:
            next_x, next_y = current_node.x + dx, current_node.y + dy
            if (
                maze.bounds(Node(next_x, next_y, None))
                and not maze.matrix[next_y][next_x].explored
                and maze.matrix[next_y][next_x].value != "##"
            ):
                next_node = maze.matrix[next_y][next_x]
                next_node.value, next_node.explored = f"{order:02d}", True
                
                # Correctly assign movement_cost based on the direction of the movement
                movement_cost = 1 if dy == 1 else 3 if dy == -1 else 2  # South: 1, North: 3, East/West: 2
                
                next_node.cost = current_node.cost + movement_cost
                next_node.astar_cost = next_node.cost + next_node.manhattan(exit_node)
                next_node.label = order
                frontier.put((next_node.astar_cost, next_node.label, next_node))
                order += 1
                
                # Store information about explored nodes in the dictionary
                maze.explored_nodes[next_node] = {
                    "label": next_node.value,
                    "g(n)": next_node.cost,
                    "h(n)": next_node.manhattan(exit_node),
                    "f(n)": next_node.astar_cost,
                }
    return maze



PATH, WALL = "[]", "##"
maze_array = [
    [WALL, WALL, WALL, PATH, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [WALL, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, PATH, PATH, WALL],
    [WALL, PATH, WALL, WALL, PATH, WALL, PATH, WALL, WALL, WALL, PATH, WALL],
    [WALL, PATH, WALL, PATH, PATH, WALL, PATH, PATH, PATH, WALL, PATH, PATH],
    [WALL, PATH, WALL, WALL, WALL, WALL, WALL, WALL, PATH, WALL, WALL, WALL],
    [WALL, PATH, PATH, WALL, PATH, PATH, PATH, WALL, PATH, PATH, PATH, WALL],
    [WALL, WALL, PATH, WALL, PATH, WALL, WALL, WALL, PATH, WALL, PATH, WALL],
    [WALL, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, WALL, PATH, WALL],
    [WALL, PATH, WALL, WALL, WALL, WALL, PATH, WALL, PATH, WALL, WALL, WALL],
    [WALL, PATH, PATH, PATH, PATH, PATH, PATH, WALL, PATH, PATH, PATH, WALL],
    [WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
]

def main():
    maze = Maze(maze_array)
    entrance_node = Node(3, 0, PATH)
    exit_node = Node(11, 3, PATH)

    print("A* Search")
    result = search_init(maze, entrance_node, exit_node)
    entrance_node.value, exit_node.value = PATH, PATH  # Reset the values for entrance and exit nodes
    result.print_maze()

    # Print information about explored nodes with coordinates
    for node, info in maze.explored_nodes.items():
        print(f"Node {info['label']:>02} (x:{node.x:>2}, y:{node.y:>2}) - g(n): {info['g(n)']:>2}, h(n): {info['h(n)']:>2}, f(n): {info['f(n)']:>2}")



if __name__ == "__main__":
    main()
