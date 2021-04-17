from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import binascii
import time

# this class required to work on to make transactions more significant
class Transaction:

    def __init__(self,  amount=0, sender_public_key=None, recipient_public_key=None, timestamp=time.time()):
        self.amount = amount
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.timestamp = timestamp
        self.signautre = None

    def get_transaction_bill(self):
        return OrderedDict({'sender_public_key': self.sender_public_key,
                            'recipient_public_key': self.recipient_public_key,
                            'amount': self.amount,
                            'timestamp': self.timestamp
                            })

    def sign_transaction(self, sender_private_key):

        private_key = RSA.importKey(
            binascii.unhexlify(sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        message = SHA.new(str(self.get_transaction_bill()).encode('utf8'))
        self.signature = binascii.hexlify(signer.sign(message)).decode('ascii')

    def verifyIt(self, blockchain):

        if(self.sender_public_key != None
                and self.signature != None
                and self.amount > 0
                and self.recipient_public_key != None):

            response = blockchain.verify_transaction(
                self.get_transaction_bill(), self.signature)

            return response
        else:
            return False

    @staticmethod
    def printIt(transaction):
        if isinstance(transaction, Transaction):
            transaction = transaction.get_transaction_bill()

        print('amount : ', transaction['amount'])
        print('sender : ', transaction['sender_public_key'][-50:])
        print('reciever : ', transaction['recipient_public_key'][-50:])
        print('timestamp : ', transaction['timestamp'])
        print()
