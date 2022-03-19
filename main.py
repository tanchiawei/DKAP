
import os
import sys
import time
import platform
import threading
import subprocess
from prompt_toolkit import PromptSession  # pip install prompt_toolkit


def initcheck():
    if os.path.isdir(os.environ["USERPROFILE"] + "\\.ssh\\DKAP"):  # create folder to house DKAP managed data
        print("DKAP folder exists.")
    else:
        try:
            print("Creating DKAP folder at " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP")
            cmd = "mkdir " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP"  # HOME variable, really
            subprocess.run(cmd, shell=True, check=True)  # stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL for silent error, silent run
        except subprocess.CalledProcessError:
            print("DKAP folder creation failed. Insufficient permissions? Application will now exit.")
            sys.exit(1)

    if os.path.isdir(os.environ["USERPROFILE"] + "\\.ssh\\authorized_keys"):  # create folder to house authorised pubkeys (people who can ssh to this machine)
        print("authorized_keys folder exists.")  # SSH standard folder (https://security.stackexchange.com/questions/20706/what-is-the-difference-between-authorized-keys-and-known-hosts-file-for-ssh)
    else:
        try:
            print("Creating authorized_keys folder at " + os.environ["USERPROFILE"] + "\\.ssh\\authorized_keys")
            cmd = "mkdir " + os.environ["USERPROFILE"] + "\\.ssh\\authorized_keys"  # HOME variable, really
            subprocess.run(cmd, shell=True, check=True)  # stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL for silent error, silent run
        except subprocess.CalledProcessError:
            print("authorized_keys folder creation failed. Insufficient permissions? Application will now exit.")
            sys.exit(1)

    if os.path.isfile(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"):  # create file to track which pubkeys are managed by DKAP, there may be sshkeys that are not DKAP's business
        print("DKAP register exists.")
    else:
        try:
            cmd = "type NUL > " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("DKAP register creation failed. Insufficient permissions? Application will now exit.")
            sys.exit(1)


def genkey():
    try:
        cmd = "ssh-keygen -f " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\SELF -t ecdsa -b 521 -C \"WalletAddress\"" ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
        subprocess.run(cmd, shell=True, check=True)
        cmd = "ssh-add " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\SELF"  ### replace SELF and WALLETADDRESS with wallet address, unique identifier for self
        subprocess.run(cmd, shell=True, check=True)  # add privkey to ssh-agent
        ### FUNCTION TO COMMIT SELF.PUBKEY TO BLOCKCHAIN HERE ###
    except subprocess.CalledProcessError:
        print("Key generation failed.")

def delkey():
    pass


def listenplaceholder():
    pass
    #  while True:
        #  print("Listening..")  # should be listening silently
        #  time.sleep(3)


def main():
    session = PromptSession()

    print("\nWelcome to the Distributed Key Authority Project.")
    print("Type \'help\' for available commands. Press up for previous commands.\n")

    initcheck()  # check that folders and files required are present

    listenthread = threading.Thread(target=listenplaceholder, daemon=True)  # args= for arguments to pass, daemon to kill thread when main ends
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
        elif input == "gen":
            print("Generating keypair for this machine. Save private key (ssh-add), commit public key to blockchain. Maybe on first run only.")
            genkey()
        elif input == "del":
            print("Delete keypair for this machine. Delete private key (ssh-add -d), commit public key deletion to blockchain.")
            delkey()
        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":

    if platform.system() != "Windows":
        print("DKAP runs on Windows systems only, for now. This application will now exit.")
        sys.exit(1)

    main()
