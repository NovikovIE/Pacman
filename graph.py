from gameObject import GameObject
from config import BRICKSWIDTH, BRICKSHEIGHT
from collections import deque


class Vertex(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, BRICKSWIDTH, BRICKSHEIGHT)
        self.neighbours = []


class Graph:
    def __init__(self, length):
        self.length = length
        self.edges = []
        for i in range(length):
            self.edges.append([])
        self.nodes = [Vertex] * length
        self.vertices_by_coords = dict()

    def add_edge(self, v, u):
        self.edges[v].append(u)
        self.edges[u].append(v)

    def add_vertex(self, v: int, x, y):
        self.nodes[v] = Vertex(x, y)
        self.vertices_by_coords[(x, y)] = v

    def bfs(self, v):
        self.used[v] = True
        self.deq.append(v)
        self.path_lenghts[v] = 0
        while len(self.deq) != 0:
            vertex = self.deq.popleft()
            for u in self.edges[vertex]:
                if self.path_lenghts[u] == -1:
                    self.deq.append(u)
                    self.path_lenghts[u] = self.path_lenghts[vertex] + 1
                    self.parent[u] = vertex

    # searches the shortest path from v to u
    def find_path(self, v, u):
        self.used = [False] * self.length
        self.deq = deque()
        self.path_lenghts = [-1] * self.length
        self.parent = [int] * self.length
        self.bfs(v)
        path = []
        while v != u:
            path.append(self.nodes[u])
            u = self.parent[u]
        path.append(self.nodes[v])
        path.reverse()
        return path
