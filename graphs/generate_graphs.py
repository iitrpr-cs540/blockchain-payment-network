import numpy as np
import random

def make_list(num_nodes, num_edges, weight):
    # assign edges
    adj_list = []
    edge_list = []

    # Make MST
    for i in range(0, num_nodes-1):
        adj_list.append([i, i+1, weight])
        edge_list.append({i, i+1})
        num_edges -=1

    # connect random remaining edges
    for _ in range(num_edges):
        node1 = random.randint(0, np.floor(num_nodes/2))
        node2 = random.randint(node1+1, num_nodes-1)
        if {node1, node2} not in edge_list:
            adj_list.append([node1, node2, weight])
    
    return adj_list

def write_graph(num_nodes, num_edges,adj_list):
    file_name = f'{num_nodes}_{num_edges}_graph.txt'
    with open(file_name, 'w') as file:
        for edge in adj_list:
            file.write(f"{edge[0]} {edge[1]} {edge[2]}\n")
    
if __name__ == '__main__':
    num_nodes = int(input("Enter number of nodes: "))
    num_edges = int(input("Enter number of edges: "))
    weight = int(input("Enter weight of edges: "))

    adj_list = make_list(num_nodes, num_edges, weight)
    write_graph(num_nodes, num_edges, adj_list)
