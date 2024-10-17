class Graph:
    def __init__(self, matrix):
        self.V = len(matrix)
        self.adj = [[] for _ in range(self.V)]
        for i in range(self.V):
            for j in range(self.V):
                if matrix[i][j] == 1:
                    self.adj[i].append(j)

    def to_undirected(self):
        size = len(self.adj)
        print(self.adj)
        for i in range(size):
            for j in range(size):
                if i != j:
                    if self.adj[i][j] == 1 and self.adj[j][i] == 0:
                        self.adj[j][i] = 1

    def tarjan_util(self, v, low, disc, stack_member, stack, sccs):
        disc[v] = low[v] = self.time
        self.time += 1
        stack.append(v)
        stack_member[v] = True

        for neighbor in self.adj[v]:
            if disc[neighbor] == -1:  # If neighbor is not visited
                self.tarjan_util(neighbor, low, disc, stack_member, stack, sccs)
                low[v] = min(low[v], low[neighbor])
            elif stack_member[neighbor]:  # If neighbor is in the stack, it's part of the current SCC
                low[v] = min(low[v], disc[neighbor])

        if low[v] == disc[v]:
            scc = []
            while True:
                w = stack.pop()
                stack_member[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    def tarjan(self):
        disc = [-1] * self.V
        low = [-1] * self.V
        stack_member = [False] * self.V
        stack = []
        self.time = 0
        sccs = []

        for i in range(self.V):
            if disc[i] == -1:
                self.tarjan_util(i, low, disc, stack_member, stack, sccs)

        return sccs

    def build_reduced_graph(self, sccs):
        scc_index = {}
        for index, component in enumerate(sccs):
            for node in component:
                scc_index[node] = index

        reduced_size = len(sccs)
        reduced_graph = [[0] * reduced_size for _ in range(reduced_size)]

        for v in range(self.V):
            for neighbor in self.adj[v]:
                if scc_index[v] != scc_index[neighbor]:
                    reduced_graph[scc_index[v]][scc_index[neighbor]] = 1

        return reduced_graph

    def dfs(self, v, visited, reachability_matrix):
        visited[v] = True
        for neighbor in range(len(self.adj[v])):
            if self.adj[v][neighbor] == 1 and neighbor != v:
                reachability_matrix[v][neighbor] =1 
                if not visited[neighbor]:
                    # reachability_matrix[v][neighbor] = 1
                    self.dfs(neighbor, visited, reachability_matrix)
                for n in range(len(self.adj)):
                    if reachability_matrix[neighbor][n] == 1:
                        reachability_matrix[v][n] = 1

    def find_reachability_matrix(self, reduced_graph):
        size = len(reduced_graph)
        reachability_matrix = [[0] * size for _ in range(size)]
        visited = [False] * size
        for i in range(size):
            self.adj = reduced_graph  # Set current adjacency list to the reduced graph
            self.dfs(i, visited, reachability_matrix)
            reachability_matrix[i][i] = 1  # Ensure each vertex can reach itself

        return reachability_matrix

