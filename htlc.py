from pcnn import PCNN, NodeProbabilities

MAX_HOP = 5
class HTLCBid:
    def __init__(self, amount, transaction_fee, security_deposit, hop_count, src, dest, tx_id):
        if hop_count > MAX_HOP:
            raise ValueError("Hop count exceeds maximum allowed")

        self.amount = amount
        self.transaction_fee = transaction_fee
        self.security_deposit = security_deposit
        self.hop_count = hop_count
        self.state = "locked"
        self.src = src
        self.dest = dest
        self.tx_id = tx_id

    def resolve(self, payment_channel, node_probabilities: NodeProbabilities):
        self.state = 'completed'
        payment_channel[self.src] -= self.amount + self.transaction_fee
        payment_channel[self.dest] += self.amount + self.transaction_fee
        node_probabilities[self.src].add_successes(self.dest)

    def reject(self, payment_channel):
        self.state = 'rejected'
        payment_channel[self.src] += self.security_deposit
        payment_channel[self.dest] -= self.security_deposit