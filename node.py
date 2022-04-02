import base64
import json
import os
import subprocess
import time
from unicodedata import name

from web3 import Web3


class ssh_node:
    def __init__(self) -> None:
        # INFURA WEB SOCKET API
        # infura_url = 'https://ropsten.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        infura_url = 'https://rinkeby.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        # infura_url = 'https://eth-ropsten.alchemyapi.io/v2/Kc77KmAsZu_ctaAJ_xUxBHmNMonYZdEN'  # your uri
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        node_file = open('node.txt', 'r')
        node_lines = node_file.readlines()
        self.main_account = node_lines[0].strip()
        self.private_key = node_lines[1].strip()
        # Smart contract ABI and address it was deployed

        self.abi = json.loads(
            '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"},{"indexed":false,"internalType":"bytes","name":"ADDRESS","type":"bytes"}],"name":"PairError","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"delete_public_key","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
        self.address = self.web3.toChecksumAddress("0xb2bc329e642f1706017f3276d6b07faf7f0cb46f")
        # self.address = self.web3.toChecksumAddress("0x304f9500452c38ac3f7621005bef95c83703d79a")
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def add_public_value(self, in_public_file):
        # Demo account #2 read and save into the contract using the set method
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
        print(tx_hash)
        time.sleep(4)
        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        decoded_logs = self.contract.events.PairError().processReceipt(receipt)
        # Access details as simply as:
        status = ''
        for log in decoded_logs:
            status = log.args.STATUS
        if "Not Authorized" in status:
            print("NOT AUTHORIZED")

    def remove_public_value(self):
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
        print(tx_hash)

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

        except subprocess.CalledProcessError:
            print("Key generation failed.")

    def delKeyPair(self):
        cmd = "ssh-add -d \"" + os.environ[
            "USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + "\""  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
        subprocess.run(cmd, shell=True, check=True)  # del privkey from ssh-agent
        os.remove(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account)
        os.remove(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\" + self.main_account + ".pub")
        ### FUNCTION TO DELETE SELF.PUBKEY FROM BLOCKCHAIN HERE ###
        # ssh_admin.remove_permitted_address("0x2592175D63aeAfC7ADDE6014Fd1A881B16e17A9e")
        # ssh_admin.add_permitted_address("0x2592175D63aeAfC7ADDE6014Fd1A881B16e17A9e")
        self.remove_public_value()
