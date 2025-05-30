import unittest
from src.Card import Card

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        fields = {
            "link": "http://example.com",
            "note": "Test note",
            "alert": ["pc", "discord"],
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "seller": "1"
        }
        card = Card("testcard", fields)
        self.assertEqual(card.links, ["http://example.com"])
        self.assertEqual(card.note, "Test note")
        self.assertEqual(card.alert, ["pc", "discord"])
        self.assertEqual(card.product, "Pokemon")
        self.assertEqual(card.condition, "1")
        self.assertEqual(card.language, "2")
        self.assertEqual(card.channels, ["email", "sms"])
        self.assertEqual(card.seller_location, "1")
        self.assertEqual(card.name, "testcard")

    def test_card_default_values(self):
        fields = {
            "link": "http://example.com"
        }
        card = Card("testcard", fields)
        self.assertEqual(card.links, ["http://example.com"])
        self.assertEqual(card.note, "")
        self.assertEqual(card.alert, [])
        self.assertEqual(card.product, "Digimon")
        self.assertEqual(card.condition, "any")
        self.assertEqual(card.language, "any")
        self.assertEqual(card.channels, ["default"])
        self.assertEqual(card.seller_location, "1,2,3,33,35,5,6,8,9,11,12,7,14,15,37,16,17,36,21,18,19,20,22,23,24,25,26,27,29,31,30,10,28,4")
        self.assertEqual(card.name, "testcard")
    
    def test_card_to_dict(self):
        fields = {
            "links": ["http://example.com"],
            "note": "Test note",
            "alert": ["pc", "discord"],
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "seller": "1"
        }
        card = Card("testname", fields)
        self.assertEqual(card.to_dict(), fields)

    def test_missing_link_raises_error(self):
        fields = {}
        with self.assertRaises(ValueError):
            Card("testname", fields)
 
    def test_order(self):
        fields = {
            "link": "http://example.com",
            "product": "Magic"
        }
        card = Card("testname", fields)
        self.assertEqual(card.order, 0)

        fields = {
            "link": "http://example.com",
            "product": "Digimon"
        }
        card = Card("testname", fields)
        self.assertEqual(card.order, 1)

        fields = {
            "link": "http://example.com",
            "product": "Yugioh"
        }
        card = Card("testname", fields)
        self.assertEqual(card.order, 9)
    
    def test_last_data(self):
        fields = {
            "link": "http://example.com",
        }
        card = Card("testname", fields)
        self.assertEqual(card.last_data, {"min": 0, "avg": 0})

        card.data = {
            "2021-01-01": {"min": 1, "avg": 2},
            "2021-01-02": {"min": 2, "avg": 3},
            "2021-01-03": {"min": 3, "avg": 4},
        }
        self.assertEqual(card.last_data, {"min": 3, "avg": 4})
    
    def test_min_data(self):
        fields = {
            "link": "http://example.com",
        }
        card = Card("testname", fields)
        self.assertEqual(card.min_data, 0)

        card.data = {
            "2021-01-01": {"min": 1, "avg": 2},
            "2021-01-02": {"min": 2, "avg": 3},
            "2021-01-03": {"min": 3, "avg": 4},
        }
        self.assertEqual(card.min_data, 1)
    