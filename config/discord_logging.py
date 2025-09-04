import logging
import traceback
import requests
from django.conf import settings

DISCORD_MAX = 1900  # 디스코드 content 제한(2,000) 고려해 안전컷


class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url=None, level=logging.ERROR):
        super().__init__(level)
        self.webhook_url = settings.DISCORD_WEBHOOK_URL
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL is not set")

    def emit(self, record: logging.LogRecord):
        if getattr(settings, "DISABLE_DISCORD_LOGS", False):
            return

        try:
            # 기본 메시지
            msg = self.format(record)

            # 예외가 있으면 traceback 붙이기
            if record.exc_info:
                tb = "".join(traceback.format_exception(*record.exc_info))
                msg = f"{msg}\n```{tb[-DISCORD_MAX:]}```"

            content = f"**[{record.levelname}] {record.name}**\n{msg}"
            if len(content) > DISCORD_MAX:
                content = content[-DISCORD_MAX:]

            requests.post(self.webhook_url, json={"content": content}, timeout=2)
        except Exception:
            # 로깅 중 에러는 절대 예외 전파하지 않음
            pass
