import networkx as nx
import matplotlib.pyplot as plt

# Define cities and roads
cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

# Create the graph
G = nx.Graph()
for city, connections in roads.items():
    for neighbor, distance in connections:
        G.add_edge(city, neighbor, weight=distance)

# Find the shortest path
source = input("Insert the Initial City: ")
target = input("Insert the Goal City: ")
shortest_path = nx.shortest_path(G, source=source, target=target, weight='weight')
print(f"Shortest path from {source} to {target}: {shortest_path}")

# Visualize the graph
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=500, font_size=12)

# Add edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# Highlight the shortest path
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=2)

plt.title("Ethiopian Cities Road Network", fontsize=14)
plt.show()
