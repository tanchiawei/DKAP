import json

from web3 import Web3


class ssh_admin:
    def __init__(self, main_account, private_key) -> None:
        # INFURA WEB SOCKET API
        infura_url = 'https://rinkeby.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.main_account = main_account
        self.private_key = private_key
        address_file = open('contract.txt', 'r')
        address_lines = address_file.readlines()
        address = address_lines[0].strip()
        # Smart contract ABI and address it was deployed
        self.abi = json.loads(
            '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"},{"indexed":false,"internalType":"bytes","name":"ADDRESS","type":"bytes"}],"name":"PairError","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"delete_public_key","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
        self.address = self.web3.toChecksumAddress(address)
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def add_permitted_address(self, in_permitted):
        if len(in_permitted) < 42:
            print("You enter incorrect address format")
            return
        try:
            self.permitted_address = self.web3.toChecksumAddress(in_permitted)
            self.tx = self.contract.functions.adminSetPermittedAddresses(self.permitted_address).buildTransaction({
                'from': self.main_account,  # Only 'from' address, don't insert 'to' address
                'value': 0,  # Add how many ethers you'll transfer during the deploy
                'gas': 2000000,  # Trying to make it dynamic ..
                'gasPrice': (5000000000 + self.web3.eth.gasPrice),  # Get Gas Price
                'nonce': self.web3.eth.getTransactionCount(self.main_account)
            })

            self.signed = self.web3.eth.account.signTransaction(self.tx, self.private_key)

            self.tx_hash = self.web3.eth.sendRawTransaction(self.signed.rawTransaction)
            self.web3.eth.wait_for_transaction_receipt(self.tx_hash)
            print('Successfully permitted address')
        except:
            print('Issued occurred during transacting to block chain.')

    def remove_permitted_address(self, in_permitted):
        if len(in_permitted) < 42:
            print("You enter incorrect address format")
            return
        try:
            self.permitted_address = self.web3.toChecksumAddress(in_permitted)
            self.tx = self.contract.functions.adminRemovePermittedAdress(self.permitted_address).buildTransaction({
                'from': self.main_account,  # Only 'from' address, don't insert 'to' address
                'value': 0,  # Add how many ethers you'll transfer during the deploy
                'gas': 2000000,  # Trying to make it dynamic ..
                'gasPrice': (5000000000 + self.web3.eth.gasPrice),  # Get Gas Price
                'nonce': self.web3.eth.getTransactionCount(self.main_account)
            })

            self.signed = self.web3.eth.account.signTransaction(self.tx, self.private_key)

            self.tx_hash = self.web3.eth.sendRawTransaction(self.signed.rawTransaction)

            self.web3.eth.wait_for_transaction_receipt(self.tx_hash)
            print('Successfully removed address')
        except:
            print('Issued occurred during transacting to block chain.')
