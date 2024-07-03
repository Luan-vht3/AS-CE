import networkx as nx
import random

def generate_city_graph(neighborhoods: list[str]) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(neighborhoods)

    # Ensure the graph is connected by creating a spanning tree first
    for i in range(len(neighborhoods) - 1):
        G.add_edge(neighborhoods[i], neighborhoods[i + 1])

    # Add additional random edges
    for neighborhood in neighborhoods:
        num_additional_edges = random.randint(1, 5) - 1  # Subtracting 1 because each node already has 1 edge in the spanning tree
        for _ in range(num_additional_edges):
            neighbor = random.choice(neighborhoods)
            if neighbor != neighborhood and not G.has_edge(neighborhood, neighbor):
                G.add_edge(neighborhood, neighbor)

    print("City graph generation complete.")
    return G

if __name__ == "__main__":
    neighborhoods = [f"N{i}" for i in range(10)]
    G = generate_city_graph(neighborhoods)
    print(G.edges)
