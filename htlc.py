class HTLCBid:
    def __init__(self, amount, transaction_fee,security_deposit, lock_time, transfer_time, bid_id, state='open'):
        self.amount = amount
        self.transaction_fee = transaction_fee
        self.security_deposit = security_deposit
        self.lock_time = lock_time
        self.transfer_time = transfer_time
        self.bid_id = bid_id
        self.state = state

    def lock(self):
        self.state = 'locked'

    def unlock(self, success=True):
        if success:
            self.state = 'completed'
        else:
            # Logic to handle security deposits on failure
            self.state = 'failed'