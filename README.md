# DKAP

The blockchain-based KMS must be installed on each participating device and uniquely identified by an address (similar to the identifier for a Bitcoin wallet). Every peer on this private/permissioned blockchain must be pre-approved by a steward. It must be capable of generating SSH key pairs for devices and storing the public key on the blockchain as a transaction. When a user attempts to SSH to this device, the KMS must refer to the blockchain for the user’s public key and device; if the key is accurate, up to date and from the correct originating device (as identified by address), the connection is established.

Keypairs that are generated must be regularly rotated – the KMS will prompt the user to renew keys that are out of date (as identified by its generation timestamp on the blockchain). The KMS will handle the uninstallation of the old private key and attaching the uninstallation of the corresponding old public key to the blockchain – after which it will install the new public key and attach the installation of the new public key to the blockchain.

The KMS must periodically compare its blockchain with that of its peers to obtain updates (installing and uninstalling keys as instructed) and identify fraudulent transactions (e.g., a device has more than one keypair assigned to it, a keypair is installed for an unknown peer, etc.).

The KMS on all participating devices must be able to continue to function if any single device fails.

There must also be one or more appointed wardens to take executive action if warranted (e.g., a new device is added and must be listed as a peer, or a device is stolen, and all the keys assigned to that device must be purged from the canonical blockchain).

# Pre-requisite

python => 3.8 <br/>
pip <br/>
Metamask wallet ( Wallet Address , Private Key of Wallet) <br/>
SSH agent <br/>
SSH key-gen <br/>
Windows <br/>

# Node

Start Windows Powershell x86 as admin <br/>
Set-Service ssh-agent -StartupType Manual <br/>
Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_node.py <br/>

# Peer

Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_peer.py <br/>

# Admin

Start Windows Powershell x86 as admin <br/>
Set-Service ssh-agent -StartupType Manual <br/>
Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_admin.py <br/>
