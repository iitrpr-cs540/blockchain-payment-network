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

class Transaction:
    stack: list[HTLCBid]
    current_node: str
    src: str
    dest: str
    amount: int
    network: Network
    hop_count: int
    tx_id: str

    def __init__(self, src, dest, amount, network: Network, id):
        self.stack = []
        self.current_node = src
        self.src = src
        self.dest = dest
        self.amount = amount
        self.network = network
        self.hop_count = 0
        self.tx_id: id

    def next_hop(self):
        if (self.network.notification(self.current_node, self.dest)):
            self.stack.append(HTLCBid(amount=self.amount, transaction_fee=0, security_deposit=0, hop_count=self.hop_count+1, src=self.current_node, dest=self.dest, tx_id=self.tx_id))
            self.network.node_probabilities[self.current_node].chosen(self.dest)
            return True, True
        else:
            try:
                bid = self.network.bidding(self.current_node, self.dest)
                self.stack.append(HTLCBid(amount=self.amount, transaction_fee=bid[0], security_deposit=self.network.alpha * bid[0], hop_count=self.hop_count+1, src=self.current_node, dest=bid[1], tx_id=self.tx_id))
                self.network.node_probabilities[self.current_node].chosen(bid[1])
                self.hop_count += 1
                self.current_node = bid[1]
                return True, False
            except ValueError as e:
                print(e)
                return False, None
        # returns hop_success, has_ended
        # when hop_success returns as false, run reject()
        # when hop_success returns true, true, run resolve()
        
    def resolve(self):
        while len(self.stack) > 0:
            bid = self.stack.pop()
            bid.resolve(self.network.payment_channels[self.tx_id], node_probabilities=self.network.node_probabilities[self.current_node])
        print(f"{self.network.env.now}: Transaction completed successfully.")

    def reject(self):
        while len(self.stack) > 0:
            bid = self.stack.pop()
            bid.reject(self.network.payment_channels[self.tx_id])
        print(f"{self.network.env.now}: Transaction failed to reach {self.dest} from {self.src}.")

    def execute_tx(self):
        hop_success, has_ended = self.next_hop()
        if not hop_success:
            self.reject()
            return
        while not has_ended:
            hop_success, has_ended = self.next_hop()
            if not hop_success:
                self.reject()
                return
        self.resolve()