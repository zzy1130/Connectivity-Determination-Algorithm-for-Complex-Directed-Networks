import numpy as np
import random

def generate_complex_directed_network(num_nodes, num_edges):
    # Create an adjacency matrix initialized to zeros
    adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    # Generate unique edges
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        edges.add((u, v))  # Self-loops are now allowed

    # Fill the adjacency matrix based on the generated edges
    for (u, v) in edges:
        adjacency_matrix[u][v] = 1

    return adjacency_matrix
