import networkx as nx
import simpy
import numpy as np
import random



class HTLCBid:
    def __init__(self, amount, security_deposit, lock_time, transfer_time, bid_id, state='open'):
        self.amount = amount
        self.security_deposit = security_deposit
        self.lock_time = lock_time
        self.transfer_time = transfer_time
        self.bid_id = bid_id
        self.state = state  # 'open', 'locked', 'completed', 'failed'

    def lock(self):
        self.state = 'locked'

    def unlock(self, success=True):
        if success:
            self.state = 'completed'
        else:
            self.state = 'failed'


def create_pcn_network():
    G = nx.DiGraph()
    G.add_edge('A', 'B', capacity=10, fee=0.1, deposit=0.01, success_probability=0.9)
    G.add_edge('B', 'C', capacity=10, fee=0.1, deposit=0.01, success_probability=0.95)
    G.add_edge('C', 'D', capacity=10, fee=0.1, deposit=0.01, success_probability=0.98)
    return G

def example_distribution_F(pvi):
    return pvi

def calculate_bid(pvi, K, alpha):
    return (1 - example_distribution_F(pvi)) ** (K - 1) / (1 + alpha)

def bidding(env, G, node, amount, alpha):
    neighbors = list(G.successors(node))
    K = len(neighbors)
    bids = []
    for neighbor in neighbors:
        edge_data = G[node][neighbor]
        pvi = edge_data['success_probability']
        bid_value = calculate_bid(pvi, K, alpha)
        # Create an HTLC-bid object for each bid
        htlc_bid = HTLCBid(amount=amount, security_deposit=alpha * bid_value, lock_time=5, transfer_time=10, bid_id=f'{node}-{neighbor}')
        bids.append((bid_value + edge_data['deposit'], neighbor, htlc_bid))
    return bids


def outsourcing(env, G, current_node, amount, alpha):
    bids = bidding(env, G, current_node, amount, alpha)
    best_bid, best_neighbor, best_htlc_bid = min(bids, key=lambda x: x[0])
    print(f"{env.now}: Node {current_node} selects Node {best_neighbor} with bid {best_bid}")
    best_htlc_bid.lock()  # Lock the HTLC-bid
    G[current_node][best_neighbor]['htlc'] = best_htlc_bid  # Store the HTLC-bid in the edge data
    return best_neighbor, best_htlc_bid



def simulate_transaction(env, G, source, destination, amount, alpha):
    current_node = source
    path = [(source, None)]  # Tuple of (node, HTLC-bid), None for the source node's HTLC
    print(f"Starting transaction from {source} to {destination} with amount {amount}")

    while current_node != destination:
        next_node, htlc_bid = outsourcing(env, G, current_node, amount, alpha)
        path.append((next_node, htlc_bid))
        current_node = next_node
        yield env.timeout(1)  # Simulate time for each step
    
    # Assuming transaction success for simplicity, unlock HTLC-bids accordingly
    for node, htlc_bid in path[1:]:  # Skip the first entry (source node)
        if htlc_bid:  # Check if HTLC-bid exists
            htlc_bid.unlock(success=True)
            print(f"{env.now}: HTLC-bid unlocked for {node}")

    # Update the network state for success here
    # Note: Implement the logic to handle and unlock HTLC-bids on transaction failure

