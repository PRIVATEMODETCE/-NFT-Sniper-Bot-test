import os
import pandas as pd
from cryptography.fernet import Fernet
from ton import Wallet, TonClient

class WalletManager:
    def __init__(self):
        self.encryption_key = self.load_encryption_key()
        self.wallet_file = "wallet.csv"
        self.client = TonClient(network="mainnet")

    def load_encryption_key(self):
        if not os.path.exists("encryption.key"):
            key = Fernet.generate_key()
            with open("encryption.key", "wb") as key_file:
                key_file.write(key)
        with open("encryption.key", "rb") as key_file:
            return Fernet(key_file.read())

    def create_wallet(self):
        wallet = Wallet.create_new_wallet()
        encrypted_key = Fernet(self.encryption_key).encrypt(wallet.private_key.encode()).decode()

        data = {
            "address": wallet.address,
            "private_key": encrypted_key,
            "public_key": wallet.public_key,
            "balance": 0
        }
        df = pd.DataFrame([data])
        if not os.path.exists(self.wallet_file):
            df.to_csv(self.wallet_file, index=False)
        else:
            df.to_csv(self.wallet_file, mode='a', header=False, index=False)
        return wallet.address

    def load_wallet(self, address=None):
        if not os.path.exists(self.wallet_file):
            return None
        wallets = pd.read_csv(self.wallet_file)
        if address:
            wallet_data = wallets[wallets["address"] == address]
        else:
            wallet_data = wallets.iloc[0]  # Load the first wallet by default

        if wallet_data.empty:
            return None
        private_key_encrypted = wallet_data.iloc[0]["private_key"]
        private_key = Fernet(self.encryption_key).decrypt(private_key_encrypted.encode()).decode()
        return Wallet(private_key=private_key)

    def check_balance(self, wallet):
        balance = self.client.get_balance(wallet.address)
        return balance

    def send_transaction(self, wallet, recipient_address, amount):
        try:
            transaction = wallet.create_transaction(to_address=recipient_address, amount=amount)
            result = self.client.send_transaction(transaction)
            return result
        except Exception as e:
            return str(e)
