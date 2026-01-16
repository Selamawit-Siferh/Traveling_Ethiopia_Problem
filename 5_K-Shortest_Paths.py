import heapq
import networkx as nx
import matplotlib.pyplot as plt


def find_shortest_path(cities, roads, start_city, goal_city):
    """
    Find the shortest path between two cities using Dijkstra's algorithm.
    """
    pq = [(0, start_city, [])]  # Priority queue: (cost, city, path)
    visited = set()

    while pq:
        current_cost, current_city, path = heapq.heappop(pq)

        # If the goal city is reached, return the path and its cost
        if current_city == goal_city:
            return path + [current_city], current_cost

        # Skip if the city has already been visited
        if current_city in visited:
            continue

        visited.add(current_city)

        # Check neighboring cities
        for neighbor, distance in roads.get(current_city, []):
            if neighbor not in visited:
                heapq.heappush(pq, (current_cost + distance, neighbor, path + [current_city]))

    return [], float('inf')


def yen_k_shortest_paths(cities, roads, start_city, goal_city, k):
    """
    Find the k-shortest paths between two cities using Yen's algorithm.
    """
    first_path, first_cost = find_shortest_path(cities, roads, start_city, goal_city)
    if not first_path:
        return [], []

    k_shortest_paths = [(first_path, first_cost)]
    potential_paths = []

    # Find alternative paths by blocking edges from the first path
    for _ in range(1, k):
        for j in range(len(first_path) - 1):
            blocked_roads = roads.copy()
            u, v = first_path[j], first_path[j + 1]

            # Block the road between cities u and v
            blocked_roads[u] = [(neigh, dist) for neigh, dist in blocked_roads[u] if neigh != v]

            # Find new path with blocked road
            path, cost = find_shortest_path(cities, blocked_roads, start_city, goal_city)
            if path:
                potential_paths.append((path, cost))

        # Sort the potential paths by cost and select the best one
        if potential_paths:
            potential_paths.sort(key=lambda x: x[1])
            next_path, next_cost = potential_paths.pop(0)
            k_shortest_paths.append((next_path, next_cost))
            potential_paths.clear()

    return k_shortest_paths


def visualize_roads(cities, roads):
    """
    Visualize the road network using NetworkX and Matplotlib.
    """
    G = nx.Graph()

    # Add cities as nodes and roads as edges
    for city in cities:
        G.add_node(city)

    for city, connections in roads.items():
        for neighbor, distance in connections:
            G.add_edge(city, neighbor, weight=distance)

    # Layout and visualization
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    
    # Display edge labels with road distances
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Road Network Visualization")
    plt.show()


# Example cities and roads data
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

# Get start and goal cities from user input
start_city = input('Enter the start city: ')
goal_city = input('Enter the goal city: ')

# Add a new road between the start and goal city with a cost of 400
roads[start_city].append((goal_city, 400))
roads[goal_city].append((start_city, 400))

# Set k value (number of shortest paths to find)
k = 2  # You can change this to any number of paths you'd like to find

# Find the k-shortest paths
k_shortest_paths = yen_k_shortest_paths(cities, roads, start_city, goal_city, k)

# Print the k-shortest paths and their costs
for idx, (path, cost) in enumerate(k_shortest_paths, 1):
    print(f"Path {idx}: {path} with total cost {cost}")

# Visualize the road network before and after the road addition
print("\nVisualizing road network before finding paths:")
visualize_roads(cities, roads)
