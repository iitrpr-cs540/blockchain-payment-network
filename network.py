from pcnn import PCNN
from htlc import HTLCBid

class Network(PCNN):
    # bids structure: transaction_id: {payement_channel_id: HTLCBid}
    bids: dict[str, dict[str, HTLCBid]]

    def __init__(self, alpha):
        super().__init__()
        self.alpha = alpha
        self.bids = {}

    def notification(self, current_node, destination):
        if destination in self.G.neighbors(current_node):
            print(f"{self.env.now}: Direct connection to destination {destination} from {current_node}. Transaction successful.")
            return True
        else:
            return False

    def bidding(self, node, destination) -> tuple[float, str]:
        neighbors = list(self.G.successors(node))
        bid_value = []
        for neighbor in neighbors:
            bid_value.append([self.get_bid_for_node(node, destination), neighbor])
        min_bid = min(bid_value, key=lambda x: x[0])
        return min_bid
