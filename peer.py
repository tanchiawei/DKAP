import asyncio
import json
import os
import subprocess
import time

from web3 import Web3


class ssh_peer:
    def __init__(self) -> None:
        self.alive_address = []
        file_exists = os.path.isfile(os.path.abspath(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"))
        if file_exists:
            register_file = open(os.path.abspath(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"), 'r')
            self.alive_address = register_file.read().splitlines()
        else:
            open(os.path.abspath(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"), 'w+')
        print(self.alive_address)
        # INFURA WEB SOCKET API
        self.alive_public_key = []
        infura_url = 'https://rinkeby.infura.io/v3/2fff4910776f44fabc07743eac1186e3'  # your uri
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.main_account = ""
        self.private_key = ""
        address_file = open('contract.txt', 'r')
        address_lines = address_file.readlines()
        address = address_lines[0].strip()
        # Smart contract ABI and address it was deployed
        self.abi = json.loads(
            '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"},{"indexed":false,"internalType":"bytes","name":"ADDRESS","type":"bytes"}],"name":"PairError","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"STATUS","type":"string"}],"name":"PairEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"test","type":"address"},{"indexed":false,"internalType":"address","name":"test2","type":"address"}],"name":"VoteCast","type":"event"},{"inputs":[],"name":"adminGetPermittedAddresses","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"inRemoveAddress","type":"address"}],"name":"adminRemovePermittedAdress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"inPermittedAddress","type":"address"}],"name":"adminSetPermittedAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"delete_public_key","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPubKey","outputs":[{"components":[{"internalType":"address","name":"permittedAddress","type":"address"},{"internalType":"string","name":"pubValue","type":"string"},{"internalType":"bool","name":"flag","type":"bool"}],"internalType":"struct PubKey.pubKey[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"inPubKey","type":"string"}],"name":"setPubKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"}]')
        self.address = self.web3.toChecksumAddress(address)
        # self.address = self.web3.toChecksumAddress("0xE175bC1A687a8490B15381235011BB77981DC1C4")

        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def handle_event(self, event):
        print(event.args.STATUS)
        if event.args.STATUS == "NEW":
            self.read_public_key()
        elif event.args.STATUS == "DELETE":
            self.read_public_key()

    def read_public_key(self):
        try:
            chain_current_list = 0

            incomingPubValue = self.contract.functions.getPubKey().call()
            valid_public_address = []
            for each_public_key in incomingPubValue:
                if each_public_key[0] == '0x0000000000000000000000000000000000000000':
                    pass
                else:
                    valid_public_address.insert(len(valid_public_address), each_public_key[0])
                    if each_public_key[1] != '':
                        chain_current_list += 1
                        if each_public_key[0] not in self.alive_address:
                            self.alive_address.insert(len(self.alive_address), each_public_key[0])
                            self.add_public_key(each_public_key[0], each_public_key[1])
                        else:
                            self.add_public_key(each_public_key[0], each_public_key[1])
                    else:
                        if each_public_key[0] in self.alive_address:
                            self.alive_address.remove(each_public_key[0])
                            self.delete_public_key(each_public_key[0])
            for each_alive_address in self.alive_address:
                if each_alive_address not in valid_public_address:
                    self.alive_address.remove(each_alive_address)
                    self.delete_public_key(each_alive_address)

            with open(os.path.abspath(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"), "w") as f:
                alive_address = "\n".join(self.alive_address)
                f.write(alive_address)
            f.close()
            print('Updated Public Key')
            print(self.alive_address)
        except:
            print('Issued occurred during reading of block chain.')

    def add_public_key(self, in_address, in_public_key):
        try:
            f = open("" + os.path.abspath(os.environ["USERPROFILE"] + "\\.ssh\\authorized_keys\\" + in_address) + ".pub", "w")
            f.write(in_public_key)
            f.close()
        except:
            print('Issued occurred during saving of public key')

    def delete_public_key(self, in_address):
        try:
            os.remove(os.environ["USERPROFILE"] + "\\.ssh\\authorized_keys\\" + in_address + ".pub")
        except:
            print('Issued occurred during deleting of public key')
    def listen(self):
        event_filter = self.contract.events.PairEvent.createFilter(fromBlock='latest')
        while True:
            print("Listening..")  # should be listening silently
            time.sleep(4)
            for PairEvent in event_filter.get_new_entries():
                self.handle_event(PairEvent)
