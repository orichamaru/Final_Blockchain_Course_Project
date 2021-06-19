# Final Blockchain_Course_Project

## Implementation of Cryptocurrency using Blockchain from scratch

### Steps for installation

1. Clone this project using terminal or zip it.
2. Open folder containing this project and run terminal


### Assumptions

1. All users intially are provided with 50 tokens.
2. All nodes in network are hard nodes i.e they will can make transaction as well as mine a block.
3. Transaction fees rate is 5% will be dedcuted from your account and will be credited to miner account upon successful addition of block into  network.
4. For now upon addition of 2 transaction in transaction book, everyone starts mining.


![alt_text](https://tenor.com/view/baby-yoda-baby-yoda-happy-laughing-smile-happy-gif-16061896)

### Steps for Generation Key Pair to become valid user of network 

1. For transaction you need to have wallet i.e private and public key pair , to generated key pair run below command and enter your name
   '''
      python3 generate_wallet.py
   '''    
2. Your key pairs are saved in your wallet with your name
3. Now you have your key pair , then you are ready to make transaction in blockchain network :smile:


### Steps for getting connected to blockchain network

#### Creating blockchain network for first time
1. If network isn't created , then first run python3 client.py , add your port number and for first time connection(i.e for first node) enter -1.
2. Above step creates blockchain network.

#### Getting connected to existing blockchain network
1. Run ''' python3 client.py ''' , enter your port number.
2. For getting connected to network enter port number of any node which is connected in network.

![alt_text](https://tenor.com/view/surprise-chris-pratt-parks-and-recreation-parks-and-rec-shocked-gif-5571450)

### Operations available 

After getting connected to network you will be prompted with following options
1. Create transaction
2. Getting information of last block of network
3. Getting list of available transaction
4. Getting information about your wallet

![alt_text](https://tenor.com/view/im-ready-cat-sunglass-gif-13422464)

### Steps for making transaction blockchain network

1. After pressing 1,  you will be asked for your name to fetch your wallet credentials.(Enter same name which you have typed while wallet generation).
2. Then you, will be asked for reciever's name, enter his/her name.
3. After that you will be asked for transaction amount,
4. If all entries are legitimate, then your transaction will be recored in transaction book of every miner.
5. As soon as number of transactions are sufficient in transaction book , then upon successfull mining you will be notified accordingly.
6. Hurray your transaction is successfully added in network now :smile:


