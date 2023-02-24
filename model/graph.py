import math
from model.node import Border, Node


class Graph:
    def __init__(self):
        self.graph: list[Node] = []
        self.result: list[Node] = []

    def read_points(self, points):
        borders = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                borders.append((points[i].id, points[j].id, Graph.calculate_single_weight(points[i], points[j])))
        for row in borders:
            node1 = None
            node2 = None
            for node in self.graph:
                if row[0] == node.id:
                    node1 = node
                if row[1] == node.id:
                    node2 = node
            if not node1:
                node1 = Node(row[0])
            if not node2:
                node2 = Node(row[1])
            Border(int(row[2]), node1, node2)
            Border(int(row[2]), node2, node1)
            if node1 not in self.graph:
                self.graph.append(node1)
            if node2 not in self.graph:
                self.graph.append(node2)

    @staticmethod
    def calculate_single_weight(point1, point2):
        return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

    def solve_greedy(self):
        node = self.graph[0]
        for i in range(len(self.graph)):
            node = self.get_next_node_greedy(node)
        self.result.append(self.result[0])

    def get_result_ids(self):
        result = []
        for node in self.result:
            result.append(node.id)
        return result

    def get_next_node_greedy(self, node):
        next_node, distance = None, None
        for border in node.borders:
            old = False
            if len(self.result) > 0:
                if border.node in self.result:
                    old = True
            if not old:
                if not distance:
                    distance = border.weight
                if border.weight <= distance:
                    distance = border.weight
                    next_node = border.node
        self.result.append(node)
        self.graph = [ele for ele in self.graph if ele != node]
        return next_node

    def calculate_weight(self):
        weight = 0
        for i in range(len(self.result) - 1):
            weight += self.result[i].get_border(self.result[i + 1]).weight
        return weight

    def solve_brute_force_start(self):
        min_weight, min_path = self.solve_brute_force(self.graph[0], [], 0, float('inf'), [])
        self.result = min_path

    def solve_brute_force(self, node, visited, weight, min_weight, min_path):
        visited.append(node)
        if weight > min_weight:
            return min_weight, min_path
        if len(visited) == len(self.graph):
            weight += node.get_border(visited[0]).weight
            visited.append(visited[0])
            if weight < min_weight:
                min_weight = weight
                min_path = visited
            return min_weight, min_path
        for border in node.borders:
            if border.node not in visited:
                min_weight, min_path = self.solve_brute_force(border.node, visited[:], weight + border.weight,
                                                              min_weight, min_path)
        return min_weight, min_path

