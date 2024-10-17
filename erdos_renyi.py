import networkx as nx
import numpy as np
from itertools import combinations, product
import argparse
from tarjan import Graph
from unilateral import is_unilaterally_connected
from weak import to_undirected
from tqdm import tqdm
import csv
import time
import math

def network_exp(start_p, final_p, sample_num, num_nodes, p_num):
    filename = f"{num_nodes}_{start_p}_erdos_renyi_network_results.csv"
    with open(filename , mode='w', newline='') as csvfile:
        fieldnames = ['p_value', 'strong', 'unilateral', 'weak', 'disconnected', 'scc_mean', 'edge_mean']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        for i in np.arange(start_p, final_p + (final_p-start_p) / p_num, (final_p-start_p) / p_num):
            
            p_value = round(i, 4)
            print("For p with value of: ",p_value)
            strong = 0
            unilateral = 0
            weak = 0
            edge_num = []
            scc_num = []

            for num in tqdm(range(sample_num), desc="Sampling"):
                network = nx.erdos_renyi_graph(num_nodes, p_value, directed=True)
                num_edges = network.number_of_edges()
                edge_num.append(num_edges)
                adjacency_matrix = nx.to_numpy_array(network, dtype=int)
                net = Graph(adjacency_matrix)
                
                sccs = net.tarjan()
                scc_num.append(len(sccs))

                if len(sccs) == 1:
                    strong += 1
                    unilateral += 1
                    weak += 1
                    continue
                else:
                    reduced_graph = net.build_reduced_graph(sccs)
                    reachability_matrix = net.find_reachability_matrix(reduced_graph)
                    if is_unilaterally_connected(reachability_matrix):
                        unilateral += 1
                        weak += 1
                        continue
                    else:
                        mat = to_undirected(adjacency_matrix)
                        undirected_graph = Graph(mat)
                        weak_sccs = undirected_graph.tarjan()
                        if len(weak_sccs) == 1:
                            weak += 1
            
            disconnection = sample_num - weak
            scc_num = np.array(scc_num)
            edge_num = np.array(edge_num)
            scc_mean = np.mean(scc_num)
            edge_mean = np.mean(edge_num)

            print(str(strong) + " cases out of " + str(sample_num) + " are strongly connected")
            print(str(unilateral) + " cases out of " + str(sample_num) + " are unilaterally connected")
            print(str(weak) + " cases out of " + str(sample_num) + " are weakly connected")
            print(str(disconnection) + " cases out of " + str(sample_num) + " are unconnected")

            # Write the results for this p_value to the CSV
            writer.writerow({
                'p_value': p_value,
                'strong': strong,
                'unilateral': unilateral,
                'weak': weak,
                'disconnected': disconnection,
                'scc_mean': scc_mean,
                'edge_mean': edge_mean
            })

def main():
    parser = argparse.ArgumentParser(description='Generate directed network adjacency matrices.')
    parser.add_argument('--num_nodes', type=int, help='Number of nodes in the graph')
    parser.add_argument('--start_p', type=float, help='the initial value of p')
    parser.add_argument('--final_p', type=float, help='the final value of p')
    parser.add_argument('--sample_num', type=int, help='the number of samples for every p value')
    parser.add_argument('--p_num', type=int, help='the number of p in the experiment')
    args = parser.parse_args()

    network_exp(args.start_p, args.final_p, args.sample_num, args.num_nodes, args.p_num)
if __name__ == "__main__":
    main()
