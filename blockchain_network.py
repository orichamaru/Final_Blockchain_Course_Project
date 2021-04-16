from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import binascii
import hashlib
import json
from time import time
from block import Block

global isStop
isStop = False

DIFFICULTY = 4

class Blockchain:

    def __init__(self):
        self.miner_nodes = set()
        self.available_transactions = []
        self.chain = []
        self.create_genesis_block()

    #Create Genesis Block
    def create_genesis_block(self):
        genesis_block  = Block()
        self.chain.append(genesis_block)

    #Adding Miner Nodes
    def create_miner_node(self,host,port):
        self.miner_nodes.add((host,self))
        #Return address of miner node created
        return (host,port)
    
    #Return all miner nodes
    def get_miner_node(self):
        return {'nodes' : list(self.miner_nodes)}
    
    #Return last block
    def last_block_chain(self):
        return self.chain[-1]
    
    #Proof of work
    def proof_of_work(self,block):
        
        #block - block which needs to be added
        #initially new block.nonce = 0 is set to 0 by defualt
        while not self.is_block_valid(block) and isStop==False:
            block.nonce+=1  
    
    #Calculate hash of block
    def calculate_hash_of_block(self,block):
       
        string_format_block = json.dumps(block.get_block_data(), sort_keys=True).encode()
        return hashlib.sha256(string_format_block).hexdigest()
    
    #Add transaction to blockchain network
    def add_transaction(self,transaction,digital_signature):
       
        sender_public_key = transaction['sender_public_key']
        recipient_public_key = transaction['recipient_public_key']
        amount = transaction['amount']

        if(self.verify_transactions(sender_public_key, transaction, digital_signature)):
            self.available_transactions.append(transaction)
            return True
        else:
            return False

    #Verifying transaction before adding to blockchain network
    def verify_transactions(self,sender_public_key,transaction,digital_signature):
           
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        message = SHA.new(str(transaction).encode('utf8'))

        return verifier.verify(message, binascii.unhexlify(digital_signature))


    #Checking validity of block to be added
    def is_block_valid(self,block,difficulty=DIFFICULTY):
        
        #Calculate hash of block items

        block_hash = self.calculate_hash_of_block(block)
        
        return block_hash[:difficulty] == '0'*difficulty
    
    #Add block to blockchain network
    def add_block(self,block):
        self.chain.append(block)

    #Mining of block
    def mine(self):

        prev_block = self.last_block_chain()
        prev_hash =  self.calculate_hash_of_block(prev_block)

        #Creating new block
        new_block = Block()

        # new_block.index = prev_block.index+1
        # new_block.previous_hash = prev_hash

        #Coinbase transaction is also included
        # new_block.transactions = self.get_reward(self.available_transactions)
        # new_block.transactions = self.available_transactions
        # new_block.timestamp = time()

        #Nounce is correctily calculated
        self.proof_of_work(new_block)
 
        #This valid block will be added to block chain
        # self.add_block(new_block)
        return new_block
        



    
   