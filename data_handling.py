import hashlib

def encrypt_data(data):
    # Very basic encryption. In reality, you'd use something like AES with proper key management
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()

def decrypt_data(encrypted_data, buyer_address):
    # This is a placeholder. In a real scenario, you'd use the buyer's private key to decrypt:
    return json.dumps({"decrypted": f"Data for {buyer_address}"})  # Mock data
