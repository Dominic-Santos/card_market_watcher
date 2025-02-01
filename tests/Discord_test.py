import unittest
from unittest.mock import patch

from src.Discord import Discord

TEST_AUTH_TOKEN = "test_token"

class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
    
    def json(self):
        return {"status": self.status_code}

class TestDiscord(unittest.TestCase):
    @patch("src.Discord.DiscordAPI.post")
    def test_send_message(self, mock_post):
        discord = Discord()
        discord.send_message("test", "123")
        mock_post.assert_called_with("https://discord.com/api/v9/channels/123/messages", "test")
    
    def test_headers(self):
        discord = Discord(TEST_AUTH_TOKEN)
        self.assertEqual(discord.get_headers(), {"Authorization": TEST_AUTH_TOKEN})
    
    def test_check_content(self):
        discord = Discord()
        self.assertTrue(discord.check_content("test"))
        self.assertFalse(discord.check_content("a" * 2001))

    def test_check_can_send(self):
        discord = Discord(TEST_AUTH_TOKEN)
        self.assertTrue(discord.check_can_send("test"))
        self.assertFalse(discord.check_can_send("a" * 2001))
        discord = Discord()
        self.assertFalse(discord.check_can_send("test"))

    @patch("src.DiscordAPI.requests.post")
    def test_post(self, mock_post):
        mock_post.return_value = MockResponse(200)
        discord = Discord(TEST_AUTH_TOKEN)
        self.assertEqual(discord.post("test_url", "test_content"), 200)
        self.assertEqual(discord.post("test_url", "test_content", "file"), 200)
        self.assertEqual(discord.post("test_url", "a" * 2001), False)
        discord = Discord()
        self.assertEqual(discord.post("test_url", "test_content"), False)
    
    @patch("src.DiscordAPI.requests.get")
    def test_get(self, mock_get):
        mock_get.return_value = MockResponse(200)
        discord = Discord(TEST_AUTH_TOKEN)
        self.assertEqual(discord.get("test_url"), {"status": 200})
        discord = Discord()
        self.assertEqual(discord.get("test_url"), False)

    @patch("src.DiscordAPI.requests.delete")
    def test_delete(self, mock_delete):
        mock_delete.return_value = MockResponse(204)
        discord = Discord(TEST_AUTH_TOKEN)
        self.assertTrue(discord.delete("test_url"))
        discord = Discord()
        self.assertFalse(discord.delete("test_url"))
