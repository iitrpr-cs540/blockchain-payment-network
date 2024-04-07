import networkx as nx
import simpy
import numpy as np
import random
from htlc import HTLCBid

def create_pcn_network():
    G = nx.DiGraph()
    G.add_edge('A', 'B', balane=10, success_probability=0.3, preimage=None)
    G.add_edge('B', 'A', balane=10, success_probability=0.3, preimage=None)

    G.add_edge('B', 'C', balance=10, success_probability=0.5, preimage=None)
    G.add_edge('C', 'B', balane=10, success_probability=0.3, preimage=None)
    
    G.add_edge('C', 'D', balance=10, success_probability=0.8, preimage=None) 
    G.add_edge('D', 'C', balane=10, success_probability=0.3, preimage=None)
    return G

def example_distribution_F(pvi):
    return pvi

def calculate_bid(pvi, K, alpha):
    return (1 - example_distribution_F(pvi)) ** (K - 1) / (1 + alpha)

def notification(env, G, current_node, destination, amount, alpha):
    if destination in G.neighbors(current_node):
        # Assuming preimage is somehow retrieved or validated here
        print(f"{env.now}: Direct connection to destination {destination} from {current_node}. Transaction successful.")
        return True, "preimage"  # Simplification for demonstration
    else:
        bids = bidding(G, current_node, amount, alpha)
        if bids:
            success, preimage = outsourcing(env, G, current_node, destination, amount, alpha, bids)
            return success, preimage
        else:
            print(f"{env.now}: No bids received by {current_node}. Transaction failed.")
            return False, None


def bidding(G, node, amount, alpha):
    neighbors = list(G.successors(node))
    K = len(neighbors)
    bids = []
    for neighbor in neighbors:
        edge_data = G[node][neighbor]
        pvi = edge_data['success_probability']
        bid_value = calculate_bid(pvi, K, alpha)
        security_deposit = alpha * bid_value
        lock_time = 5
        transfer_time = 10
        htlc_bid = HTLCBid(amount=amount, transaction_fee=bid_value, security_deposit=security_deposit, lock_time=lock_time, transfer_time=transfer_time, bid_id=f'{node}-{neighbor}')
        bids.append((bid_value, neighbor, htlc_bid))
    return bids



def outsourcing(env, G, current_node, destination, amount, alpha, bids):
    best_bid, best_neighbor, best_htlc_bid = min(bids, key=lambda x: x[0])
    print(f"{env.now}: Node {current_node} selects Node {best_neighbor} with bid {best_bid}")
    best_htlc_bid.lock() 
    success, preimage = notification(env, G, best_neighbor, destination, amount, alpha)
    return success, preimage




def simulate_transaction(env, G, source, destination, amount, alpha):
    success, preimage = notification(env, G, source, destination, amount, alpha)
    yield env.timeout(1)
    if success:
        print(f"{env.now}: Transaction completed successfully.")
    else:
        print(f"{env.now}: Transaction failed to reach {destination} from {source}.")



env = simpy.Environment()
pcn_network = create_pcn_network()
alpha = 0.1  # Example security deposit ratio
env.process(simulate_transaction(env, pcn_network, 'A', 'D', 100, alpha))
env.run()
