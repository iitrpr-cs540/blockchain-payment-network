import networkx as nx
import numpy as np

class NodeProbabilities:
    def __init__(self, node):
        self.node = node
        self.successes = {}

    def chosen(self, destination):
        if destination in self.successes:
            self.successes[destination]["chosen"] += 1
        else:
            self.successes[destination] = {"chosen": 1, "successes": 0}
    
    def get_probability(self, destination):
        if (destination in self.probabilities):
            return self.probabilities[destination]["successes"] / self.probabilities[destination]["chosen"]
        else:
            return 1
    
    def add_successes(self, destination):
        self.successes[destination]["successes"] += 1

class PCNN:
    G: nx.DiGraph
    node_probabilities: dict[str, NodeProbabilities] = {}
    payment_channels: dict[str, dict[str, int]]

    def __init__(self):
        self.G = G = nx.DiGraph()
        self.payment_channels = {}

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

        self.node_probabilities[source] = NodeProbabilities(source)
        self.node_probabilities[destination] = NodeProbabilities(destination)

    def get_bid_for_node(self, node, destination) -> float:
        # (1 - prob)^(K-1)
        return (1 - self.node_probabilities[node].get_probability(destination)) ** (len(self.G.successors(node)) - 1)