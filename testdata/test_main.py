from model.graph import Graph

if __name__ == '__main__':
    graph=Graph()
    graph.read_points([(0, 447, 196), (1, 353, 243), (2, 243, 181), (3, 245, 108), (4, 164, 128), (5, 173, 268), (6, 383, 229), (7, 397, 39), (8, 178, 65)])
    graph.create_nodes()
    graph.solve_greedy()
    graph.get_result_ids()
    #print(graph.calculate_weight())