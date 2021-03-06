from Crypto.PublicKey import RSA
from Crypto import Random
import binascii


class Wallet:

    def __init__(self, name=''):
        self.public_key = ''
        self.private_key = ''
        self.name = name

    def generate_keys(self):
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        private, public = key, key.publickey()

        self.private_key = binascii.hexlify(
            private.exportKey(format='DER')).decode('ascii')
        self.public_key = binascii.hexlify(
            public.exportKey(format='DER')).decode('ascii')

    def get_keys(self):

        self.generate_keys()

        private = open(self.name + "_private.txt", "w")
        public = open(self.name + "_public.txt", "w")

        private.write(self.private_key)
        private.close()

        public.write(self.public_key)
        public.close()

    def import_key(self):

        private = open(self.name + "_private.txt", "r")
        self.private_key = private.readline()

        public = open(self.name + "_public.txt", "r")
        self.public_key = public.readline()

    def generate_recipient_key(self, name):

        public_key = open(name + "_public.txt", "r")
        recipient_public_key = public_key.readline()

        return recipient_public_key


if __name__ == "__main__":
    name = input("Enter Your name\n")
    Wallet(name).get_keys()
