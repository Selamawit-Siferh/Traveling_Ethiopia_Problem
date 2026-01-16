import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# BFS traversal for the graph
def bfs_all(cities, roads, start_city):
    visited = set()
    queue = deque([(start_city, [start_city], 0)])
    total_cost = 0

    while queue:
        current_city, path, current_cost = queue.popleft()

        if current_city not in visited:
            visited.add(current_city)
            total_cost += current_cost

            # Visit each neighboring city
            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], distance))

        if len(visited) == len(cities):
            break

    return path, total_cost


# DFS traversal for the graph
def dfs_all(cities, roads, start_city):
    visited = set()
    stack = [(start_city, [start_city], 0)]
    total_cost = 0

    while stack:
        current_city, path, current_cost = stack.pop()

        if current_city not in visited:
            visited.add(current_city)
            total_cost += current_cost

            # Explore all connected cities
            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], distance))

        if len(visited) == len(cities):
            break

    return path, total_cost


# Function to visualize the graph
def visualize_graph(cities, roads):
    G = nx.Graph()
    for city in cities:
        G.add_node(city)

    for city, neighbors in roads.items():
        for neighbor, _ in neighbors:
            G.add_edge(city, neighbor)

    # Draw the graph
    pos = nx.spring_layout(G)  # Layout for positioning nodes
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10)
    plt.show()


# Main function to traverse the cities with BFS or DFS
def traverse_all_cities(cities, roads, start_city, strategy):
    if strategy == 'bfs':
        return bfs_all(cities, roads, start_city)

    elif strategy == 'dfs':
        return dfs_all(cities, roads, start_city)

    else:
        raise ValueError("Invalid strategy. Choose 'bfs' or 'dfs'.")


# Example usage
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510)],
    'Bahir Dar': [('Gondar', 180)],
    'Gondar': [('Mekelle', 300)],
    'Mekelle': []
}

start_city = 'Addis Ababa'

# BFS traversal
bfs_path, bfs_cost = traverse_all_cities(cities, roads, start_city, strategy='bfs')
print(f"BFS Path: {bfs_path} with cost {bfs_cost}")

# DFS traversal
dfs_path, dfs_cost = traverse_all_cities(cities, roads, start_city, strategy='dfs')
print(f"DFS Path: {dfs_path} with cost {dfs_cost}")

# Visualize the graph
visualize_graph(cities, roads)
