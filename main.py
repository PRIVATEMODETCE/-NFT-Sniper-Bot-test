import streamlit as st
from wallet_manager import WalletManager
from nft_monitor import NFTMonitor
from auto_purchase import AutoPurchase
from telegram_bot import TelegramBot
import pandas as pd
import os

# مقداردهی اولیه ماژول‌ها
wallet_manager = WalletManager()
nft_monitor = NFTMonitor()
auto_purchase = AutoPurchase()
telegram_bot = TelegramBot(bot_token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

# تنظیمات صفحه اصلی Streamlit
st.set_page_config(
    page_title="NFT Sniper Bot",
    page_icon="🎯",
    layout="wide",
)

# عنوان اصلی
st.title("🎯 NFT Sniper Bot")
st.markdown("### ابزاری برای خرید و مدیریت NFT در شبکه TON")

# منوی کناری
st.sidebar.header("📂 منوی اصلی")
menu = st.sidebar.radio("انتخاب کنید:", ["مدیریت کیف پول", "پایش بازار", "خرید خودکار", "مدیریت بازارها", "گزارش‌دهی تلگرام"])

# صفحات مختلف بر اساس انتخاب
if menu == "مدیریت کیف پول":
    st.header("🔑 مدیریت کیف پول")
    with st.expander("🔹 ایجاد کیف پول جدید"):
        if st.button("ایجاد کیف پول"):
            new_wallet = wallet_manager.create_wallet()
            st.success(f"کیف پول جدید ایجاد شد: {new_wallet}")

    with st.expander("🔹 بارگذاری کیف پول موجود"):
        if st.button("بارگذاری کیف پول"):
            wallet = wallet_manager.load_wallet()
            if wallet:
                balance = wallet_manager.check_balance(wallet)
                st.info(f"آدرس کیف پول: `{wallet.address}`\nموجودی: `{balance} TON`")
            else:
                st.error("هیچ کیف پولی یافت نشد!")

if menu == "پایش بازار":
    st.header("📊 پایش بازار NFT")
    if st.button("اجرای پایش"):
        nft_monitor.fetch_all_markets()
        st.success("پایش بازارها با موفقیت انجام شد!")

    with st.expander("🔹 داده‌های پایش‌شده"):
        nft_data = pd.read_csv("nft_data.csv") if os.path.exists("nft_data.csv") else pd.DataFrame()
        if not nft_data.empty:
            st.dataframe(nft_data)
        else:
            st.info("هیچ داده‌ای برای نمایش موجود نیست.")

if menu == "خرید خودکار":
    st.header("🤖 خرید خودکار NFT")
    if st.button("اجرای خرید خودکار"):
        auto_purchase.execute_purchases()
        st.success("خرید خودکار با موفقیت اجرا شد!")

    with st.expander("🔹 تاریخچه تراکنش‌ها"):
        transactions = pd.read_csv("transactions.csv") if os.path.exists("transactions.csv") else pd.DataFrame()
        if not transactions.empty:
            st.dataframe(transactions)
        else:
            st.info("هیچ تراکنشی برای نمایش موجود نیست.")

if menu == "مدیریت بازارها":
    st.header("🛒 مدیریت بازارهای NFT")
    with st.expander("🔹 مشاهده بازارهای موجود"):
        markets = pd.read_csv("markets.csv") if os.path.exists("markets.csv") else pd.DataFrame()
        if not markets.empty:
            st.dataframe(markets)
        else:
            st.info("هیچ بازاری ثبت نشده است.")

    with st.expander("🔹 افزودن بازار جدید"):
        market_name = st.text_input("نام بازار:")
        api_url = st.text_input("API URL:")
        sdk_supported = st.selectbox("پشتیبانی از SDK:", [True, False])

        if st.button("افزودن بازار"):
            new_market = {"market_name": market_name, "api_url": api_url, "sdk_supported": sdk_supported}
            markets = markets.append(new_market, ignore_index=True)
            markets.to_csv("markets.csv", index=False)
            st.success(f"بازار '{market_name}' با موفقیت افزوده شد!")

if menu == "گزارش‌دهی تلگرام":
    st.header("📤 گزارش‌دهی تلگرام")
    with st.expander("🔹 ارسال پیام تست"):
        if st.button("ارسال پیام تست"):
            telegram_bot.send_message("پیام تست از NFT Sniper Bot!")
            st.success("پیام تست ارسال شد.")

    with st.expander("🔹 ارسال گزارش تراکنش‌ها"):
        if st.button("ارسال فایل گزارش"):
            telegram_bot.send_file("transactions.csv", caption="گزارش تراکنش‌ها")
            st.success("گزارش تراکنش‌ها به تلگرام ارسال شد!")
