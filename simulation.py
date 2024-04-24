import time
from graphToPCNN import generate_PCNN_from_graph
from htlc import HTLCBid
from pcnn import PCNN
import pandas as pd

def example_distribution_F(pvi):
    return pvi

def calculate_bid(pvi, K, alpha):
    return (1 - example_distribution_F(pvi)) ** (K - 1) / (1 + alpha)

def notification(pcnn, current_node, destination, amount, alpha, selected_bids_dict, stats):
    if destination in pcnn.G.neighbors(current_node):
        print(f"Direct connection to destination {destination} from {current_node}. Transaction successful.")
        # Remove the htlcs from selected_bids_dict one by one starting from last index
        for htlc_bid in selected_bids_dict[::-1]:
            htlc_bid.resolve(pcnn.payment_channels)
            pcnn.update_transaction_success(htlc_bid.src, destination, True)
            stats['propability_updates'] += 1
        return True; 
    else:
        stats['total_bidding'] += 1
        bids = bidding(pcnn, current_node, destination, amount, alpha)
        if bids:
            stats['total_outsourcing'] += 1
            success= outsourcing(pcnn, current_node, destination, amount, alpha, bids, selected_bids_dict, stats)
            return success
        else:
            print(f"No bids received by {current_node}. Transaction failed.")
            for htlc_bid in selected_bids_dict[::-1]:
                htlc_bid.reject(pcnn.payment_channels)
                pcnn.update_transaction_success(htlc_bid.src, destination, False)
                stats['propability_updates'] += 1
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
        max_hop_count = pcnn.G.number_of_nodes()
        htlc_bid = HTLCBid(amount=amount, transaction_fee=bid_value, security_deposit=security_deposit, src=node,dest=neighbor, max_hop_count=max_hop_count)
        bids.append((bid_value, neighbor, htlc_bid))
    return bids

def outsourcing(pcnn, current_node, destination, amount, alpha, bids, selected_bids_dict, stats):
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
            stats['propability_updates'] += 1
            # print("Debug", current_node, pcnn.node_probabilities[current_node].success_count[destination], pcnn.node_probabilities[current_node].total_count[destination])
            # remove last entry from selected_bids_dict
            selected_bids_dict[-1].reject(pcnn.payment_channels)
            stats['failed_transactions'] += 1
            selected_bids_dict.pop()
            return notification(pcnn,selected_bids_dict[-1].dest, destination, amount, alpha, selected_bids_dict=selected_bids_dict, stats = stats)
    print(f"Node {current_node} selects Node {best_neighbor} with bid {best_bid}")
    selected_bids_dict.append(best_htlc_bid)
    # for each entry in selected_bids_dict we check if hop count has excedded the max_hop_count
    for htlc_bid in selected_bids_dict:
        # hops is total length is the selected_bids_dict- index of the current htlc_bid
        hops = len(selected_bids_dict)-selected_bids_dict.index(htlc_bid)
        if hops >= htlc_bid.max_hop_count:
            # remove all bids from this index to the end of the list
            for i in range(selected_bids_dict.index(htlc_bid), len(selected_bids_dict)):
                selected_bids_dict[i].reject(pcnn.payment_channels)
                pcnn.update_transaction_success(selected_bids_dict[i].src, destination, False)
                stats['propability_updates'] += 1
            selected_bids_dict = selected_bids_dict[:selected_bids_dict.index(htlc_bid)]
            # htlc_bid.reject(pcnn.payment_channels)
            # pcnn.update_transaction_success(htlc_bid.dest, destination, False)
            print(f"Transaction failed to reach {destination} from {current_node}.")
            print("Transaction failed due to hop count.")
            return notification(pcnn, htlc_bid.src, destination, amount, alpha, selected_bids_dict=selected_bids_dict, stats = stats)
        
    # print notifying the next node that is best_neighbor
    print(f"Notifying {best_neighbor} about the transaction.")
    success = notification(pcnn, best_neighbor, destination, amount, alpha, selected_bids_dict=selected_bids_dict, stats = stats)
    return success

def simulate_transaction(pcnn, source, destination, amount, alpha, selected_bids_dict, stats):
    success = notification(pcnn, source, destination, amount, alpha, selected_bids_dict, stats)
    if success:
        print("Transaction completed successfully.")
    else:
        print(f"Transaction failed to reach {destination} from {source}.")
    return success


def run():
    results = []

    num_nodes = [x*4 for x in range(1, 201, 1)]
    num_edges = [2*n - 2 for n in num_nodes]  # sparse graph

    for i in range(len(num_nodes)):
        # stats variables
        stats = {
            'total_bidding': 0,
            'total_outsourcing': 0,
            'propability_updates': 0,
            'failed_transactions': 0,
        }

        # generate PCNN
        pcnn = generate_PCNN_from_graph(num_nodes[i], num_edges[i])
        if pcnn is None:
            print("Error in generating PCNN: ", num_nodes[i], num_edges[i])
            continue
        alpha = 0.1
        selected_bids_dict = []
        print("Enter source and destination nodes for transaction.")

        ## FOR MANUAL INPUT
        # source = input("Enter source node: ")
        # destination = input("Enter destination node: ")
        # amount = float(input("Enter amount to be transferred: "))

        source = '0'
        destination  = str(num_nodes[i]-1)
        amount = 9*num_nodes[i]

        try:
            time_before = time.time()
            success = simulate_transaction(pcnn, source, destination, amount, alpha, selected_bids_dict, stats)
            time_after = time.time()    
            results.append([num_nodes[i], num_edges[i], source, destination, amount, time_after - time_before, success, stats['total_bidding'], stats['total_outsourcing'], stats['propability_updates'], stats['failed_transactions']])
        except Exception as e:
            print("An error occurred:", str(e))

    df = pd.DataFrame(results, columns=['num_nodes', 'num_edges', 'source', 'destination', 'amount', 'time', 'success', 'total_bidding', 'total_outsourcing', 'propability_updates', 'failed_transactions'])
    return df

if __name__ == '__main__':
    df = run()
    df.to_csv('results_multiplicative_increment.csv', index=False)




