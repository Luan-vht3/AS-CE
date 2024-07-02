import networkx as nx
import random

def generate_city_graph(neighborhoods: list[str]) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(neighborhoods)

    # Add edges (neighborhood borders) between nodes
    for neighborhood in neighborhoods:
        num_edges = random.randint(1, 5)
        for _ in range(num_edges):
            neighbor = random.choice(neighborhoods)
            if neighbor != neighborhood and not G.has_edge(neighborhood, neighbor):
                G.add_edge(neighborhood, neighbor)
    
    print(f"City graph generation complete.")

    return G


if __name__ == "__main__":
    neighborhoods = [f"N{i}" for i in range(10)]
    G = generate_city_graph(neighborhoods)
    print(G.edges)
