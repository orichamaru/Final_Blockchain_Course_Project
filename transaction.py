from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import binascii
from blockchain_network import Blockchain


class Transaction:

    def __init__(self,sender_public_key=None,sender_private_key=None,amount=0,recipient_public_key=None):
        self.sender_public_key = sender_public_key
        self.sender_private_key = sender_private_key
        self.amount = amount
        self.recipient_public_key = recipient_public_key


    def get_transaction_bill(self):
        return OrderedDict({'sender_public_key':self.sender_public_key,
                            'recipient_public_key':self.recipient_public_key,
                            'amount':self.amount})


    def sign_transactions(self):
       
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        message = SHA.new(str(self.get_transaction_bill()).encode('utf8'))
        signature = binascii.hexlify(signer.sign(message)).decode('ascii')
        
        return signature

    def generate_transaction(self):
        
        if( self.sender_public_key != None 
            and self.sender_private_key !=None
            and self.amount !=0
            and self.recipient_public_key != None):

            digital_signature = self.sign_transactions()
            a = Blockchain()
            response = a.add_transaction(self.get_transaction_bill(),digital_signature)
            
            return response
         