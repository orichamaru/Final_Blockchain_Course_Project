from collections import OrderedDict
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import blockchain_network 
import binascii
import select
import socket
import pickle
import threading
import hashlib
import random
import time

#global blockchain object - available to all clients
global_chain_object = blockchain_network.Blockchain()

peerPorts = []
problems = []

currentProblemTime = -1
lastSolvedMaxTime = -2

TIMEOUT = 30  # seconds
DIFFICULTY = 5

PEERREQUEST = -2
NEWPEER = -1

SOLUTION = 1
PROBLEM = 2

MYPORT = -1

blockchain_network.isStop = False
global_previous_hash = ''
global_previous_index = 0

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
            local_block_object = blockchain_network.Blockchain()
            response = local_block_object.add_transaction(self.get_transaction_bill(),digital_signature)

            return response

def sendData(port, message, type):
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("localhost", port))
        dic = {'type': type, 'message': message}
        clientSocket.send(pickle.dumps(dic))
        clientSocket.close()
    except Exception as e:
        peerPorts.remove(port)
        print(e)


def extractMessage(data):
    dic = pickle.loads(data)
    return dic['type'], dic['message']


def broadcast(message, type):
    for port in peerPorts:
        sendData(port, message, type)


def askPeers(firstPeer):
    global global_chain_object

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(("localhost", firstPeer))

        dic = {'type': PEERREQUEST, "message": MYPORT}
        clientSocket.send(pickle.dumps(dic))

        data = clientSocket.recv(4096)
        clientSocket.close()

        _, message = extractMessage(data)
        for k in message['ports']:
            if k not in peerPorts and isinstance(k, int):
                peerPorts.append(k)
        
        global_chain_object = message['chain']

    except Exception as e:
        clientSocket.close()
        print(e)


def publish(answer):
    print("Solved Problem")
    # print(answer)

    T = threading.Thread(target=broadcast, args=(answer, SOLUTION,))
    T.setDaemon(True)
    T.start()


def worker():
    global lastSolvedMaxTime
    global global_previous_hash
    global global_previous_index
    global problems
    global global_chain_object
    global currentProblemTime

    while len(problems)>=2 and not blockchain_network.isStop:
        
        if(problems[0]['timestamp'] > problems[1]['timestamp']):
            temp = problems[0]
            problems[0] = problems[1]
            problems[1] = temp

        problem1 = problems[0] 
        problems = problems[1:]
    
        if(problem1['timestamp']<lastSolvedMaxTime):
            continue

        problem2 = problems[0]
        problems = problems[1:]
        
        if(problem2['timestamp']<lastSolvedMaxTime):
            continue
        
        # #dicscarding both last blocks
        # if (problem1['timestamp']  or problem2['timestamp']) < lastSolvedMaxTime:
        #     continue

        #Creating local block object of blockchain
        local_block_object = blockchain_network.Blockchain()
        local_block_object.available_transactions = []
        local_block_object.available_transactions.append(problem1)
        local_block_object.available_transactions.append(problem2)
        
        currentProblemTime = max(problem1['timestamp'],problem2['timestamp'])

        #Add timestamp
        # local_block_object.timestamp = currentProblemTime 
        
        # #Adding index and prev hash
        # local_block_object.previous_hash = global_previous_hash
        # local_block_object.index = global_previous_index+1

        # nonce = work(problem['statement'])
        new_block = local_block_object.mine()
        new_block.previous_hash = global_previous_hash
        new_block.index = global_previous_index+1
        new_block.timestamp = currentProblemTime 
        new_block.transactions = local_block_object.available_transactions

        if blockchain_network.isStop:
            return
        else:
            lastSolvedMaxTime = max(lastSolvedMaxTime, currentProblemTime)
            
            #Updating prev_hash, index
            global_previous_index = new_block.index+1
            global_previous_hash = local_block_object.calculate_hash_of_block(new_block)
           
            #Appending new block to global blockchain
            global_chain_object.add_block(new_block) 
            
            print('\n@@@@@@@@@New Block@@@@@@@')
            print('index : ',new_block.index)
            print('previous_hash : ',new_block.previous_hash)
            print('timestamp : ',new_block.timestamp)
            print('transactions : ' ,new_block.transactions)
            print('nonce : ',new_block.nonce)
            print('@@@@@@dONE@@@@@\n')
            
            publish(new_block)



            # publish({'statement': problem['statement'],
            #          'time': problem['time'], "nonce": nonce})

    thread = None


# def work(message):
#     p = 0
#     while not blockchain_network.isStop:
#         nonce = random.randint(0, 1000000)
#         hash = hashlib.sha256(
#             (message+str(nonce)).encode()).hexdigest()
#         if hash[:DIFFICULTY] == '0'*DIFFICULTY:
#             return nonce
#         p += 1

#         if p > 10000000:
#             return "fail"


thread = None

MYPORT = (int)(input("enter the alloted port number\n"))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)

server_address = ('localhost', MYPORT)
print("binding up on port")
server.bind(server_address)
server.listen(10)


firstPeer = (int)(
    input("enter the port number of first peer or -1 if iam the first\n"))

if firstPeer != -1:
    peerPorts.append(firstPeer)
    askPeers(firstPeer)

    # d = ProcessData("Test")
    # broadcast(d, 3)

