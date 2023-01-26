import csv
from model.node import Border,Node

def read_csv(csv_file):
    """Reads a csv file and returns a list of lists"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def create_nodes(csv_file):
    """Creates nodes from a csv file"""
    data = read_csv(csv_file)
    graph = []
    node_list = []
    for row in data:
        node1=None
        node2=None
        for node in graph:
            if row[0]==node.name:
                node1=node
            if row[1]==node.name:
                node2=node
        if not node1:
            node1=Node(row[0])
        if not node2:
            node2=Node(row[1])
        Border(int(row[2]), node1, node2)
        #border_tupel = Border(row[0], node1, node2)
        #node_list.append(border_tupel)
        if node1 not in graph:
            graph.append(node1)
        if node2 not in graph:
            graph.append(node2)
    print(graph)
    return graph, node_list


def solve(graph,node_list):
    for key_, value_ in graph.items():
        print(key_,value_)
        for node in value_:
            print(node)


