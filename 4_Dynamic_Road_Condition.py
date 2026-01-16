import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Function to find the shortest path considering dynamic road conditions
def find_shortest_path_with_dynamic_roads(cities, roads, start_city, goal_city):
    # Priority queue to store cities to explore with the total cost, current city, and path taken
    pq = [(0, start_city, [])]
    visited = set()  # Set to keep track of visited cities

    # While there are still cities to explore in the queue
    while pq:
        current_cost, current_city, path = heapq.heappop(pq)

        # If we've reached the goal city, return the path and cost
        if current_city == goal_city:
            return path + [current_city], current_cost

        # Skip if the city has already been visited
        if current_city in visited:
            continue

        visited.add(current_city)

        # Explore the neighboring cities
        for neighbor, distance in roads.get(current_city, []):
            if neighbor not in visited:
                heapq.heappush(pq, (current_cost + distance, neighbor, path + [current_city]))

    # Return an empty path and infinite cost if no path is found
    return [], float('inf')


# Function to block a road between two cities (remove a road)
def remove_road(roads, city1, city2):
    # Remove the connection between the two cities in both directions
    if city1 in roads:
        roads[city1] = [conn for conn in roads[city1] if conn[0] != city2]
    if city2 in roads:
        roads[city2] = [conn for conn in roads[city2] if conn[0] != city1]


# Function to visualize the road network using NetworkX
def visualize_roads(cities, roads):
    G = nx.Graph()
    
    # Add nodes (cities)
    for city in cities:
        G.add_node(city)

    # Add edges (roads) with weights (distances)
    for city, connections in roads.items():
        for neighbor, distance in connections:
            G.add_edge(city, neighbor, weight=distance)

    # Create a layout for positioning nodes
    pos = nx.spring_layout(G)
    
    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')

    # Draw edge labels for the weights (distances)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Show the plot
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

# Take input for the start and goal cities
start_city = input('Enter the start city: ')
goal_city = input('Enter the goal city: ')

# Visualize the road network before blocking a road
print("\nVisualizing road network before blocking the road:")
visualize_roads(cities, roads)

# Remove the road between the start and goal cities
remove_road(roads, start_city, goal_city)

# Simulate a new road (or rerouted path) with a cost of 400
roads[start_city].append((goal_city, 400))
roads[goal_city].append((start_city, 400))

# Visualize the updated road network after blocking the road
print("\nVisualizing road network after blocking the road:")
visualize_roads(cities, roads)

# Check the connectivity between the start and goal cities
print(f"\nChecking the path from {start_city} to {goal_city}:")
dynamic_path, dynamic_cost = find_shortest_path_with_dynamic_roads(cities, roads, start_city, goal_city)

# Print the result of the pathfinding
if dynamic_path:
    print(f"Path found: {dynamic_path} with a total cost of {dynamic_cost}")
else:
    print(f"No path found from {start_city} to {goal_city} after road removal.")
