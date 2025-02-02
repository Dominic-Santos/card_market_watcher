from src.Helpers import load_json, save_json

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.load()
        self.save()

    def load(self):
        raw_config = load_json(CONFIG_FILE)
        self._config = {
            "discord_token": raw_config.get("discord_token", None),
            "discord_channels": raw_config.get("discord_channels", {
                "default": None
            }),
        }
    
    def save(self):
        save_json(CONFIG_FILE, self._config)

    @property
    def discord_token(self):
        return self._config["discord_token"]
    
    @property
    def discord_channels(self):
        return self._config["discord_channels"]

    @property
    def discord_channel_names(self):
        return list(self._config["discord_channels"].keys())

    def discord_channel_by_name(self, name: str):
        return self._config["discord_channels"].get(name, "")
