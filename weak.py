def to_undirected(graph):
    size = len(graph)
    for i in range(size):
        for j in range(size):
            if i != j:
                if graph[i][j] == 1:
                    graph[j][i] = 1
    return graph