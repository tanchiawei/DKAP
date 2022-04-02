import os
import sys
import time  # for listener
import platform
import threading
import subprocess
from prompt_toolkit import PromptSession  # pip install prompt_toolkit
from node import ssh_node
from admin import ssh_admin
from peer import ssh_peer
# for housekeeping, separate functions into different files when complete
from DKAPinit import initCheck


def main():
    session = PromptSession()

    print("\nWelcome to the Distributed Key Authority Project.")
    print("Type \'help\' for available commands. Press up for previous commands.\n")

    initCheck()  # check that folders and files required are present

    #listenthread = threading.Thread(target=ssh_peer.listen,
                                    #daemon=True)  # args= for arguments to pass, daemon= to kill thread when main ends
    #listenthread.start()  # while kms is running, listen for blockchain changes

    while True:
        print("> ", end="")
        input = session.prompt()
        print(input[:-1])
        if input == "help":
            print("Help dialogue.")
        elif input == "exit":
            sys.exit(0)
        elif input == "gen":
            print(
                "Generating keypair for this machine. Save private key (ssh-add), commit public key to blockchain. Maybe on first run only.")
            ssh_node.genKeyPair()
        elif input == "del":
            print(
                "Delete keypair for this machine. Delete private key (ssh-add -d), commit public key deletion to blockchain.")
            ssh_node.delKeyPair()
        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":
    ssh_node = ssh_node()
    if platform.system() != "Windows":
        print("DKAP runs on Windows systems only, for now. This application will now exit.")
        sys.exit(1)

    main()
