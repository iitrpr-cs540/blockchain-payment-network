import numpy as np
import random
import argparse

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
    return file_name
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a graph and write it to a file.')
    parser.add_argument('--manual', action='store_true', help='Enter graph details manually')
    manual = parser.parse_args().manual

    num_nodes = int(input("Enter number of nodes: "))
    num_edges = int(input("Enter number of edges: "))
    weight = int(input("Enter weight of edges: "))

    adj_list = []
    if not manual:
        adj_list = make_list(num_nodes, num_edges, weight)
    else:
        nodes = [i for i in range(num_nodes)]
        print("Nodes: ", nodes)
        print("Enter edges in the format: node1 node2")
        for _ in range(num_edges):
            node1, node2 = input("Enter edge: ").split()
            adj_list.append([int(node1), int(node2), weight])
    file = write_graph(num_nodes, num_edges, adj_list)
    if manual:
        print(f"Graph written to {file}")
