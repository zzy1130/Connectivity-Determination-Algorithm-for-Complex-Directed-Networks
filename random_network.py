import numpy as np
from itertools import combinations, product
import argparse
from tarjan import Graph
from unilateral import is_unilaterally_connected
from weak import to_undirected
from tqdm import tqdm
import time
import math

def generate_adjacency_matrices(num_nodes, num_edges):
    possible_edges = [(i, j) for i in range(num_nodes) for j in range(num_nodes)]
    edge_combinations = combinations(possible_edges, num_edges)
    strong = 0
    unilateral = 0
    weak = 0
    mat_num = 0
    total_iterations = math.comb(num_nodes*num_nodes, num_nodes)
    # Generate combinations of edges
    # for edges in combinations(possible_edges, num_edges):
    for edges in tqdm(combinations(possible_edges, num_edges), total=total_iterations):
        mat_num += 1
        matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        for (u, v) in edges:
            matrix[u][v] = 1
        graph = Graph(matrix)
        sccs = graph.tarjan()
        if len(sccs) == 1:
            strong += 1
            unilateral += 1
            weak += 1
            continue
        else:
            reduced_graph = graph.build_reduced_graph(sccs)
            reachability_matrix = graph.find_reachability_matrix(reduced_graph)
            if (is_unilaterally_connected(reachability_matrix)):
                unilateral += 1
                weak += 1
                continue
            else:
                mat = to_undirected(matrix)
                undirected_graph = Graph(mat)
                sccs = undirected_graph.tarjan()
                if (len(sccs)==1):
                    weak += 1
    print(str(strong)+" cases out of "+str(mat_num)+" are strongly connected")
    print(str(unilateral)+" cases out of "+str(mat_num)+" are unilaterally connected")
    print(str(weak)+" cases out of "+str(mat_num)+" are weakly connected")

    
from itertools import combinations

def constrained_generate_adjacency_matrices(num_nodes, num_edges):
    # Ensure that num_edges does not exceed num_nodes (each can have only one outgoing edge)
    if num_edges > num_nodes:
        raise ValueError("Number of edges cannot exceed the number of nodes when limiting to one outgoing edge per node.")
    
    # Possible edges where each node can only have one outgoing edge
    possible_edges = [(i, j) for i in range(num_nodes) for j in range(num_nodes)]
    strong = 0
    unilateral = 0
    weak = 0
    mat_num = 0
    total_iterations = math.comb(num_nodes*num_nodes, num_nodes)
    # Generate combinations of edges
    # for edges in combinations(possible_edges, num_edges):
    for edges in tqdm(combinations(possible_edges, num_edges), total=total_iterations):
        # Create an adjacency matrix
        matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        
        # Check for outgoing edge constraints
        outgoing_count = [0] * num_nodes
        constrained = True
        for (u, v) in edges:
            # Ensure that node u does not already have an outgoing edge
            outgoing_count[u] += 1
            matrix[u][v] = 1
            if outgoing_count[u] > 1:
                constrained = False
                break
        if not constrained:
            continue
        mat_num+=1
        
        graph = Graph(matrix)
        sccs = graph.tarjan()
        
        if len(sccs) == 1:
            strong += 1
            unilateral += 1
            weak += 1
            continue
        else:
            reduced_graph = graph.build_reduced_graph(sccs)
            reachability_matrix = graph.find_reachability_matrix(reduced_graph)
            if is_unilaterally_connected(reachability_matrix):
                unilateral += 1
                weak += 1
                continue
            else:
                
                mat = to_undirected(matrix)
                undirected_graph = Graph(mat)
                sccs = undirected_graph.tarjan()
                if len(sccs) == 1:
                    weak += 1

    print(str(strong)+" cases out of "+str(mat_num)+" are strongly connected")
    print(str(unilateral)+" cases out of "+str(mat_num)+" are unilaterally connected")
    print(str(weak)+" cases out of "+str(mat_num)+" are weakly connected")
        
    
    

def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Generate directed network adjacency matrices.')
    parser.add_argument('--constrained', type=bool, help='If constraining one node to have one outgoing edge')
    parser.add_argument('--num_nodes', type=int, help='Number of nodes in the graph')
    parser.add_argument('--num_edges', type=int, help='Number of edges in the graph')

    args = parser.parse_args()
    if not args.constrained:
        generate_adjacency_matrices(args.num_nodes, args.num_edges)
    else:
        constrained_generate_adjacency_matrices(args.num_nodes, args.num_edges)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time spent: {elapsed_time} seconds")

if __name__ == "__main__":
    main()