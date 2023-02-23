import csv
import math
from copy import copy

from model.node import Border,Node

class Graph:
    def __init__(self):
        #self.csv_file=csv_file
        #self.points=[]
        self.borders=[]
        self.graph=[]
        self.result=[]
        self.create_nodes()


    def read_points(self,points):
        #self.points=points
        for i in range(len(points)):
            for j in range(i+1,len(points)):
                self.borders.append((points[i].id,points[j].id,Graph.calculate_single_weight(points[i],points[j])))

    @staticmethod
    def calculate_single_weight(point1,point2):
        return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)

    #def read_csv(self):
    #    """Reads a csv file and returns a list of lists"""
    #    with open(self.csv_file, 'r') as f:
    #        reader = csv.reader(f)
    #        return list(reader)

    def create_nodes(self):
        """Creates nodes from a csv file"""
        #data = self.read_csv()
        data=self.borders
        graph = []
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
            Border(int(row[2]), node2, node1)
            #border_tupel = Border(row[0], node1, node2)
            #node_list.append(border_tupel)
            if node1 not in graph:
                graph.append(node1)
            if node2 not in graph:
                graph.append(node2)
        self.graph=graph



    def solve_greedy(self):
        node=self.graph[0]
        for i in range(len(self.graph)):
            node=self.getNextNodeGreedy(node)
        self.result.append(self.result[0])
        for node in self.result:
            print(node.name)

    def get_result_ids(self):
        result=[]
        for node in self.result:
            result.append(node.name)
            #print(node.name)
        return result

    def getNextNodeGreedy(self,node):
        next_node,entfernung=None,None
        for border in node.borders:
            old = False
            if len(self.result)>0:
                if border.node in self.result:
                    old=True
            if not old:
                if not entfernung:
                    entfernung=border.weight
                if border.weight<=entfernung:
                    entfernung=border.weight
                    next_node=border.node

        self.result.append(node)
        self.graph=[ele for ele in self.graph if ele != node]
        return next_node

    def calculate_weight(self):
        weight=0
        for i in range(len(self.result)-1):
            weight+=self.result[i].getBorder(self.result[i+1]).weight
        return weight

    def solve_brute_force_start(self):
        min_weight, min_path = self.solve_brute_force(self.graph[0], [], 0, float('inf'), [])
        self.result=min_path




    def solve_brute_force(self, node, visited, weight, min_weight, min_path):
        visited.append(node)
        if len(visited) == len(self.graph):
            weight += node.getBorder(visited[0]).weight
            visited.append(visited[0])
            if weight < min_weight:
                min_weight = weight
                min_path = visited

            return min_weight, min_path
        for border in node.borders:
            if border.node not in visited:
                min_weight, min_path = self.solve_brute_force(border.node, visited[:], weight + border.weight, min_weight, min_path)
        return min_weight, min_path
