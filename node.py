import base64
import json
import os
import subprocess
import time
from unicodedata import name

from web3 import Web3


class ssh_node:
    def __init__(self, main_account, priv_key) -> None:
        # INFURA WEB SOCKET API
        # infura_url = 'https://ropsten.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        infura_url = 'https://rinkeby.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        # infura_url = 'https://eth-ropsten.alchemyapi.io/v2/Kc77KmAsZu_ctaAJ_xUxBHmNMonYZdEN'  # your uri
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.main_account = main_account
        self.private_key = priv_key
        # Smart contract ABI and address it was deployed

        self.abi = json.loads(
            '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"},{"indexed":false,"internalType":"bytes","name":"ADDRESS","type":"bytes"}],"name":"PairError","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"delete_public_key","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
        self.address = self.web3.toChecksumAddress("0x46b45f9622b4be0dE27d974E36862748bF317C4C")
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def add_public_value(self, in_public_file):
        try:
            pub_file = open(in_public_file, "r")
            pub_key = pub_file.read()
            tx = self.contract.functions.setPubKey(pub_key).buildTransaction({
                'from': self.main_account,  # Only 'from' address, don't insert 'to' address
                'value': 0,  # Add how many ethers you'll transfer during the deploy
                'gas': 2000000,  # Trying to make it dynamic ..
                'gasPrice': (5000000000 + self.web3.eth.gasPrice),  # Get Gas Price
                'nonce': self.web3.eth.getTransactionCount(self.main_account)
            })

            signed = self.web3.eth.account.signTransaction(tx, self.private_key)

            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)

            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            time.sleep(4)
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            decoded_logs = self.contract.events.PairEvent().processReceipt(receipt)
            # Access details as simply as:
            status = ''
            for log in decoded_logs:
                status = log.args.STATUS
            if "Not Authorized" in status:
                print("NOT AUTHORIZED")
            else:
                print('Successfully added public key.')
        except:
            print('Issued occurred during transacting to block chain.')

    def remove_public_value(self):
        try:
            tx = self.contract.functions.delete_public_key().buildTransaction({
                'from': self.main_account,  # Only 'from' address, don't insert 'to' address
                'value': 0,  # Add how many ethers you'll transfer during the deploy
                'gas': 2000000,  # Trying to make it dynamic ..
                'gasPrice': (5000000000 + self.web3.eth.gasPrice),  # Get Gas Price
                'nonce': self.web3.eth.getTransactionCount(self.main_account)
            })
            signed = self.web3.eth.account.signTransaction(tx, self.private_key)

            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            self.web3.eth.wait_for_transaction_receipt(tx_hash)
            print('Successfully removed public key.')
        except:
            print('Issued occurred during transacting to block chain.')

    def genKeyPair(self):
        try:
            cmd = "ssh-keygen -f \"" + os.environ[
                "USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + "\" -t ecdsa -b 521 -C \"" + self.main_account + "\""  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
            subprocess.run(cmd, shell=True, check=True)
            cmd = "ssh-add \"" + os.environ[
                "USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + "\""  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
            subprocess.run(cmd, shell=True, check=True)  # add privkey to ssh-agent
            ### FUNCTION TO COMMIT SELF.PUBKEY TO BLOCKCHAIN HERE ###
            self.add_public_value(
                os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + ".pub")
            print('Done generating')

        except subprocess.CalledProcessError:
            print("Key generation failed.")

    def delKeyPair(self):
        try:
            cmd = "ssh-add -d \"" + os.environ[
                "USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + "\""  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
            subprocess.run(cmd, shell=True, check=True)  # del privkey from ssh-agent
            os.remove(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account)
            os.remove(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + ".pub")
            ### FUNCTION TO DELETE SELF.PUBKEY FROM BLOCKCHAIN HERE ###
            self.remove_public_value()
            print('Done deleting')
        except:
            print('Failed to delete key pair')
