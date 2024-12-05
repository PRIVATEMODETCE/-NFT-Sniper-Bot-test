import pandas as pd
import re
from datetime import datetime
from wallet_manager import WalletManager


class AutoPurchase:
    def __init__(self):
        self.pattern_file = "patterns.csv"
        self.transaction_file = "transactions.csv"
        self.nft_file = "nft_data.csv"
        self.floor_price_file = "floor_prices.csv"
        self.wallet_manager = WalletManager()

    def load_patterns(self):
        """بارگذاری الگوهای خرید"""
        if not os.path.exists(self.pattern_file):
            return pd.DataFrame(columns=["pattern", "max_price"])
        return pd.read_csv(self.pattern_file)

    def load_floor_prices(self):
        """بارگذاری قیمت کف تعیین‌شده توسط کاربر"""
        if not os.path.exists(self.floor_price_file):
            return pd.DataFrame(columns=["collection", "floor_price"])
        return pd.read_csv(self.floor_price_file)

    def load_nft_data(self):
        """بارگذاری داده‌های توکن‌ها"""
        if not os.path.exists(self.nft_file):
            return pd.DataFrame(columns=["market", "collection", "nft_id", "price", "timestamp"])
        return pd.read_csv(self.nft_file)

    def match_conditions(self, nft, patterns, floor_prices):
        """بررسی شرایط خرید"""
        # بررسی قیمت کف
        floor_price_row = floor_prices[floor_prices["collection"] == nft["collection"]]
        if floor_price_row.empty:
            return False
        floor_price = floor_price_row.iloc[0]["floor_price"]
        if nft["price"] > floor_price:
            return False

        # بررسی تطبیق با الگوها
        for _, pattern in patterns.iterrows():
            if re.search(pattern["pattern"], nft["collection"]) and nft["price"] <= pattern["max_price"]:
                return True
        return False

    def execute_purchases(self):
        """اجرای فرآیند خرید خودکار"""
        patterns = self.load_patterns()
        floor_prices = self.load_floor_prices()
        nfts = self.load_nft_data()

        if nfts.empty or patterns.empty or floor_prices.empty:
            print("No data available for purchase.")
            return

        wallet = self.wallet_manager.load_wallet()
        if not wallet:
            print("No wallet loaded.")
            return

        for _, nft in nfts.iterrows():
            if self.match_conditions(nft, patterns, floor_prices):
                print(f"Purchasing NFT: {nft['nft_id']} from {nft['collection']}")
                result = self.wallet_manager.send_transaction(wallet, nft["nft_id"], nft["price"])
                self.log_transaction(nft, "Successful" if result else "Failed")

    def log_transaction(self, nft, status):
        """ثبت وضعیت خرید"""
        data = {
            "date": datetime.now().isoformat(),
            "collection": nft["collection"],
            "price": nft["price"],
            "status": status,
            "nft_id": nft["nft_id"],
            "market": nft["market"]
        }
        df = pd.DataFrame([data])
        if not os.path.exists(self.transaction_file):
            df.to_csv(self.transaction_file, index=False)
        else:
            df.to_csv(self.transaction_file, mode='a', header=False, index=False)
