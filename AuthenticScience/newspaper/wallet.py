from web3 import Web3

#creates a new address and the relative priavate key
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/17b153bb0c384e5995ee7a12b450370e'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f'Your adress: {address} \n Your Key: {privateKey}')