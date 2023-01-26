class Border:
    def __init__(self, weight, node_1, node_2):
        self.weight = weight
        self.nodes = None
        self.set_nodes(node_1,node_2)
    def set_nodes(self,node_1, node_2):
        self.nodes = (node_1, node_2)
        self.nodes[0].addBorder(self)
        self.nodes[1].addBorder(self)

class Node:
    def __init__(self, name):
        self.name = name
        self.borders = []

    def addBorder(self,border):
        self.borders.append(border)

    def getBorders(self):
        #erg=[]
        #for border in self.borders:
        #    bordercopy=border.nodes
        #    bordercopy.remove(self.name)
        #    bordercopy=bordercopy[0]
        #    erg.append((bordercopy,border.weight))
        #return erg
        pass
