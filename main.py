
import os
import sys
import platform
import subprocess
from prompt_toolkit import PromptSession # pip install prompt_toolkit

def genkey():
    try:
        subprocess.run("ssh-keygen -f $HOME/.ssh/DKAP/1", check=True)
    except subprocess.CalledProcessError:
        print("Key generation failed")


def main():
    session = PromptSession()

    print("\nWelcome to the Distributed Key Authority Project.")
    print("Type \'help\' for available commands. Press up for previous commands.\n")

    ### FIRST INIT ###

    if os.path.isdir(os.environ["USERPROFILE"] + "\\.ssh\\DKAP"):
        print("DKAP folder exists.")
    else:
        try:
            print("Creating DKAP folder at " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP")
            cmd = "mkdir " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP"  # HOME variable, really
            subprocess.run(cmd, shell=True, check=True)  # stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL for silent error, silent run
        except subprocess.CalledProcessError:
            print("DKAP folder creation failed. Insufficient permissions? Application will now exit.")
            sys.exit(1)

    if os.path.isfile(os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"): # if folder exists but register doesn't exist
        print("DKAP register exists.")
    else:
        try:
            cmd = "type NUL > " + os.environ["USERPROFILE"] + "\\.ssh\\DKAP\\register.txt"
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("DKAP register creation failed. Insufficient permissions? Application will now exit.")
            sys.exit(1)

    ### FIRST INIT ###

    while True:
        print(">", end="")
        input = session.prompt()

        if input == "help":
            print("Help dialogue.")
        elif input == "exit":
            sys.exit(0)
        elif input == "list":
            print("List keys. Own private key and other installed public keys here.")
        elif input == "upd":
            print("Update public keys according to blockchain. This should be done automatically, remove later.")
        elif input == "gen":
            print("Generate keypair for this machine. Save private key (ssh-add), commit public key to blockchain. Maybe on first run only.")
            genkey()
        elif input == "del":
            print("Delete keypair for this machine. Delete private key (ssh-add -d), commit public key deletion to blockchain.")
        else:
            print("Unrecognised command. Type \'help\' for available commands. Press up for previous commands.")


if __name__ == "__main__":

    if platform.system() != "Windows":
        print("DKAP runs on Windows systems only, for now.")
        sys.exit(1)

    main()
