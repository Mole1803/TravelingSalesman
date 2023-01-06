class border:
    def __init__(self, weight, node1, node2):
        self.weight = weight
        self.node1 = node1
        self.node2 = node2
        node1.setBorder(self)
        node2.setBorder(self)

class node:
    def __init__(self, name):
        self.name = name
        self.borders = []

    def addBorder(self,border):
        self.borders.append(border)
