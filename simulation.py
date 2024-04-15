import simpy
from htlc import HTLCBid
from pcnn import PCNN

def example_distribution_F(pvi):
    return pvi

def calculate_bid(pvi, K, alpha):
    return (1 - example_distribution_F(pvi)) ** (K - 1) / (1 + alpha)

def notification(pcnn, current_node, destination, amount, alpha, selected_bids_dict):
    if destination in pcnn.G.neighbors(current_node):
        print(f"Direct connection to destination {destination} from {current_node}. Transaction successful.")
        # Remove the htlcs from selected_bids_dict one by one starting from last index
        for htlc_bid in selected_bids_dict[::-1]:
            htlc_bid.resolve(pcnn.payment_channels)
            pcnn.update_transaction_success(htlc_bid.src, destination, True)
        return True; 
    else:
        bids = bidding(pcnn, current_node, destination, amount, alpha)
        if bids:
            success= outsourcing(pcnn, current_node, destination, amount, alpha, bids, selected_bids_dict)
            return success
        else:
            print(f"No bids received by {current_node}. Transaction failed.")
            return False


def bidding(pcnn, node, destination, amount, alpha):
    neighbors = list(pcnn.G.successors(node))
    K = len(neighbors)
    bids = []
    for neighbor in neighbors:
        pvi = pcnn.get_probability(neighbor, destination)
        # print("Debug", node, destination, pvi)
        if(pvi<0.2):
            continue
        bid_value = calculate_bid(pvi, K, alpha)
        security_deposit = alpha * bid_value
        htlc_bid = HTLCBid(amount=amount, transaction_fee=bid_value, security_deposit=security_deposit, src=node,dest=neighbor, max_hop_count=5)
        bids.append((bid_value, neighbor, htlc_bid))
    return bids

def outsourcing(pcnn, current_node, destination, amount, alpha, bids, selected_bids_dict):
    # sort the bids in ascending order of bid_value
    bids.sort(key=lambda x: x[0])
    # print("Debug ", bids)
    best_bid, best_neighbor, best_htlc_bid = bids[0]
    # Check if best neigbor is already in selected_bids_dict
    while (best_neighbor in [htlc_bid.src for htlc_bid in selected_bids_dict]):
        if(len(bids)>1):
            # print("Debug", bids)
            bids.remove((best_bid, best_neighbor, best_htlc_bid))
            # print("Debug", bids)
            best_bid, best_neighbor, best_htlc_bid = bids[0]
            # print(best_bid, best_neighbor, best_htlc_bid, current_node)
        else:
            # Print transaction failed to reach destination
            print(f"Transaction failed to reached {destination} from {current_node}.")
            print("Transaction failed due to wrong path. Updating Probabilities.")
            pcnn.update_transaction_success(current_node, destination, False)
            # print("Debug", current_node, pcnn.node_probabilities[current_node].success_count[destination], pcnn.node_probabilities[current_node].total_count[destination])
            # remove last entry from selected_bids_dict
            selected_bids_dict.pop()
            return notification(pcnn,selected_bids_dict[-1].dest, destination, amount, alpha, selected_bids_dict=selected_bids_dict)
    print(f"Node {current_node} selects Node {best_neighbor} with bid {best_bid}")
    selected_bids_dict.append(best_htlc_bid)
    # for each entry in selected_bids_dict we check if hop count has excedded the max_hop_count
    for htlc_bid in selected_bids_dict:
        # hops is total length is the selected_bids_dict- index of the current htlc_bid
        hops = len(selected_bids_dict)-selected_bids_dict.index(htlc_bid)
        if hops >= htlc_bid.max_hop_count:
            # remove all bids from this index to the end of the list
            selected_bids_dict = selected_bids_dict[:selected_bids_dict.index(htlc_bid)]
            htlc_bid.reject(pcnn.payment_channels)
            pcnn.update_transaction_success(htlc_bid.dest, destination, False)
            print(f"Transaction failed to reach {destination} from {current_node}.")
            print("Transaction failed due to hop count.")
            return notification(pcnn, htlc_bid.src, destination, amount, alpha, selected_bids_dict=selected_bids_dict)
        
    # print notifying the next node that is best_neighbor
    print(f"Notifying {best_neighbor} about the transaction.")
    success = notification(pcnn, best_neighbor, destination, amount, alpha, selected_bids_dict=selected_bids_dict)
    return success

def simulate_transaction(pcnn, source, destination, amount, alpha, selected_bids_dict):
    success = notification(pcnn, source, destination, amount, alpha, selected_bids_dict)
    if success:
        print("Transaction completed successfully.")
    else:
        print(f"Transaction failed to reach {destination} from {source}.")



pcnn = PCNN()

# Create a simple network with 6 nodes and some edges
pcnn.add_payment_channel('A', 'B', deposit=10)
pcnn.add_payment_channel('A', 'C', deposit=10)
pcnn.add_payment_channel('B', 'D', deposit=10)
pcnn.add_payment_channel('C', 'D', deposit=10)
pcnn.add_payment_channel('D', 'E', deposit=10)
pcnn.add_payment_channel('E', 'F', deposit=10)
pcnn.add_payment_channel('C', 'G', deposit=10)

alpha = 0.1
selected_bids_dict = []

simulate_transaction(pcnn, 'A', 'F', 10, alpha, selected_bids_dict)



