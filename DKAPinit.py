import os
import sys
import subprocess

def initCheck():
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