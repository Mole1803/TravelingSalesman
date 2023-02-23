class Border:
    def __init__(self, weight, node_1, node_2):
        self.weight = weight
        self.node = None
        self.set_nodes(node_1,node_2)
    def set_nodes(self,node_1, node_2):
        self.node = node_1
        node_2.addBorder(self)


class Node:
    def __init__(self, name):
        self.name = name
        self.borders = []

    def addBorder(self,border):
        self.borders.append(border)

    def getBorder(self,node):
        for border in self.borders:
            if node == border.node:
                return border
