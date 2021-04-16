from time import time
import json
import hashlib

class Block:

    def __init__(self,index=0,previous_hash=None,timestamp = 1618473245.5043766, transactions = [],nonce=0):
       self.index= index
       self.previous_hash = previous_hash
       self.timestamp = timestamp
       self.transactions = []
       self.nonce = nonce

    #Get block datagithub
    def get_block_data(self):
        data = {
                'index': self.index,
                'previous_hash': self.previous_hash,
                'timestamp': self.timestamp,
                'transactions': self.transactions,
                'nonce': self.nonce
               }
        return data


    