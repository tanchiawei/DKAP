from web3 import Web3

import json
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.defaultAccount = web3.eth.accounts[0]
abi = json.loads('[{"inputs":[],"name":"Greeter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greets","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
address= web3.toChecksumAddress("0xa3412d684e70c8B440f2d219Cc98A68d92E5effb")

contract = web3.eth.contract(address=address,abi=abi)
print(contract.functions.greets().call())
tx_hash=contract.functions.setGreeting('TEST').transact()


print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)
print('updated noob')

print(contract.functions.greets().call())