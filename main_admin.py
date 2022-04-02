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
        if input == "help":
            print("Help dialogue.")
        elif input == "exit":
            sys.exit(0)
        elif input.split()[0] == "addnode":
            ssh_admin.add_permitted_address(input.split()[1])
        elif input.split()[0] == "removenode":
            ssh_admin.remove_permitted_address(input.split()[1])
        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":
    ssh_peer = ssh_peer()
    ssh_node = ssh_node()
    ssh_admin = ssh_admin()
    if platform.system() != "Windows":
        print("DKAP runs on Windows systems only, for now. This application will now exit.")
        sys.exit(1)

    main()
