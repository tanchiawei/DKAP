
import os
import sys
import time  # for listener
import platform
import threading
import subprocess
from prompt_toolkit import PromptSession  # pip install prompt_toolkit

# for housekeeping, separate functions into different files when complete
from DKAPinit import initCheck


def genKeyPair():
    try:
        cmd = "ssh-keygen -f " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\SELF -t ecdsa -b 521 -C \"WalletAddress\"" ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
        subprocess.run(cmd, shell=True, check=True)
        cmd = "ssh-add " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\SELF"  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
        subprocess.run(cmd, shell=True, check=True)  # add privkey to ssh-agent
        ### FUNCTION TO COMMIT SELF.PUBKEY TO BLOCKCHAIN HERE ###
    except subprocess.CalledProcessError:
        print("Key generation failed.")

def delKeyPair():
    cmd = "ssh-add -d " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\SELF"  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
    subprocess.run(cmd, shell=True, check=True)  # del privkey from ssh-agent
    ### FUNCTION TO DELETE SELF.PUBKEY FROM BLOCKCHAIN HERE ###


def listKeys():  # display pubkeys in authorized_keys folder that are managed by DKAP. tracked in register.txt
    pass


def addPubKey():  # should take an argument for the pubkey to add, data comes from blockchain
    pass  # after adding, should add line to register.txt if does not exist


def rmPubKey():  # should take an argument for the pubkey to remove, data comes from blockchain
    pass  # after removing, delete line from register.txt


def listenplaceholder():
    pass
    #  while True:
        #  print("Listening..")  # should be listening silently
        #  time.sleep(3)
    ### FUNCTION TO LISTEN FOR BLOCKCHAIN EVENTS HERE ###
    ### based on event received:
    ### addPrivKey()  #  adding and removing pubKeys from authorized_keys folder
    ### rmPrivKey()


def main():
    session = PromptSession()

    print("\nWelcome to the Distributed Key Authority Project.")
    print("Type \'help\' for available commands. Press up for previous commands.\n")

    initCheck()  # check that folders and files required are present

    listenthread = threading.Thread(target=listenplaceholder, daemon=True)  # args= for arguments to pass, daemon= to kill thread when main ends
    listenthread.start()  # while kms is running, listen for blockchain changes

    while True:
        print("> ", end="")
        input = session.prompt()

        if input == "help":
            print("Help dialogue.")
        elif input == "exit":
            sys.exit(0)
        elif input == "list":
            print("List keys. Own private key and other installed public keys here. Refer to register.txt")
            listKeys()
        elif input == "gen":
            print("Generating keypair for this machine. Save private key (ssh-add), commit public key to blockchain. Maybe on first run only.")
            genKeyPair()
        elif input == "del":
            print("Delete keypair for this machine. Delete private key (ssh-add -d), commit public key deletion to blockchain.")
            delKeyPair()
        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":

    if platform.system() != "Windows":
        print("DKAP runs on Windows systems only, for now. This application will now exit.")
        sys.exit(1)

    main()