RUN = True
while RUN:
    # try:
        r, _, _ = select.select([server, 0, ], [], [], TIMEOUT)

        for fd in r:
            if fd == -1:
                print("Something Goes Wrong")
                RUN = False
                break

            if fd == 0:

                print('Print 1 for transaction , 2 for mining, 3 for last block,4 for available transactions')
                x = int(input())

                #Transaction
                if(x==1):
                    sender_public_key = input('Enter sender public key\n')
                    sender_private_key = input('Enter sender private key\n')
                    amount = int(input('Enter amount\n'))
                    recipient_public_key = input('Enter recipient_public_key \n')
                    new_transaction = Transaction(sender_public_key,sender_private_key,amount,recipient_public_key)
                    
                    dic = new_transaction.get_transaction_bill()
                    dic['timestamp'] = time.time()

                    #self verifying
                    if(new_transaction.generate_transaction()):
                        
                        #broadcasting to all nodes
                        broadcast(dic,PROBLEM)
                        
                        problems.append(dic)
                 
                        if thread != None and (not thread.is_alive()):
                            thread = None
                   
                       #Atleast having three transactions in pool
                        if thread == None and len(problems)>=2:
                            blockchain_network.isStop = False
                            thread = threading.Thread(target=worker)
                            thread.setDaemon(True)
                            thread.start()               
                   
                        
                        print('Transaction Successfully Added and Broadcasted')
                    else:
                        print('Wrong Transaction')

                # #Mining
                # if(x==2):
                    
                #      #If there is available transaction
                #      if(len(problems)):
                          
                #           if thread != None and (not thread.is_alive()):
                #             thread = None

                #           if thread == None:
                #                 blockchain_network.isStop = False
                #                 thread = threading.Thread(target=worker)
                #                 thread.setDaemon(True)
                #                 thread.start()
                          
                #           new_block = block_object.mine()
                #           broadcast(new_block.get_block_data(),SOLUTION)

                #Get Last Block of Chain
                if(x==3):
                      print('\nLast Block of Chain is \n')
                      print(global_chain_object.last_block_chain().get_block_data())
                      print('\n')
                
                #Available Transactions
                if(x==4):
                    if(len(problems) == 0):
                        print('\nNo due transactions are left\n')
                    else:
                        for i in range(len(problems)):
                            trans = {}
                            trans['sender_public_key'] = problems[i]['sender_public_key']
                            trans['recipient_public_key'] = problems[i]['recipient_public_key']
                            trans['amount'] = problems[i]['amount']
                            print(trans)
               
                # statement = input()
                # th = time.time()

                # problem = {'statement': statement, "time": th}

                # problems.append(problem)

                # if thread != None and (not thread.is_alive()):
                #     thread = None

                # if thread == None:
                #     blockchain_network.isStop = False
                #     thread = threading.Thread(target=worker)
                #     thread.setDaemon(True)
                #     thread.start()

                # broadcast(problem, PROBLEM)

            else:

                    connection, client_address = server.accept()

                    data = connection.recv(4096)
                    type, message = extractMessage(data)
                    
                    if type == PEERREQUEST:
                        dic = {"type": "none", "message": {'ports':peerPorts,'chain':global_chain_object}}
                        connection.send(pickle.dumps(dic))

                        if message not in peerPorts and isinstance(message, int):
                            broadcast(message, NEWPEER)
                            peerPorts.append(message)

                    elif type == NEWPEER:
                        if message not in peerPorts and isinstance(message, int):
                            peerPorts.append(message)

                    elif type == SOLUTION:
                        print('\narfr\n')
                        print(currentProblemTime)
                        print('\n')

                        #verifying block to be added
                        prev_block = global_chain_object.last_block_chain()
                        prev_hash = global_chain_object.calculate_hash_of_block(prev_block)

                        if(prev_block.index + 1 == message.index and prev_hash == message.previous_hash):
                            print('\ncrrtr\n')
                            print("Recieved Solution")
                            print('index : ',message.index)
                            print('previous_hash : ',message.previous_hash)
                            print('timestamp : ',message.timestamp)
                            print('transactions : ' ,message.transactions)
                            print('nonce : ',message.nonce)
                            
                            print('\n  Valid Block is Mined By another miner \n')

                            blockchain_network.isStop = True
                            thread = None
                            lastSolvedMaxTime = max(
                                lastSolvedMaxTime, message['timestamp'])

                            if thread != None and (not thread.is_alive()):
                                thread = None

                            if len(problems)>=2:
                                blockchain_network.isStop = False
                                thread = threading.Thread(target=worker)
                                thread.setDaemon(True)
                                thread.start()
                            

                    elif type == PROBLEM:

                        problems.append(message)

                        if thread != None and (not thread.is_alive()):
                            thread = None
                   
                        #Atleast having three transactions in pool
                        if thread == None and len(problems)>=2:
                            blockchain_network.isStop = False
                            thread = threading.Thread(target=worker)
                            thread.setDaemon(True)
                            thread.start()               
                        

                    elif type == 3:
                        print(message.name)

                    connection.close()
                # except Exception as e:

                #     connection.close()
                #     print(e)

    # except Exception as e:
    #     server.close()
    #     print(e)
    #     RUN = False
