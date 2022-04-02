from web3 import Web3

ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = "0xd38F44fB75D74De33C75B536583ac473506cFcBE"
account_2 = "0x8E71CD05e43297a3E24935ebA038F5112e563143"

private_key = "2b42918679ee3a218197ac878e43353757267de4cee4134a90f6440e93f9ea2e"
nonce = web3.eth.getTransactionCount(account_1)
tx = {
    'nonce':nonce,
    'to': account_2,
    'value': web3.toWei(1,'ether'),
    'gas': 2000000,
    'gasPrice' :web3.toWei('50','gwei')
}

signed_tx = web3.eth.account.signTransaction(tx,private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(web3.toHex(tx_hash))
