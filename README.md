# DKAP

The blockchain-based KMS must be installed on each participating device and uniquely identified by an address (similar to the identifier for a Bitcoin wallet). Every peer on this private/permissioned blockchain must be pre-approved by a steward. It must be capable of generating SSH key pairs for devices and storing the public key on the blockchain as a transaction. When a user attempts to SSH to this device, the KMS must refer to the blockchain for the user’s public key and device; if the key is accurate, up to date and from the correct originating device (as identified by address), the connection is established.

Keypairs that are generated must be regularly rotated – the KMS will prompt the user to renew keys that are out of date (as identified by its generation timestamp on the blockchain). The KMS will handle the uninstallation of the old private key and attaching the uninstallation of the corresponding old public key to the blockchain – after which it will install the new public key and attach the installation of the new public key to the blockchain.

The KMS must periodically compare its blockchain with that of its peers to obtain updates (installing and uninstalling keys as instructed) and identify fraudulent transactions (e.g., a device has more than one keypair assigned to it, a keypair is installed for an unknown peer, etc.).

The KMS on all participating devices must be able to continue to function if any single device fails.

There must also be one or more appointed wardens to take executive action if warranted (e.g., a new device is added and must be listed as a peer, or a device is stolen, and all the keys assigned to that device must be purged from the canonical blockchain).

# Pre-requisite

Python => 3.8 <br/>
Pip <br/>
Metamask wallet ( Wallet Address , Private Key of Wallet) <br/>
SSH agent <br/>
SSH key-gen <br/>
Windows <br/>

# Installation and Usage of MetaMask wallet
Click [here] to download. <br/>
Create / Login your MetaMask Wallet. <br/>
Create at least 2 wallet address. <br/>
Request for testnet ethereum at this [website]. <br/>

[here]: https://metamask.io/download/
[website]: https://rinkebyfaucet.com/

# SSH Agent for Node Machine
Enable SSH Agent if disabled using the following command in PowerShell terminal as Administrator. <br/>
```Set-Service -Name ssh-agent -StartupType Manual``` <br/>
Start SSH Agent service. <br/>
```Start-Service ssh-agent``` <br/>

# Wallet Configuration for Admin / Node machine
Admin / Node text file to change accordingly to your wallet address and private key <br/>
![image](https://user-images.githubusercontent.com/72211145/161926003-af096d70-2390-424c-9182-62e14b7aee17.png)

![image](https://user-images.githubusercontent.com/72211145/161926064-0149af4f-f3b6-441a-8ee1-1ca7e177c332.png)



# Deploy Smart Contract
Proceed to [Remix] on any browser. <br/>
Load the solidity code contract.sol onto [Remix] IDE <br/>
Make necessary changes to wallet address of the administrator machine
![image](https://user-images.githubusercontent.com/72211145/161918052-7f415acf-65b0-4b58-947f-2c2d27eb55b9.png)
<br/>
![image](https://user-images.githubusercontent.com/72211145/161918526-61897e9f-68fb-4845-b842-0ced1374646c.png)

Compile the code with 0.87+commit <br/>
![image](https://user-images.githubusercontent.com/72211145/161832689-a32523e1-f004-4196-b487-6f6b7c879a39.png) <br/>
Change the environment to Injected Web3 with selected wallet
Deploy
![image](https://user-images.githubusercontent.com/72211145/161832915-7d95b5e4-f012-471d-ae14-0f11793344a7.png)

Modify with new deployed contract address
![image](https://user-images.githubusercontent.com/72211145/161925821-725e52a1-2d00-414d-a40d-8c2f8b8d8c73.png)



[Remix]: https://remix.ethereum.org/#optimize=false&runs=200&evmVersion=null&version=soljson-v0.8.7+commit.e28d00a7.js


# Node

Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_node.py <br/>

![image](https://user-images.githubusercontent.com/72211145/161927123-991c1f12-4ab0-4536-9f74-299ff6468e9b.png)


# Peer

Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_peer.py <br/>

![image](https://user-images.githubusercontent.com/72211145/161927045-814770e0-eba9-41df-a3dc-b57d0859c3eb.png)


# Admin

Download project source code from github <br/>
pip install -r requirements.txt <br/>
python main_admin.py <br/>

![image](https://user-images.githubusercontent.com/72211145/161927177-6e1cd112-4d54-4c2c-b556-43d64590ae4d.png)

