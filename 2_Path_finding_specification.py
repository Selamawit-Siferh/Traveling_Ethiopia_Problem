import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

# Define cities and roads
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

# Function to implement BFS and DFS
def uninformed_path_finder(cities, roads, start_city, goal_city, strategy, visit_all=False):
    if strategy not in ['bfs', 'dfs']:
        raise ValueError("Strategy must be 'bfs' or 'dfs'")

    visited = set()
    path = []
    cost = 0

    if strategy == 'bfs':
        # If it's a weighted graph, use a priority queue (min-heap) to handle cumulative costs
        queue = [(0, start_city, [start_city])]  # (cost, current_city, path)
        while queue:
            current_cost, current_city, current_path = heapq.heappop(queue)
            if current_city in visited:
                continue
            visited.add(current_city)

            if current_city == goal_city:
                return current_path, current_cost

            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (current_cost + distance, neighbor, current_path + [neighbor]))

    elif strategy == 'dfs':
        stack = [(start_city, [start_city], 0)]
        while stack:
            current_city, current_path, current_cost = stack.pop()
            if current_city in visited:
                continue
            visited.add(current_city)

            if current_city == goal_city:
                return current_path, current_cost

            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in visited:
                    stack.append((neighbor, current_path + [neighbor], current_cost + distance))

    if visit_all:
        # Implementing a solution to visit all cities exactly once (simple backtracking)
        def visit_all_cities(current_city, current_path, visited):
            if len(current_path) == len(cities):
                return current_path, sum(roads[current_path[i]][1] for i in range(len(current_path)-1))
            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result = visit_all_cities(neighbor, current_path + [neighbor], visited)
                    if result:
                        return result
                    visited.remove(neighbor)
            return None

        visited = set([start_city])
        return visit_all_cities(start_city, [start_city], visited)

    return None, None


# Input cities for the task
start_city = input("Insert the Initial City: ")
goal_city = input("Insert the Goal City: ")
strategy = input("Choose a strategy ('bfs' or 'dfs'): ").lower()
visit_all = input("Visit all cities exactly once? (yes/no): ").lower() == 'yes'

# Get path and cost
path, cost = uninformed_path_finder(cities, roads, start_city, goal_city, strategy, visit_all)
if path:
    print(f"Path found using {strategy.upper()}: {path} with cost {cost}")
else:
    print("No path found.")

# Visualize the graph
G = nx.Graph()
for city, connections in roads.items():
    for neighbor, distance in connections:
        G.add_edge(city, neighbor, weight=distance)

pos = nx.spring_layout(G)
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=500, font_size=12)

# Add edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# Highlight the path
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

plt.title("Ethiopian Cities Road Network", fontsize=14)
plt.show()
