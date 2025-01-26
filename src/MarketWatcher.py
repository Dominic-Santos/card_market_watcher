from .Discord import Discord
from .Config import Config
from .Helpers import pc_alert, create_logger

class MarketWatcher():
    def __init__(self):
        self.logger = create_logger("MarketWatcher", "logs/market_watcher.log")
        self.config = Config()
        self.discord = Discord(self.config.discord_token)

    def send_alert(self, title: str = "title", message: str = "message", alert: list = [], channels: list = ["default"], link: str = ""):
        if "discord" in alert:
            for channel in channels:
                ok = self.discord.send_message(message, self.config.discord_channels[channel])
                if not ok:
                    self.logger.error("Failed to send discord message")
        if "pc" in alert:
            pc_alert(title, message, link)

