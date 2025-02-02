import unittest
from src.Config import Config
from unittest.mock import patch


class TestConfig(unittest.TestCase):
    
    @patch("src.Config.save_json")
    @patch("src.Config.load_json")
    def test_config(self, mock_load_json, *args):
        mock_load_json.return_value = {
            "discord_token": "test_token",
            "discord_channels": {
                "default": "test_channel"
            }
        }
        config = Config()
        self.assertEqual(config.discord_token, "test_token")
        self.assertEqual(config.discord_channels, {"default": "test_channel"})
        self.assertEqual(config.discord_channel_names, ["default"])
        self.assertEqual(config.discord_channel_by_name("default"), "test_channel")
