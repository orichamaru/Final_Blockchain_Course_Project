from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import binascii

class Wallet:
     
     def __init__(self,name=''):
         self.public_key = ''
         self.private_key = ''
         self.name = name
     
     def generate_keys(self):
          random_generator = Random.new().read
          key = RSA.generate(1024, random_generator)
          private, public = key, key.publickey()
          
          self.private_key = binascii.hexlify(private.exportKey(format='DER')).decode('ascii')
          self.public_key = binascii.hexlify(public.exportKey(format='DER')).decode('ascii')

          return self.private_key, self.public_key


     def get_keys(self):
         
         private_key,public_key = self.generate_keys()

         private = open(self.name + "_private.txt","w")
         public = open(self.name + "_public.txt","w")

         private.write(private_key)
         private.close()

         public.write(public_key)
         public.close()         

    
     def import_key(self):
          
         private = open(self.name + "_private.txt","r")
         self.private_key = private.readline()

         public = open(self.name + "_public.txt","r")
         self.public_key = public.readline()

         
         
        #    private_key = RSA.importKey(fileContent) 
        #  self.private_key = RSA.importKey(file.readLines())

        #  public = self.name + "_public.pem"
        #  self.public_key = RSA.importKey(open(public, "rb").decode('UTF-8'))
         

        #  print('\n\n',self.private_key.exportKey())

# message = b'Hello'
# cipher = PKCS1_OAEP.new(public)
# print(b64encode(cipher.encrypt(message)))



# random_generator = Random.new().read
# key = RSA.generate(1024, random_generator)
# pub_key = key.publickey()

# self.public_key = binascii.hexlify(key.exportKey(format='DER')).decode('ascii')
# self.private_key = binascii.hexlify(pub_key.exportKey(format='DER')).decode('ascii')

# return self.public_key,self.private_key