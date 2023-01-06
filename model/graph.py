import csv


def read_csv(csv_file):
    """Reads a csv file and returns a list of lists"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        return list(reader)

def create_nodes(csv_file):
    """Creates nodes from a csv file"""
    data = read_csv(csv_file)
    graph = {
    }
    node_list = []

    for row in data:
        border_tupel = (row[0], row[1], row[2])
        node_list.append(border_tupel)
        if row[0] not in graph:
            graph[row[0]] = []
        if row[1] not in graph:
            graph[row[1]] = []
        graph[row[0]].append(node_list[-1])
        graph[row[1]].append(node_list[-1])
    return graph, node_list


def solve(graph,node_list):
    for key_, value_ in graph.items():
        print(key_,value_)
        for node in value_:
            print(node)


