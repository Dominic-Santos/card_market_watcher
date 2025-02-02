import unittest
from unittest.mock import MagicMock, patch

from src.MarketWatcher import MarketWatcher

class TestMarketWatcher(unittest.TestCase):  
    @patch("src.MarketWatcher.get_cards_location", return_value="tests/testdata/cards.json")
    @patch("src.MarketWatcher.get_data_location", return_value="tests/testdata/data.json")
    def test_init(self, *args):
        market_watcher = MarketWatcher()
        self.assertFalse(market_watcher.running)
        self.assertEqual(len(market_watcher.card_db.cards), 2)
        self.assertEqual(market_watcher.card_db.cards[0].name, "testcard")
        self.assertEqual(market_watcher.card_db.cards[0].data, {})

    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.pc_alert")
    def test_send_alert(self, mock_pc_alert, mock_reload_db):
        market_watcher = MarketWatcher()
        market_watcher.logger.error = MagicMock()

        market_watcher.discord.send_message = lambda x, y: True
        market_watcher.send_alert("title", "message", ["discord"], link="http://example.com")
        market_watcher.logger.error.assert_not_called()
        mock_pc_alert.assert_not_called()

        market_watcher.discord.send_message = lambda x, y: False
        market_watcher.send_alert("title", "message", ["discord", "pc"], link="http://example.com")
        market_watcher.logger.error.assert_called_with("Failed to send discord message")
        mock_pc_alert.assert_called_with("title", "message", "http://example.com")

        