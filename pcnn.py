import networkx as nx
import numpy as np

class PCNN:

    def __init__(self):
        self.G = self.create_pcn_network()

    def create_pcn_network(self):
        G = nx.DiGraph()
        G.add_edge('A', 'B', balance=10, success_probability=0.3, preimage=None)
        G.add_edge('B', 'A', balance=10, success_probability=0.3, preimage=None)

        G.add_edge('B', 'C', balance=10, success_probability=0.5, preimage=None)
        G.add_edge('C', 'B', balance=10, success_probability=0.3, preimage=None)
        
        G.add_edge('C', 'D', balance=10, success_probability=0.8, preimage=None) 
        G.add_edge('D', 'C', balance=10, success_probability=0.3, preimage=None)
        return G
