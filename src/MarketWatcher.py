from .Discord import Discord
from .Config import Config
from .Helpers import pc_alert, create_logger, get_wait_time
from time import sleep

class MarketWatcher():
    def __init__(self):
        self.logger = create_logger("MarketWatcher", "logs/market_watcher.log")
        self.config = Config()
        self.discord = Discord(self.config.discord_token)
        self.running = False
        self._wait_time = get_wait_time()

    def send_alert(self, title: str = "title", message: str = "message", alert: list = [], channels: list = ["default"], link: str = ""):
        if "discord" in alert:
            for channel in channels:
                ok = self.discord.send_message(message, self.config.discord_channels[channel])
                if not ok:
                    self.logger.error("Failed to send discord message")
        if "pc" in alert:
            pc_alert(title, message, link)

    def single_run(self):
        self.running = False
    
    def run(self):
        self.logger.info("Starting MarketWatcher")
        self.running = True
        while self.running:
            self.single_run()
            if self.running is False:
                break
            sleep(self._wait_time)
        
        self.logger.info("Stopping MarketWatcher")


