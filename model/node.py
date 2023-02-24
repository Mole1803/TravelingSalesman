from __future__ import annotations


class Border:
    def __init__(self, weight, node_1, node_2):
        self.weight: float = weight
        self.node: Node or None = None
        self.set_nodes(node_1, node_2)

    def set_nodes(self, node_1, node_2):
        self.node = node_1
        node_2.add_border(self)


class Node:
    def __init__(self, id_: int):
        self.id: int = id_
        self.borders: list[Border] = []

    def add_border(self, border: Border):
        self.borders.append(border)

    def get_border(self, node: Node):
        for border in self.borders:
            if node == border.node:
                return border
