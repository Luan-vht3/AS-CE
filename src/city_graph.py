import networkx as nx
import random

def generate_city_graph(
        neighborhoods: list[str],
        file_name: str = "src/city_graph.adjlist"
    ) -> None:
    G = nx.Graph()
    G.add_nodes_from(neighborhoods)

    # Add edges (neighborhood borders) between nodes
    for neighborhood in neighborhoods:
        num_edges = random.randint(1, 5)
        for _ in range(num_edges):
            neighbor = random.choice(neighborhoods)
            if neighbor != neighborhood and not G.has_edge(neighborhood, neighbor):
                G.add_edge(neighborhood, neighbor)
    
    # Export the graph to a file
    nx.write_adjlist(G, file_name)

    print(f"Graph generation complete. City graph saved to {file_name}.")
