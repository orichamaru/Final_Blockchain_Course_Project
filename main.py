# from generate_wallet import Wallet
from blockchain_network import Blockchain
from transaction import Transaction


print('\n @@@@@@@@@@    Enter Operation Type   @@@@@@@@@@@ \n')

# a=Blockchain()
# print(a.last_block_chain().get_block_data())
# a.mine()
# print(a.last_block_chain().get_block_data())


# while(x!=2 or x!=1):

#     print('\n1 - Generate Wallet \n')
#     print('\n2-  Import Wallet \n')

#     x  = int(input())

#     if(x==1):
#         print('Enter Username\n')
#         name = input()
#         wallet = Wallet(name)
#         wallet.get_keys()
#         print('\n\n@@@@@@@@@    Wallet is successfully created   @@@@@@@@@@')
#         break
            
#     elif(x==2):
#         print('Enter Username\n')
#         name = input()
#         wallet = Wallet(name)
#         wallet.import_key()
#         print('\n\n@@@@@@@@@@   Keys are successfully fetched  @@@@@@@@@')
#         break

#     else:
#         print('Wrong Operation')
    


#For transaction enter folllowing 
sender_public_key = '30819f300d06092a864886f70d010101050003818d0030818902818100ab5a50c296ceded77bca8d04d12339f993114cfb6bcc708ffe8c11dc5dab3af76b195669b9885ea00509c22a9275dc00906cfe95833dbbb6b8f9bfd62a30c3a4d5b758b3207222ee4ee0a5012d6d24ea1181f56a2b00ef6b5cd578f28b92cda8edb9d03ab72a2e00ef3c2bbbaae2e0b08d5e6959d99d84cc4511995be60f577b0203010001'
sender_private_key = '3082025c02010002818100ab5a50c296ceded77bca8d04d12339f993114cfb6bcc708ffe8c11dc5dab3af76b195669b9885ea00509c22a9275dc00906cfe95833dbbb6b8f9bfd62a30c3a4d5b758b3207222ee4ee0a5012d6d24ea1181f56a2b00ef6b5cd578f28b92cda8edb9d03ab72a2e00ef3c2bbbaae2e0b08d5e6959d99d84cc4511995be60f577b02030100010281806a1d07104a26181827a01ace55d953c8bb8ba639b8db2505f723b4d7dbe5f3214f60a483da9299ceccefeb1f440ddacd3aa354d1303225b215410ccccad9e1fd8932c5f613e6e1eac669dd255567ce72811e85fd1abe440fbfdab2bda78dce6329fb7755588315c5e3327e239a9cdbf0efbbf0b4e104d93dad7324c428f7ca69024100c498640e4cfe29628adff631ef07adc5dfd80a37482ae7e8c333e91291ad97d66fce820f60ebe6670386a2ac6f8861c108740806bd3fab0c23ed60de4a8f803d024100df214b7890bc788c601a52009c6b34d515bed74327cbdccb4276245b6abcf2c08b432b9902bd13864f64f6e21384636f6456389248de97116683e6cc0d613a17024068285d0a7e9c420ce58b170309a345dc0a6689b31457371b49209da1aaf10ffb1aad8c96dd40de874184f976e67899620e3a7b6e26a22edb75c574871175c9f9024100c0815b39b3b5c75364fe904d12a6b3b83bc0a0bbc1b3f2d4328cf7251fdbd09c2a0a53acf95de360775326653a6d77d47cfe9e64271653c3a16c9f4ce1264715024031743c8eba2072bf97d314e35610d16afde8d98a7865ba36b109394e2da5b30c400c8eae41b5217b6ef54a97cd4873da14e63d47f6940de6db01512963044320'
amount = 10
recipient_public_key = '30819f300d06092a864886f70d010101050003818d0030818902818100ab5a50c296ceded77bca8d04d12339f993114cfb6bcc708ffe8c11dc5dab3af76b195669b9885ea00509c22a9275dc00906cfe95833dbbb6b8f9bfd62a30c3a4d5b758b3207222ee4ee0a5012d6d24ea1181f56a2b00ef6b5cd578f28b92cda8edb9d03ab72a2e00ef3c2bbbaae2e0b08d5e6959d99d84cc4511995be60f577b0203010001'

new_transaction = Transaction(sender_public_key,sender_private_key,amount,recipient_public_key)
if(new_transaction.generate_transaction()):
    print('Transaction Successfully Added')
else:
    print('Wrong Transaction')
