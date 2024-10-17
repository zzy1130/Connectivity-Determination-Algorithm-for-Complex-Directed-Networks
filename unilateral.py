def is_unilaterally_connected(reachability_matrix):
    size = len(reachability_matrix)
    
    for i in range(size):
        for j in range(size):
            if i != j:
                if reachability_matrix[i][j] == 0 and reachability_matrix[j][i] == 0:
                    return False
    return True