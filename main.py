from tarjan import Graph
from unilateral import is_unilaterally_connected
from weak import to_undirected
import argparse
from net_gen import generate_complex_directed_network
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def parse_input(input_string):
    lines = input_string.strip().split("\n")
    matrix = [list(map(int, line.split(","))) for line in lines]
    return matrix

def format_reachability_matrix(reachability_matrix):
    return "\n".join(",".join(map(str, row)) for row in reachability_matrix)

def save_gephi_files(adjacency_matrix, nodes_file, edges_file):
    # Get the number of nodes
    num_nodes = adjacency_matrix.shape[0]

    # Create the nodes DataFrame
    nodes = pd.DataFrame({
        'Id': range(num_nodes),
        'Label': [f'Node {i}' for i in range(num_nodes)]
    })

    # Save the nodes DataFrame to a CSV file
    nodes.to_csv(nodes_file, index=False)

    # Create the edges DataFrame
    edges = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i, j] > 0:  # Assuming non-zero indicates an edge
                edges.append({'Source': i, 'Target': j, 'Weight': adjacency_matrix[i, j]*1})

    edges_df = pd.DataFrame(edges)

    # Save the edges DataFrame to a CSV file
    edges_df.to_csv(edges_file, index=False)

def draw_network_from_adjacency_matrix(adjacency_matrix, output_file, csv):
    df = pd.DataFrame(adjacency_matrix)
    # Save the DataFrame to a CSV file
    df.to_csv(csv, index=False, header=False)
    print(f"Adjacency matrix saved as {output_file}")

    # Create a directed graph from the adjacency matrix
    G = nx.from_numpy_matrix(adjacency_matrix, create_using=nx.DiGraph)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx(G, pos, arrows=True, node_size=200, node_color='lightblue', font_size=6)
    plt.title("Directed Network from Adjacency Matrix")

    # Save the figure as a JPG file
    plt.savefig(output_file, format='jpg', bbox_inches='tight')
    plt.close()  # Close the plot to free up memory

# Example usage
input_string = """0,1,1,0,0,0,0,0
0,0,0,1,1,0,0,0
0,0,0,0,1,0,0,0
0,0,0,0,0,1,1,0
1,0,0,0,0,1,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0
0,0,0,0,0,1,0,0"""

if __name__== "__main__" :
    start_time = time.time()
    network_type = ""
    parser = argparse.ArgumentParser(description='Generate directed network adjacency matrices.')
    parser.add_argument('--random_net', type=bool, help='Number of nodes in the graph')
    parser.add_argument('--num_nodes', type=int, help='Number of nodes in the graph')
    parser.add_argument('--num_edges', type=int, help='Number of edges in the graph')
    
    args = parser.parse_args()
    if args.random_net:
        matrix = generate_complex_directed_network(args.num_nodes, args.num_edges)
    else:
        matrix = parse_input(input_string)
    adjacency_matrix = np.array(matrix)
    output_file = "directed_network.jpg"
    output_csv = "directed_network.csv"
    # Draw the network and save it
    nodes_file = "nodes.csv"
    edges_file = "edges.csv"

    # Save the adjacency matrix in Gephi format
    save_gephi_files(adjacency_matrix, nodes_file, edges_file)
    # draw_network_from_adjacency_matrix(adjacency_matrix, output_file, output_csv)
    graph = Graph(matrix)
    sccs = graph.tarjan()
    if len(sccs) > 1:
        network_type = "Strong Connectivity"
    
    print("Strongly Connected Components:", sccs)

    reduced_graph = graph.build_reduced_graph(sccs)
    print("reduced graph: ", reduced_graph)

    sub_nodes_file = "sub_nodes.csv"
    sub_edges_file = "sub_edges.csv"
    save_gephi_files(np.array(reduced_graph), sub_nodes_file, sub_edges_file)

    # Find the reachability matrix of the reduced graph
    reachability_matrix = graph.find_reachability_matrix(reduced_graph)
    formatted_reachability_matrix = format_reachability_matrix(reachability_matrix)
    # print("Reachability Matrix (as adjacency matrix):\n", formatted_reachability_matrix)

    print("If unilaterally connected: ", is_unilaterally_connected(reachability_matrix))
    mat = to_undirected(matrix)
    undirected_graph = Graph(mat)
    sccs = undirected_graph.tarjan()
    print(sccs)
    weak_connectivity = (len(sccs)==1)
    print("If weakly connected:", weak_connectivity)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time spent: {elapsed_time} seconds")
    




