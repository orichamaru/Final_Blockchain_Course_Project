from transaction import Transaction


class Block:
    def __init__(self,
                 difficulty,
                 minerId=-1,
                 index=0,
                 previous_hash=None,
                 timestamp=1618473245.5043766,
                 nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = []
        self.nonce = nonce
        self.minerId = minerId
        self.minedAt = timestamp
        self.difficulty = difficulty

    # Get block datagithub
    def get_block_data(self):
        data = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'nonce': self.nonce,
            'minerId': self.minerId,
            'difficulty': self.difficulty
        }
        return data

    def printIt(self):
        print('index : ', self.index)
        print('miner id : ', self.minerId)
        print('diificulty : ', self.difficulty)
        if self.previous_hash != None:
            print('previous_hash : ', self.previous_hash[-50:])
        print('timestamp : ', self.timestamp)
        print('transactions : ')
        for t in self.transactions:
            Transaction.printIt(t)
        print('nonce : ', self.nonce)
        print()
