from model.graph import create_nodes,solve

if __name__ == '__main__':
    graph, node = create_nodes('nodes.csv')
    #print(graph)
    #print(node)
    solve(graph,node)