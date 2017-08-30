import numpy as np


class UnionFindDisjointSet(object):
    def __init__(self, graph):
        self.parents = -1 * np.ones(graph.shape + (2,), dtype='int32')
        self.counter = np.ones_like(graph, dtype='int32')

    def get_set(self, u):
        if (self.parents[u[0], u[1]] == (-1, -1)).all():
            return u
        else:
            self.parents[u[0], u[1]] = self.get_set(self.parents[u[0], u[1]])
            return self.parents[u[0], u[1]]

    def is_same_set(self, u, v):
        return (self.get_set(u) == self.get_set(v)).all()

    def union_set(self, u, v):
        if not self.is_same_set(u, v):
            u, v = self.get_set(u), self.get_set(v)

            aux = self.counter[v[0], v[1]]
            self.counter[v[0], v[1]] = 0
            self.parents[v[0], v[1]] = (u[0], u[1])
            self.counter[u[0], u[1]] = self.counter[u[0], u[1]] + aux

    def get_count_set(self, u):
        return self.counter[self.get_set(u)[0], self.get_set(u)[1]]

    def get_count_max(self):
        return self.counter.max()


# Preserves the connected component of graph with the biggest num of nodes (1 or more components)
def longest_connected_component(graph, neighbors, is_active):
    graph = np.asarray(graph, dtype='int32')
    neighbors = np.asarray(neighbors, dtype='int32').reshape((-1, 2))

    myset = UnionFindDisjointSet(graph)
    aux = cartesian_product(np.arange(graph.shape[0]), np.arange(graph.shape[1])).reshape((-1, 2)).astype('int32')

    for i, j in aux:
        if is_active(graph, i, j):
            for neigh in neighbors:
                n = (i, j) + neigh
                if (n >= 0).all() and (n < graph.shape).all() and is_active(graph, n[0], n[1]):
                    myset.union_set((i, j), n)

    return np.asarray([is_active(graph, u[0], u[1]) and myset.get_count_set(u) == myset.get_count_max() for u in aux],
                      dtype='bool').reshape(graph.shape)


def longest_connected_component2(graph, neighbors, filter):
    graph = np.asarray(graph, dtype='int32')
    neighbors = np.asarray(neighbors).reshape((-1, 2))
    visited = np.zeros_like(graph, np.bool)

    def dfs(updater, count, coords):
        coords = np.asarray(coords)

        if ((coords > 0).all() and (coords < graph.shape).all() and
                not visited[coords[0]][coords[1]] and filter(graph, coords[0], coords[1])):
            visited[coords[0]][coords[1]] = True
            graph[coords[0]][coords[1]] = updater(count)

            for neigh in neighbors:
                dfs(updater, updater(count), coords + neigh)

    for i in range(0, graph.shape[0]):
        for j in range(0, graph.shape[1]):
            dfs(lambda c: c + 1, 0, (i, j))

    visited = np.zeros_like(graph, np.bool)
    dfs(lambda c: c, graph.max() + 1, (graph.argmax() // graph.shape[1], graph.argmax() % graph.shape[1]))

    graph = (graph // graph.max()).astype('bool')
    return graph


# Auxiliar function that performs the cartesian product of two row-matrices and reshape them
def cartesian_product(ys, xs):
    xs, ys = (np.asarray(xs), np.asarray(ys))
    product = np.transpose([np.tile(xs, len(ys)), np.repeat(ys, len(xs))])
    product = product[:, [1, 0]].reshape((len(ys), len(xs), 2))
    return product
