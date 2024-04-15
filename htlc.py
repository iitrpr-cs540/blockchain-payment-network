from pcnn import PCNN, NodeProbabilities
class HTLCBid:
    def __init__(self, amount, transaction_fee, security_deposit, src, dest, max_hop_count):

        self.amount = amount
        self.transaction_fee = transaction_fee
        self.security_deposit = security_deposit
        self.src = src
        self.dest = dest
        self.max_hop_count = max_hop_count
        self.state = "locked"

    def resolve(self, payment_channel):
        self.state = 'completed'
        channel_id = "-".join(sorted([self.src, self.dest]))
        payment_channel[channel_id][self.src] -= self.amount+self.transaction_fee
        payment_channel[channel_id][self.dest] += self.amount+self.transaction_fee

    def reject(self, payment_channel):
        self.state = 'rejected'
        channel_id = "-".join(sorted([self.src, self.dest]))
        payment_channel[channel_id][self.src] -= self.security_deposit
        payment_channel[channel_id][self.dest] += self.security_deposit