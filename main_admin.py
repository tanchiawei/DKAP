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

    while True:
        print("> ", end="")
        input = session.prompt()
        if input == "help":
            print("HELP - COMMANDS AVAILABLE FOR DKAP ADMIN:.")
            print("gen - Generating keypair for this machine. Save private key (ssh-add), commit public key to blockchain.")
            print("del - Delete keypair for this machine. Delete private key (ssh-add -d), commit public key deletion to blockchain.")
            print("addnode <wallet address> - Permitting node for the input address.")
            print("del <wallet address> - Deleting node for the input address.")
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
        elif len(input.split(" ")) == 2:
            if input.split()[0] == "addnode":
                print("Permitting node for the input address.")
                ssh_admin.add_permitted_address(input.split()[1])
            elif input.split()[0] == "removenode":
                print("Deleting node for the input address.")
                ssh_admin.remove_permitted_address(input.split()[1])

        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":
    file_exists = os.path.isfile(".\\admin.txt")
    if file_exists:
        admin_file = open('admin.txt', 'r')
        admin_lines = admin_file.readlines()
        if len(admin_lines) < 2:
            print("You are not authorized admin")
        else:
            main_account = admin_lines[0].strip()
            private_key = admin_lines[1].strip()
            #ssh_peer = ssh_peer()
            ssh_node = ssh_node(main_account,private_key)
            ssh_admin = ssh_admin(main_account,private_key)
            if platform.system() != "Windows":
                print("DKAP runs on Windows systems only, for now. This application will now exit.")
                sys.exit(1)

        main()
    else:
        print("Please configure your admin.txt")
