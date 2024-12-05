from telegram import Bot

class TelegramBot:
    def __init__(self, bot_token, chat_id):
        """مقداردهی اولیه ربات تلگرام"""
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    def send_message(self, message):
        """ارسال پیام متنی به تلگرام"""
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
            print("Message sent successfully!")
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_file(self, file_path, caption=""):
        """ارسال فایل به تلگرام"""
        try:
            with open(file_path, "rb") as file:
                self.bot.send_document(chat_id=self.chat_id, document=file, caption=caption)
            print("File sent successfully!")
        except Exception as e:
            print(f"Error sending file: {e}")
