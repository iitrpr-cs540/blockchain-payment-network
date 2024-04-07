# Create an excrow class between two nodes for locking money on a blockchain network and releasing it when the transaction is successful.
class Escrow:
    def __init__(self, proposer, signatory, amount, time_to_expire):
        self.proposer = proposer
        self.signatory = signatory
        self.amount = amount
        self.time_to_expire = time_to_expire
        self.state = 'open'

    def lock(self):
        self.state = 'locked'

    def unlock(self):
        self.state = 'completed'