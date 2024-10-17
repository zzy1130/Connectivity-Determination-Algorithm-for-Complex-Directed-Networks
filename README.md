# Connectivity-Determination-Algorithm-for-Complex-Directed-Networks

## Results Reproduction Prerequisite
**Code Download**
```
git clone https://github.com/zzy1130/Connectivity-Determination-Algorithm-for-Complex-Directed-Networks.git
```
**Environment Suggestions**
```
python==3.8.20
numpy==1.24.3
networkx==2.8.4
matplotlib==3.7.1
pandas==1.5.3
tqdm==4.65.0
```
## Use Cases
### A. Adjacency matrix input
In ``main.py``, replace the content of ``input_string`` variable at line 65 with your matrix and run (the sample matrix has been given):
```
python main.py
```
After running, the connectivity result will be given.
### B. A single random network
Example usage: 
```
python main.py --random_net True --num_nodes 2000 --num_edges 4000
```
num_nodes specifies the number of nodes of the network and num_edges specifies that of edges.
After running, ``directed_network.jpg`` will be outputted to the main directory. ``nodes.csv`` and ``edges.csv`` will be generated, indicating the node set and edge set of the network. ``reduced_nodes.csv`` and ``reduced_edges.csv`` will be generated, indicating the node set and edge set of the reduced network after running tarjan algorithm. 
In addition, the connectivity type will be printed in the output.

### C. Enumerate all networks with node number and edge number being specified
Example usage:
```
python random_network.py --constrained True --num_nodes 5 --num_edges 5
```
for injective graphs
```
python random_network.py --num_nodes 5 --num_edges 5
```
for graphs with no constraints

### D. The Erd\H{o}s--R\'{e}nyi graphs experiment
Example usage:
```
python erdos_renyi.py --num_nodes 1000 --start_p 0.01 --final_p 0.5 --sample_num 1000 --p_num 51
```
``num_nodes`` specifies the number of nodes inside the network, ``start_p`` is the initial value of p, ``final_p`` is the final value of p, ``sample_num`` specifies the number of random samples generated for each p value, and ``p_num is`` the number of p value in the experiment. 



