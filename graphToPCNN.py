import os
from pcnn import PCNN
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(adj_list):
    G = nx.Graph()
    for edge in adj_list:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show(block=False)
    plt.pause(0.005)

def read_graph(file_path):
    adj_list = []
    with open(file_path, 'r') as file:
        for line in file:
            edge = line.split()
            adj_list.append((int(edge[0]), int(edge[1]), float(edge[2])))
    
    print("Graph read successfully.")
    return adj_list


def buildPCNN(adj_list):
    # remove duplicate from adj_list if any
    adj_list = list(set(adj_list))
    pcnn = PCNN()
    for edge in adj_list:
        pcnn.add_payment_channel(source=str(edge[0]), destination=str(edge[1]), deposit=edge[2])
    print("PCNN created successfully.")
    return pcnn

def generate_PCNN_from_graph(num_nodes, num_edges):
    try:
        file_path = f'./graphs/{num_nodes}_{num_edges}_graph.txt'
        # chech if file exists
        if not os.path.exists(file_path):
            print("File does not exist.")
            return
        adj_list = read_graph(file_path)

        draw_graph(adj_list) # uncomment to draw the graph

        pcnn = buildPCNN(adj_list)
        return pcnn
    except Exception as e:
        print("An error occurred:", str(e))
