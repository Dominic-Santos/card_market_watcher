import unittest
from unittest.mock import MagicMock, patch

from src.MarketWatcher import MarketWatcher
from src.XPath import XPath
from src.Card import Card

class MockElement():
    def __init__(self, attr, data):
        self.attr = attr
        self.data = data
    
    def get_attribute(self, attr):
        if attr == self.attr:
            return self.data

class MockDriver():
    def __init__(self, url, padding=False, data={}, interupt=False):
        self.url = url
        self.padding = padding
        self.data = data
        self.interupt = interupt
    
    def get(self, *args):
        pass
    
    def find_element(self, method, xpath):
        if self.interupt:
            raise KeyboardInterrupt("get out")
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

def mock_single_run(self):
    self.count += 1
    if self.count == 2:
        self.running = False

def raise_keyboard_interupt(*args):
    raise KeyboardInterrupt("test")

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

        driver = MockDriver(url, padding=True, interupt=True, data={
            "trend": "1,23 €",
            "lowest": "3,21 €",
            "location": "Seller location Somewhere",
            "version": "A Version",
            "condition": "Damaged",
            "language": "German"
        })
        values = MarketWatcher.get_card_market_values(driver, url)
        self.assertIsNone(values)
    
    def test_create_cardmarket_link(self):
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "cardversion/card", "1", "2", "3"),
            "https://www.cardmarket.com/en/Magic/Products/Singles/cardversion/card?sellerCountry=3&language=1&minCondition=2"
        )
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "cardversion/card", "any", "2", "3"),
            "https://www.cardmarket.com/en/Magic/Products/Singles/cardversion/card?sellerCountry=3&minCondition=2"
        )
        self.assertEqual(
            MarketWatcher.create_cardmarket_link("Magic", "card", "any", "any", "3"),
            "https://www.cardmarket.com/en/Magic/Cards/card?sellerCountry=3"
        )
    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.MarketWatcher.single_run", mock_single_run)
    @patch("src.MarketWatcher.sleep")
    def test_run(self, mock_sleep, *args):
        market_watcher = MarketWatcher()
        market_watcher.count = 0
        market_watcher.logger.info = MagicMock()

        market_watcher.logger.info.assert_not_called()
        market_watcher.run()
        self.assertEqual(market_watcher.logger.info.call_count, 2)
        self.assertEqual(market_watcher.count, 2)
        self.assertEqual(mock_sleep.call_count, 1)
    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.MarketWatcher.single_run")
    @patch("src.MarketWatcher.sleep", raise_keyboard_interupt)
    def test_run_interupt(self, *args):
        market_watcher = MarketWatcher()
        market_watcher.logger.info = MagicMock()

        market_watcher.logger.info.assert_not_called()
        market_watcher.run()
        self.assertEqual(market_watcher.logger.info.call_count, 2)
    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.MarketWatcher.send_alert")
    @patch("src.MarketWatcher.MarketWatcher.single_run_main")
    @patch("src.MarketWatcher.webdriver.Chrome")
    def test_single_run(self, mock_driver, *args):
        driver = MagicMock()
        mock_driver.return_value = driver
        market_watcher = MarketWatcher()
        market_watcher.running = True
        market_watcher.single_run()

        self.assertEqual(mock_driver.call_count, 1)
        self.assertEqual(driver.quit.call_count, 1)
        self.assertTrue(market_watcher.running)

        market_watcher.single_run_main = raise_keyboard_interupt
        market_watcher.single_run()

        self.assertEqual(mock_driver.call_count, 2)
        self.assertEqual(driver.quit.call_count, 1)
        self.assertFalse(market_watcher.running)
    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.sleep")
    @patch("src.MarketWatcher.MarketWatcher.get_card_market_values")
    def test_get_card_value(self, mock_get_values, mock_sleep, *args):
        mock_get_values.return_value = None
        market_watcher = MarketWatcher()
        fields = {
            "links": ["http://example.com", "http://example2.com"],
            "note": "Test note",
            "alert": ["pc", "discord"],
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "seller": "1"
        }
        card = Card("testcard", fields)
        market_watcher.running = True
        values = market_watcher.get_card_values(None, card)
        self.assertIsNone(values)
        self.assertFalse(market_watcher.running)
        self.assertEqual(mock_get_values.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

        mock_get_values.return_value = {"min": 0}
        with self.assertRaises(Exception):
            market_watcher.get_card_values(None, card)
        self.assertEqual(mock_get_values.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 0)

        mock_get_values.return_value = {"min": 123}
        values = market_watcher.get_card_values(None, card)
        self.assertEqual(mock_get_values.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 1)
    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    def test_get_price_change_message(self, *args):
        market_watcher = MarketWatcher()
        fields = {
            "links": ["http://example.com", "http://example2.com"],
            "note": "Test note",
            "alert": ["pc", "discord"],
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "seller": "1"
        }
        card = Card("testcard", fields)
        card.data = {
            "2021-01-01": {"min": 1, "avg": 2},
            "2021-01-02": {"min": 2, "avg": 3},
            "2021-01-03": {"min": 3, "avg": 4},
        }

        changes, msg, log = market_watcher.get_price_change_message(card, {"min": 3, "avg": 4}, 0)
        self.assertFalse(changes)
        self.assertIsNone(msg)
        self.assertEqual(log, "testcard | Low 01.00 | Min 03.00, Avg 04.00")

        changes, msg, log = market_watcher.get_price_change_message(card, {"min": 1, "avg": 2, "version": "ver", "condition": "mang", "language": "bleh", "seller_location": "nope"}, 0)
        self.assertTrue(changes)
        self.assertEqual(msg, "testcard went down, is currently 1, lowest seen\n(lowest seen: 1)\nver\n[mang] bleh from nope")
        self.assertEqual(log, "testcard | Low 01.00 | Min 03.00, Avg 04.00 | Down | Min 01.00, Avg 02.00" )

        changes, _, log = market_watcher.get_price_change_message(card, {"min": 3, "avg": 3, "version": "ver", "condition": "mang", "language": "bleh", "seller_location": "nope"}, 0)
        self.assertTrue(changes)
        self.assertEqual(log, "testcard | Low 01.00 | Min 03.00, Avg 04.00 | Down | Min 03.00, Avg 03.00" )

        changes, _, log = market_watcher.get_price_change_message(card, {"min": 5, "avg": 5, "version": "ver", "condition": "mang", "language": "bleh", "seller_location": "nope"}, 0)
        self.assertTrue(changes)
        self.assertEqual(log, "testcard | Low 01.00 | Min 03.00, Avg 04.00 |  Up  | Min 05.00, Avg 05.00" )

        changes, msg, _ = market_watcher.get_price_change_message(card, {"min": 0.5, "avg": 2, "version": "ver", "condition": "mang", "language": "bleh", "seller_location": "nope"}, 0)
        self.assertTrue(changes)
        self.assertEqual(msg, "testcard went down, is currently 0.5, NEW LOWEST!!!\n(lowest seen: 1)\nver\n[mang] bleh from nope")

    
    @patch("src.MarketWatcher.MarketWatcher.reload_db")
    @patch("src.MarketWatcher.sleep")
    @patch("src.MarketWatcher.CardDatabase.save_data")
    @patch("src.MarketWatcher.MarketWatcher.send_alert")
    @patch("src.MarketWatcher.MarketWatcher.get_price_change_message")
    @patch("src.MarketWatcher.MarketWatcher.get_card_values")
    def test_single_run_main(self, mock_card_value, mock_get_message, *args):
        market_watcher = MarketWatcher()
        market_watcher.logger.info = MagicMock()
        fields = {
            "links": ["http://example.com", "http://example2.com"],
            "note": "Test note",
            "alert": ["pc", "discord"],
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "seller": "1"
        }
        card = Card("testcard", fields)
        card.data = {
            "2021-01-01": {"min": 1, "avg": 2},
            "2021-01-02": {"min": 2, "avg": 3},
            "2021-01-03": {"min": 3, "avg": 4},
        }
        market_watcher.card_db.cards = [card]

        mock_card_value.return_value = None
        market_watcher.single_run_main(None)
        self.assertEqual(mock_get_message.call_count, 0)

        mock_card_value.return_value = {"min": 0.5, "avg": 0.75, "url": "www.test.com"}
        mock_get_message.return_value = (False, None, "something else")
        market_watcher.single_run_main(None)
        self.assertEqual(mock_get_message.call_count, 1)
        self.assertEqual(market_watcher.send_alert.call_count, 0)

        mock_get_message.return_value = (True, "something", "something else")
        market_watcher.single_run_main(None)
        self.assertEqual(mock_get_message.call_count, 2)
        self.assertEqual(market_watcher.send_alert.call_count, 1)
        self.assertEqual(market_watcher.card_db.save_data.call_count, 1)
        self.assertEqual(len(card.data.keys()), 4)
        self.assertEqual(card.last_data["min"], 0.5)
        self.assertEqual(card.last_data["avg"], 0.75)
        self.assertEqual(card.min_data, 0.5)
