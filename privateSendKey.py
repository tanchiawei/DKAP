from web3 import Web3

import json
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

#Demo account #1
#web3.eth.defaultAccount = web3.eth.accounts[0]

#Demo account #2
web3.eth.defaultAccount = web3.eth.accounts[1]

#Smart contract ABI and address it was deployed
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"getPubKeyHalf1","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_Half1","type":"string"}],"name":"setPubKeyHalf1","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
address= web3.toChecksumAddress("0x2D0828C817903704aD0Da055dbABea94581dCb42")

#Est contract
contract = web3.eth.contract(address=address,abi=abi)

#Demo account #1 read and save into the contract using the set method
'''pubFile = open("id_rsa.pub", "r")
pubKey = pubFile.read()

tx_hash=contract.functions.setPubKeyHalf1(pubKey).transact()
print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)'''

#Demo account #2 use get method
incomingPubValue = contract.functions.getPubKeyHalf1().call()
f = open("demoPub.pub", "w")
f.write(incomingPubValue)
f.close()