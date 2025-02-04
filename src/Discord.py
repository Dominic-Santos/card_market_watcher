from .DiscordAPI import DiscordAPI

Reaction_Emojis = {
    "check": "%E2%9C%85",
    "cross": "%E2%9D%8C"
}

class Discord(DiscordAPI):
    api_base = "https://discord.com/api/v9/channels"
    def __init__(self, auth_token=None):
        super().__init__(auth_token)

    def send_message(self, content, channel_id):
        return self.post(f"{self.api_base}/{channel_id}/messages", content)

    def react_to_message(self, reaction, channel_id, message_id):
        emoji = Reaction_Emojis[reaction]
        return self.put(f"{self.api_base}/{channel_id}/messages/{message_id}/reactions/{emoji}/%40me?location=Message Context Menu&type=0")

    def get_message_reaction_users(self, reaction, channel_id, message_id):
        emoji = Reaction_Emojis[reaction]
        return self.get(f"{self.api_base}/{channel_id}/messages/{message_id}/reactions/{emoji}?type=0")
