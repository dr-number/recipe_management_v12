from logging import FileHandler, LogRecord


class TelegramFileHandler(FileHandler):
    BLACK_LIST_OF_WORDS = [
        "You may need to add '0.0.0.0' to ALLOWED_HOSTS.",
        "tornado.application",
    ]

    def emit(self, record: LogRecord) -> None:
        from app.helpers import telegram_bot_send_msg
        from app.settings import BOT_TOKEN, DEBUG, ERRORS_CHAT_ID
        msg = self.format(record)

        if BOT_TOKEN and not any(word in msg for word in self.BLACK_LIST_OF_WORDS):
            msg = f'recipe: {msg}'
            telegram_bot_send_msg(
                chat_id=ERRORS_CHAT_ID, 
                text=msg[:300], 
                document=msg,
            )

        return super().emit(record)
