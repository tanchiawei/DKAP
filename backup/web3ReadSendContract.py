import json

from web3 import Web3



# INFURA WEB SOCKET API
#infura_url='https://ropsten.infura.io/v3/2fff4910776f44fabc07743eac1186e3' #your uri
infura_url = 'https://rinkeby.infura.io/v3/2fff4910776f44fabc07743eac1186e3'
web3 = Web3(Web3.HTTPProvider(infura_url))
mainAccount = "0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9"
secondAccount = "0x2592175D63aeAfC7ADDE6014Fd1A881B16e17A9e"
private_key1 = "a0750e6eaa34fde61a642d208ec2f7ade2519047bf0b57f0d4f598da9f222dc1"
private_key = "4f551f1ab248237b0d974ed4921bb01b852f402834c2ddf156b3e798bc4e1f46"

print("Connected to testnet " + str(web3.isConnected()))
print("Latest block number "+ str(web3.eth.blockNumber))
#print("Details of block "+ str(web3.eth.get_block('latest')))

balance = web3.eth.getBalance("0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9")
print("Current Balance " + str(balance / (10**18) ))

#Smart contract ABI and address it was deployed
abi = json.loads(
    '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"},{"indexed":false,"internalType":"bytes","name":"ADDRESS","type":"bytes"}],"name":"PairError","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"delete_public_key","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
address = web3.toChecksumAddress("0x46b45f9622b4be0dE27d974E36862748bF317C4C")

#test = web3.eth.account("0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9")
#Est contract

contract = web3.eth.contract(address=address,abi=abi)

#Admin add PermittedAddress
'''
PermittedAddress= web3.toChecksumAddress(mainAccount)
tx = contract.functions.adminSetPermittedAddresses(PermittedAddress).buildTransaction({
    'from': mainAccount,  # Only 'from' address, don't insert 'to' address
    'value': 0,  # Add how many ethers you'll transfer during the deploy
    'gas': 2000000,  # Trying to make it dynamic ..
    'gasPrice': (5000000000+web3.eth.gasPrice),  # Get Gas Price
    'nonce': web3.eth.getTransactionCount(mainAccount)
})

signed = web3.eth.account.signTransaction(tx, private_key1)

tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)
print('updated noob')
'''


'''
signer = web3.eth.accounts.privateKeyToAccount(private_key)
web3.eth.accounts.wallet.add(signer)
'''
'''
#Demo account #1 read and save into the contract using the set method
pubFile = open("2.pub", "r")
pubKey = pubFile.read()


tx = contract.functions.setPubKeyHalf1(pubKey).buildTransaction({
    'nonce': web3.eth.getTransactionCount(mainAccount)
})

signed = web3.eth.account.signTransaction(tx, private_key)

txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

print(txn_hash)
transaction = {
            'from': mainAccount, # Only 'from' address, don't insert 'to' address
            'value': 0, # Add how many ethers you'll transfer during the deploy
            'gas': 2000000, # Trying to make it dynamic ..
            'gasPrice': web3.eth.gasPrice, # Get Gas Price
            'nonce': web3.eth.getTransactionCount(address), # Get Nonce
            'data': tx # Here is the data sent through the network
        }


signed_tx = web3.eth.account.signTransaction(transaction,private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)
print('updated noob')
'''

#Demo account #2 use get method
'''
incomingPubValue = contract.functions.getPubKeyHalf1().call()
print(incomingPubValue)

f = open("demoPub.pub", "w")
f.write(incomingPubValue)
f.close()
incomingPubValue = contract.functions.destroy().call()
print(incomingPubValue)'''

#Demo account #2 read and save into the contract using the set method
pubFile = open("../2.pub", "r")
pubKey = pubFile.read()
tx = contract.functions.setPubKey(pubKey).buildTransaction({
    'from': mainAccount,  # Only 'from' address, don't insert 'to' address
    'value': 0,  # Add how many ethers you'll transfer during the deploy
    'gas': 2000000,  # Trying to make it dynamic ..
    'gasPrice': (5000000000+web3.eth.gasPrice),  # Get Gas Price
    'nonce': web3.eth.getTransactionCount(mainAccount)
})

signed = web3.eth.account.signTransaction(tx, private_key1)

tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)
print('updated noob')