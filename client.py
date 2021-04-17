import select
import socket
import pickle
import threading
import time
from transaction import Transaction
from blockchain_network import Blockchain

# global blockchain object
global_chain_object = Blockchain()

thread = None

TIMEOUT = 30  # seconds

CHAINREQUEST = -3
PEERREQUEST = -2
NEWPEER = -1

BLOCK = 1
TRSANSACTION = 2

INTITIAL_BALANCE = 50
MYPORT = -1


def sendData(port, message, type):
    global global_chain_object
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("localhost", port))
        dic = {'type': type, 'message': message}
        clientSocket.send(pickle.dumps(dic))
        clientSocket.close()
    except Exception as e:
        global_chain_object.removePeers(port)
        print(e)


def recvall(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def extractMessage(data):
    dic = pickle.loads(data)
    return dic['type'], dic['message']


def broadcast(message, type):
    global global_chain_object
    for port in global_chain_object.peers:
        if port != MYPORT:
            sendData(port, message, type)


def askPeers(firstPeer):
    global global_chain_object

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(("localhost", firstPeer))

        dic = {'type': PEERREQUEST, "message": MYPORT}
        clientSocket.send(pickle.dumps(dic))

        data = recvall(clientSocket)
        clientSocket.close()

        _, message = extractMessage(data)

        global_chain_object.addPeers(message)

    except Exception as e:
        clientSocket.close()
        print(e)


def askChain(peer):
    global global_chain_object

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect(("localhost", peer))

        dic = {'type': CHAINREQUEST, "message": MYPORT}
        clientSocket.send(pickle.dumps(dic))

        data = recvall(clientSocket)
        clientSocket.close()

        _, message = extractMessage(data)

        global_chain_object.replaceChain(message)

    except Exception as e:
        clientSocket.close()
        print(e)


def publish(answer):
    print("Solved Problem")

    T = threading.Thread(target=broadcast, args=(
        {'block': answer, 'port': MYPORT}, BLOCK,))
    T.setDaemon(True)
    T.start()


def counterDoubleSpend(dic, transaction):
    global global_chain_object
    if transaction['sender_public_key'] in dic:
        dic[transaction['sender_public_key']] = dic[transaction['sender_public_key']] - 1*transaction['amount']
    else: 
        dic[transaction['sender_public_key']] = -1*transaction['amount'] + global_chain_object.get_balance(transaction['sender_public_key']) + INTITIAL_BALANCE
        
    return dic[transaction['sender_public_key']]>=0


def worker():
    global global_chain_object
    global thread

    while len(global_chain_object.transactions) >= 2 and (not global_chain_object.isStopped):

        with threading.Lock():
            if(global_chain_object.transactions[0]['timestamp'] > global_chain_object.transactions[1]['timestamp']):
                temp = global_chain_object.transactions[0]
                global_chain_object.transactions[0] = global_chain_object.transactions[1]
                global_chain_object.transactions[1] = temp

            dic={}

            problem1 = global_chain_object.transactions[0]
            global_chain_object.transactions = global_chain_object.transactions[1:]

            if not counterDoubleSpend(dic,problem1):
                print("Insuficient balance")
                Transaction.printIt(problem1)
                continue

            if(problem1['timestamp'] < global_chain_object.maxTransactionTimeStamp):
                print("timestamp is less then " +
                      str(global_chain_object.maxTransactionTimeStamp))
                Transaction.printIt(problem1)
                continue

            problem2 = global_chain_object.transactions[0]
            global_chain_object.transactions = global_chain_object.transactions[1:]

            if not counterDoubleSpend(dic,problem2):
                print("Insuficient balance")
                Transaction.printIt(problem2)
                continue

            if(problem2['timestamp'] < global_chain_object.maxTransactionTimeStamp):
                print("timestamp is less then " +
                      str(global_chain_object.maxTransactionTimeStamp))
                Transaction.printIt(problem2)
                continue

        new_block = global_chain_object.mine([problem1, problem2], MYPORT)

        # block checking or insertion shuld  otbe done parallely
        with threading.Lock():
            if global_chain_object.isStopped:
                return
            else:
                # Appending new block to global blockchain
                global_chain_object.add_block(new_block)
                # publishing new block
                publish(new_block)


def startThread():
    global thread
    global global_chain_object

    global_chain_object.isStopped = True

    if thread != None:
        thread.join()

    thread = None

    # Atleast having two transactions in pool
    if len(global_chain_object.transactions) >= 2:
        global_chain_object.isStopped = False
        thread = threading.Thread(target=worker)
        thread.setDaemon(True)
        thread.start()


def stopThread():
    global global_chain_object
    global thread
    global_chain_object.isStopped = True


def handle_new_transaction(new_transaction):
    global global_chain_object
    global thread

    # self verifying
    if(new_transaction.verifyIt(global_chain_object)):
        with threading.Lock():
            global_chain_object.transactions.append(
                new_transaction.get_transaction_bill())
        startThread()
        return True

    return False


def handle_new_block(new_block, port):
    global global_chain_object

    # block checking or insertion shuld  otbe done parallely
    with threading.Lock():
        prev_block = global_chain_object.last_block_chain()
        prev_hash = global_chain_object.calculate_hash_of_block(
            prev_block)

        if(prev_block.index + 1 == new_block.index and prev_hash == new_block.previous_hash):
            stopThread()
            global_chain_object.add_block(new_block)

            print('\n  Valid Block is Mined By another miner \n')
            new_block.printIt()

        elif prev_block.index + 2 == new_block.index:
            askChain(port)

    startThread()  # this start thread function should not be kept under the lock


MYPORT = (int)(input("enter the alloted port number\n"))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', MYPORT)
print("binding up on port")
server.bind(server_address)
server.listen(10)


firstPeer = (int)(
    input("enter the port number of first peer or -1 if iam the first\n"))

if firstPeer != -1:
    global_chain_object.addPeers(firstPeer)
    askPeers(firstPeer)
    askChain(firstPeer)

print('Print 1 for transaction , 2 for last block, 3 for available transactions, 4 to get balance')

RUN = True
while RUN:
    # try:
    r, _, _ = select.select([server, 0], [], [], TIMEOUT)

    for fd in r:
        if fd == -1:
            print("Something Goes Wrong")
            RUN = False
            break

        if fd == 0:
            x = int(input())

            # Transaction
            if(x == 1):
                timestamp = time.time()
                sender_public_key = input('Enter sender public key\n')
                sender_private_key = input('Enter sender private key\n')
                amount = int(input('Enter amount\n'))
                recipient_public_key = input('Enter recipient_public_key \n')

                new_transaction = Transaction(
                    amount, sender_public_key, recipient_public_key, timestamp)
                new_transaction.sign_transaction(sender_private_key)

                if handle_new_transaction(new_transaction):

                    # broadcasting to all nodes
                    broadcast(new_transaction, TRSANSACTION)

                    print('Transaction Successfully Added and Broadcasted')
                else:
                    print('Wrong Transaction')

            # Get Last Block of Chain
            if(x == 2):
                print('\nLast Block of Chain is \n')
                global_chain_object.last_block_chain().printIt()

            # Available Transactions
            if(x == 3):
                if(len(global_chain_object.transactions) == 0):
                    print('\nNo due transactions are left\n')
                else:
                    for t in global_chain_object.transactions:
                        Transaction.printIt(t)

            if x == 4:
                public_key = input('Enter public key\n')
                print(
                    "Balance "+str(global_chain_object.get_balance(public_key) + INTITIAL_BALANCE)+'\n')

        else:
            connection, client_address = server.accept()

            data = recvall(connection)
            type, message = extractMessage(data)

            if type == PEERREQUEST:
                dic = {"type": "none", "message": global_chain_object.peers}
                connection.send(pickle.dumps(dic))

                if global_chain_object.addPeers(message):
                    broadcast(message, NEWPEER)

            elif type == CHAINREQUEST:
                dic = {"type": "none", "message": global_chain_object.chain}
                connection.send(pickle.dumps(dic))

            elif type == NEWPEER:
                global_chain_object.addPeers(message)

            elif type == TRSANSACTION:
                if handle_new_transaction(message):
                    print('Recieved new transaction... added to the pool')

            elif type == BLOCK:
                connection.close()  # its important
                handle_new_block(message['block'], message['port'])

            connection.close()
            # except Exception as e:

            #     connection.close()
            #     print(e)

    # except Exception as e:
    #     server.close()
    #     print(e)
    #     RUN = False
