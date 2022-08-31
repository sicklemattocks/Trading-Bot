from web3 import Web3
import config
import routerabi
import admcabi
import time
import addresses
import json

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
if (web3.isConnected()) == True:
    print('Swapping Admc to Bnb')

panRouterContractAddress = addresses.router_address #router address
panabi = routerabi.abi #router abi
sender_address = addresses.address1 #personal address
balance = web3.eth.get_balance(sender_address) #address balance
human_readable = web3.fromWei(balance,'ether') #convert decimals
print('Initial Contract Bnb Balance:', round(human_readable, 4))

spend = web3.toChecksumAddress(addresses.admc) #admc contract
token_to_buy = web3.toChecksumAddress(addresses.wbnb)  #wbnb contract

routerabi = web3.eth.contract(address=panRouterContractAddress, abi=panabi) #new contract instance
nonce = web3.eth.get_transaction_count(sender_address) 
start = time.time()

pancakeswap2_txn = routerabi.functions.swapTokensForExactETH(
100000000000000000, 1000000000000000000000,[spend,token_to_buy],sender_address, 1000000000000000000
).buildTransaction({
'from': sender_address,
'value': web3.toWei(0,'ether'), #how much to trade
'gas': 1500000,
'gasPrice': web3.toWei('5','gwei'),
'nonce': nonce,
})

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, config.private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print('Transaction Hash:',web3.toHex(tx_token))