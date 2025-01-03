from web3 import Web3
from contracts import DataMarketplaceContract
from data_handling import encrypt_data, decrypt_data
import json

class MezmeAgent:
    def __init__(self, web3, contract_address):
        self.web3 = web3
        self.contract = DataMarketplaceContract(web3, contract_address)

    def list_data(self, data_id, price, data_description):
        """List data for sale on the marketplace."""
        data_hash = encrypt_data(data_description)  # Hash or encrypt the description for privacy
        tx_hash = self.contract.list_data(data_id, price, data_hash)
        print(f"Data listed with transaction hash: {tx_hash.hex()}")

    def buy_data(self, data_id, buyer_address):
        """Buy data from the marketplace."""
        tx_hash = self.contract.buy_data(data_id, buyer_address)
        print(f"Data purchase initiated with transaction hash: {tx_hash.hex()}")
        # Here, we'd typically wait for the transaction to be mined
        return tx_hash

    def retrieve_data(self, data_id, buyer_address):
        """Retrieve the actual data after purchase."""
        data_encrypted = self.contract.get_data(data_id)
        if data_encrypted:
            # Decrypt data with buyer's key (in practice, this would be more complex)
            data_decrypted = decrypt_data(data_encrypted, buyer_address)
            return json.loads(data_decrypted)  # Assuming data was stored as JSON
        else:
            return None

    def check_listings(self):
        """Check current data listings."""
        listings = self.contract.get_all_listings()
        return listings

if __name__ == "__main__":
    # Setup Web3 connection (in practice, this would connect to a real or testnet blockchain)
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Example local Ganache blockchain
    
    # Assume we have deployed our contract and know its address
    contract_address = '0x1234567890123456789012345678901234567890'  # Example address
    
    # Initialize agents
    seller_agent = MezmeAgent(w3, contract_address)
    buyer_agent = MezmeAgent(w3, contract_address)
    
    # Seller action
    seller_agent.list_data("data_001", 100, {"description": "Weather data for NYC", "dataset_size": "100MB"})

    # Buyer actions
    listings = buyer_agent.check_listings()
    if listings:
        print("Available listings:", listings)
        # Assume the buyer wants to buy the first listing
        tx_hash = buyer_agent.buy_data(listings[0]['data_id'], '0xabcdef...')  # Example buyer address
        # Wait for transaction confirmation (simplified here)
        # In practice, you'd wait for the tx to be mined and check if it was successful
        data = buyer_agent.retrieve_data(listings[0]['data_id'], '0xabcdef...')
        if data:
            print("Retrieved data:", data)
        else:
            print("Failed to retrieve data or data not available.")
    else:
        print("No listings available.")
