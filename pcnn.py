import networkx as nx
import numpy as np

########### TOGGLE THIS VARIABLE TO SWITCH BETWEEN ADDITIVE AND MULTIPLICATIVE INCREMENT ###########
additive_incerment = True
######################################################################################################

class NodeProbabilities:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.success_count = {}
        self.total_count = {}

    def get_probability(self, destination: str) -> float:
        if destination not in self.total_count or self.total_count[destination] == 0:
            return 0.5  # 50% success probability if no transactions have occurred
        return self.success_count.get(destination, 0) / self.total_count[destination]

    def update_probabilities(self, destination: str, success: bool):
        if destination not in self.total_count:
            self.total_count[destination] = 20
            self.success_count[destination] = 10
        
        if additive_incerment: 
            self.total_count[destination] += 1
            if success:
                self.success_count[destination] += 1
        else:
            self.total_count[destination]  *= 1.1
            if success:
                self.success_count[destination] *=1.21


class PCNN:
    def __init__(self):
        self.G = nx.DiGraph()
        self.payment_channels = {}
        self.node_probabilities = {}

    def add_payment_channel(self, source: str, destination: str, deposit: int):
        channel_id = "-".join(sorted([source, destination]))
        print("Adding channel", channel_id)
        if channel_id in self.payment_channels:
            print("Channel already exists")
            return
        
        self.payment_channels[channel_id] = {
            source: deposit,
            destination: deposit
        }

        self.G.add_edge(destination, source)
        self.G.add_edge(source, destination)

        if source not in self.node_probabilities:
            self.node_probabilities[source] = NodeProbabilities(source)
        if destination not in self.node_probabilities:
            self.node_probabilities[destination] = NodeProbabilities(destination)
        
    def get_probability(self, source: str, destination: str) -> float:
        if source in self.node_probabilities:
            return self.node_probabilities[source].get_probability(destination)
        else:
            raise ValueError(f"No record for node {source}")
        
    def update_transaction_success(self, source: str, destination: str, success: bool):
        if source in self.node_probabilities:
            self.node_probabilities[source].update_probabilities(destination, success)
        else:
            print(f"No probability record for node {source}")

    def get_bid_for_node(self, node, destination) -> float:
        # (1 - prob)^(K-1)
        return (1 - self.node_probabilities[node].get_probability(destination)) ** (len(self.G.successors(node)) - 1)