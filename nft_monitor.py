from pytoniq import TonClient  # نمونه SDK
import os
import pandas as pd
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class NFTMonitor:
    def __init__(self):
        self.nft_file = "nft_data.csv"
        self.market_file = "markets.csv"
        self.client = TonClient(network="mainnet")  # نمونه استفاده از SDK برای TON

    def initialize_market_file(self):
        """ایجاد فایل بازارها در صورت عدم وجود"""
        if not os.path.exists(self.market_file):
            pd.DataFrame(columns=["market_name", "api_url", "sdk_supported"]).to_csv(self.market_file, index=False)

    def fetch_all_markets(self):
        """دریافت داده‌ها از تمامی بازارهای ثبت‌شده"""
        if not os.path.exists(self.market_file):
            print("No markets available. Please add markets first.")
            return

        markets = pd.read_csv(self.market_file)
        if markets.empty:
            print("Market file is empty. Please add markets first.")
            return

        # اجرای همزمان برای دریافت داده‌های بازارها
        with ThreadPoolExecutor() as executor:
            executor.map(self.fetch_market_data, markets.to_dict(orient="records"))

    def fetch_market_data(self, market):
        """دریافت داده‌های یک بازار خاص"""
        if market["sdk_supported"]:
            self.fetch_via_sdk(market["market_name"])
        else:
            self.fetch_via_api(market["market_name"], market["api_url"])

    def fetch_via_api(self, market_name, api_url):
        """دریافت داده از طریق API"""
        if not api_url:
            print(f"API URL for {market_name} is missing.")
            return
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            nfts = [
                {
                    "market": market_name,
                    "collection": nft.get("collection_name"),
                    "nft_id": nft.get("id"),
                    "price": nft.get("price"),
                    "timestamp": datetime.now().isoformat()
                }
                for nft in data.get("nfts", [])
            ]
            self.save_to_csv(pd.DataFrame(nfts))
            print(f"Data from {market_name} (API) fetched successfully.")
        except Exception as e:
            print(f"Error fetching data from {market_name} (API): {e}")

    def fetch_via_sdk(self, market_name):
        """دریافت داده از طریق SDK"""
        try:
            # این فقط یک مثال است. تابع SDK باید برای هر بازار خاص تعریف شود.
            data = self.client.get_market_data(market_name)  # تابع فرضی در SDK
            nfts = [
                {
                    "market": market_name,
                    "collection": nft["collection_name"],
                    "nft_id": nft["id"],
                    "price": nft["price"],
                    "timestamp": datetime.now().isoformat()
                }
                for nft in data
            ]
            self.save_to_csv(pd.DataFrame(nfts))
            print(f"Data from {market_name} (SDK) fetched successfully.")
        except Exception as e:
            print(f"Error fetching data from {market_name} (SDK): {e}")

    def save_to_csv(self, df):
        """ذخیره داده‌های NFT در فایل"""
        if not os.path.exists(self.nft_file):
            df.to_csv(self.nft_file, index=False)
        else:
            df.to_csv(self.nft_file, mode='a', header=False, index=False)
