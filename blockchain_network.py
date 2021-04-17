from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii
import hashlib
import json
from block import Block
import time

DIFFICULTY = 5


class Blockchain:

    def __init__(self):
        self.peers = []
        self.transactions = []
        self.chain = []
        self.isStopped = False
        self.maxTransactionTimeStamp = -1
        self.create_genesis_block()

    # Create Genesis Block
    def create_genesis_block(self):
        genesis_block = Block()
        self.chain.append(genesis_block)

    # Adding peer
    def addPeers(self, obj):
        if isinstance(obj, list):
            for k in obj:
                if isinstance(k, int) and k not in self.peers:
                    self.peers.append(k)

        elif isinstance(obj, int) and obj not in self.peers:
            self.peers.append(obj)
            return True

    def removePeer(self, obj):
        self.peers.remove(obj)

    def replaceChain(self, chain):
        if self.verify_chain(chain):
            self.chain = chain
            self.maxTransactionTimeStamp = -1
            for block in self.chain:
                for t in block.transactions:
                    self.maxTransactionTimeStamp = max(
                        self.maxTransactionTimeStamp, t['timestamp'])

    def verify_chain(self, chain):
        # verifyication of new chain should be done here
        return True

    def get_balance(self, pubKey):
        balance = 0
        for block in self.chain:
            for t in block.transactions:
                if t['sender_public_key'] == pubKey:
                    balance = balance - t['amount']
                if t['recipient_public_key'] == pubKey:
                    balance = balance + t['amount']
        return balance

    # Return last block

    def last_block_chain(self):
        return self.chain[-1]

    # Proof of work
    def proof_of_work(self, block):

        # block - block which needs to be added

        block.nonce = 0
        while not self.is_block_valid(block) and self.isStopped == False:
            block.nonce += 1

    # Calculate hash of block
    def calculate_hash_of_block(self, block):

        string_format_block = json.dumps(
            block.get_block_data(), sort_keys=True).encode()
        return hashlib.sha256(string_format_block).hexdigest()

    # Add transaction to blockchain network
    def verify_transaction(self, transaction, digital_signature):

        sender_public_key = transaction['sender_public_key']

        # If any other check you want to perform -----------------
        #Balance verification should be done prior
        available_balance = self.get_balance(sender_public_key)

        if(self.verify_signature(sender_public_key, transaction, digital_signature)):
            return True
        else:
            return False

    # Verifying transaction singature
    def verify_signature(self, sender_public_key, transaction, digital_signature):

        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        message = SHA.new(str(transaction).encode('utf8'))

        return verifier.verify(message, binascii.unhexlify(digital_signature))

    # Checking validity of block to be added
    def is_block_valid(self, block, difficulty=DIFFICULTY):

        # Calculate hash of block items

        block_hash = self.calculate_hash_of_block(block)

        return block_hash[:difficulty] == '0'*difficulty

    # Add block to blockchain network
    def add_block(self, block):
        self.chain.append(block)

        for t in block.transactions:
            self.maxTransactionTimeStamp = max(
                self.maxTransactionTimeStamp, t['timestamp'])

    # Mining of block
    def mine(self, transactions, minerId):

        prev_block = self.last_block_chain()
        prev_hash = self.calculate_hash_of_block(prev_block)

        # Creating new block
        new_block = Block(minerId)

        new_block.index = prev_block.index+1
        new_block.previous_hash = prev_hash

        # Coinbase transaction is also included
        # new_block.transactions = self.get_reward(self.available_transactions)   ## need to implement

        new_block.transactions = transactions
        new_block.timestamp = time.time()

        # Nounce is correctily calculated
        self.proof_of_work(new_block)

        # This valid block will be added to block chain
        return new_block
