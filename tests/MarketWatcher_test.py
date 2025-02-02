import unittest
from unittest.mock import MagicMock, patch

from src.MarketWatcher import MarketWatcher
from src.XPath import XPath

class MockElement():
    def __init__(self, attr, data):
        self.attr = attr
        self.data = data
    
    def get_attribute(self, attr):
        if attr == self.attr:
            return self.data

class MockDriver():
    def __init__(self, url, padding=False, data={}):
        self.url = url
        self.padding = padding
        self.data = data
    
    def get(self, *args):
        pass
    
    def find_element(self, method, xpath):
        product = "Magic" if "/Magic/" in self.url else "other"
        any_version = "/Cards/" in self.url
        xp = XPath(product, any_version=any_version, padding=self.padding)
        if xpath == xp.trend_price[0]:
            return MockElement(xp.trend_price[1], self.data["trend"])
        elif xpath == xp.lowest_price[0]:
            return MockElement(xp.lowest_price[1], self.data["lowest"])
        elif xpath == xp.seller_location[0]:
            return MockElement(xp.seller_location[1], self.data["location"])
        elif xpath == xp.card_version[0]:
            return MockElement(xp.card_version[1], self.data["version"])
        elif xpath == xp.card_condition[0]:
            return MockElement(xp.card_condition[1], self.data["condition"])
        elif xpath == xp.card_language[0]:
            return MockElement(xp.card_language[1], self.data["language"])
        elif xpath == xp.padding_check[0]:
            return MockElement(xp.padding_check[1], "anything" if self.padding else "available items")

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
    
    @patch("src.MarketWatcher.sleep")
    def test_get_market_value(self, sleep_mock):
        url = "test/Magic/Cards/test"
        driver = MockDriver(url, padding=False, data={
            "trend": "1,23 €",
            "lowest": "3,21 €",
            "location": "Seller location: Somewhere",
            "version": "A Version",
            "condition": "Damaged",
            "language": "German"
        })
        values = MarketWatcher.get_card_market_values(driver, url)
        self.assertEqual(values["avg"], 1.23)
        self.assertEqual(values["min"], 3.21)
        self.assertEqual(values["seller_location"], "Somewhere")
        self.assertEqual(values["condition"], "Damaged")
        self.assertEqual(values["version"], "A Version")
        self.assertEqual(values["language"], "German")

        # broken data
        url = "test/test.com"
        driver = MockDriver(url, padding=True, data={
            "trend": "1,23 €",
            "lowest": "3,21 €",
            "location": "Seller location Somewhere",
            "version": "A Version",
            "condition": "Damaged",
            "language": "German"
        })
        values = MarketWatcher.get_card_market_values(driver, url)
        self.assertEqual(values["avg"], 0)
        self.assertEqual(values["min"], 0)
        self.assertEqual(values["seller_location"], "")
        self.assertEqual(values["condition"], "")
        self.assertEqual(values["version"], "")
        self.assertEqual(values["language"], "")
    
    def test_create_cardmarket_link(self):
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "cardversion/card", "1", "2", "3"),
            "https://www.cardmarket.com/en/Magic/Products/Singles/cardversion/card?minCondition=2&sellerCountry=3&language=1"
        )
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "cardversion/card", "any", "2", "3"),
            "https://www.cardmarket.com/en/Magic/Products/Singles/cardversion/card?minCondition=2&sellerCountry=3"
        )
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "card", "any", "2", "3"),
            "https://www.cardmarket.com/en/Magic/Cards/card?minCondition=2&sellerCountry=3"
        )
        

        