from .DiscordAPI import DiscordAPI

class Discord(DiscordAPI):
    def __init__(self, auth_token=None):
        super().__init__(auth_token)

    def send_message(self, content, channel_id):
        return self.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", content)  
