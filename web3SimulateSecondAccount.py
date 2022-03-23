import asyncio
import json

from web3 import Web3



# INFURA WEB SOCKET API
infura_url='https://ropsten.infura.io/v3/2fff4910776f44fabc07743eac1186e3' #your uri
web3 = Web3(Web3.HTTPProvider(infura_url))
mainAccount = "0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9"
secondAccount = "0x2592175D63aeAfC7ADDE6014Fd1A881B16e17A9e"
private_key = "4f551f1ab248237b0d974ed4921bb01b852f402834c2ddf156b3e798bc4e1f46"

print("Connected to testnet " + str(web3.isConnected()))
print("Latest block number "+ str(web3.eth.blockNumber))
print("Details of block "+ str(web3.eth.get_block('latest')))

balance = web3.eth.getBalance("0x2592175D63aeAfC7ADDE6014Fd1A881B16e17A9e")
print("Current Balance " + str(balance / (10**18) ))

#Smart contract ABI and address it was deployed
abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
address= web3.toChecksumAddress("0x365C49A29A2be257A89918776708E8956259AB9d")

#test = web3.eth.account("0x9e659CF30F66956E2Dedf4027b81e39Ff1F0a7a9")
#Est contract
contract = web3.eth.contract(address=address,abi=abi)
'''
#To Read Data
incomingPubValue = contract.functions.getPubKey().call()
print(incomingPubValue)
'''
'''
#Demo account #2 read and save into the contract using the set method
pubFile = open("2.pub", "r")
pubKey = pubFile.read()
tx = contract.functions.setPubKey(pubKey).buildTransaction({
    'from': secondAccount,  # Only 'from' address, don't insert 'to' address
    'value': 0,  # Add how many ethers you'll transfer during the deploy
    'gas': 2000000,  # Trying to make it dynamic ..
    'gasPrice': web3.eth.gasPrice,  # Get Gas Price
    'nonce': web3.eth.getTransactionCount(secondAccount)
})

signed = web3.eth.account.signTransaction(tx, private_key)

tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash)
web3.eth.wait_for_transaction_receipt(tx_hash)
print('updated noob')
'''

# define function to handle events and print to the console
def handle_event(event):
    print(event.args.STATUS)
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairEvent in event_filter.get_new_entries():
            handle_event(PairEvent)
        await asyncio.sleep(poll_interval)

def main():
    event_filter = contract.events.PairEvent.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()

