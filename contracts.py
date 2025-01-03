from web3 import Web3

class DataMarketplaceContract:
    def __init__(self, web3, address):
        self.w3 = web3
        self.contract = web3.eth.contract(address=address, abi=...)  # ABI would be loaded from a JSON file in practice

    def list_data(self, data_id, price, data_hash):
        tx = self.contract.functions.listData(data_id, price, data_hash).buildTransaction({
            'from': self.w3.eth.accounts[0],  # Assume the first account is the seller
            'gas': 2000000,
            'gasPrice': self.w3.toWei('20', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key='...')  # Seller's private key
        return self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def buy_data(self, data_id, buyer_address):
        tx = self.contract.functions.buyData(data_id).buildTransaction({
            'from': buyer_address,
            'value': self.w3.toWei(100, 'ether'),  # Assuming price is 100 ETH for simplicity
            'gas': 2000000,
            'gasPrice': self.w3.toWei('20', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key='...')  # Buyer's private key
        return self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    def get_data(self, data_id):
        # This would call a smart contract function to retrieve data. 
        # In practice, this would involve some form of access control or decryption.
        return self.contract.functions.getData(data_id).call()

    def get_all_listings(self):
        # Retrieve all listings from the contract
        return self.contract.functions.getAllListings().call()
