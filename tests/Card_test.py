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
            "any_version": True,
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
        self.assertTrue(card.any_version)
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
        self.assertEqual(card.condition, "2")
        self.assertEqual(card.language, "1")
        self.assertEqual(card.channels, ["default"])
        self.assertEqual(card.seller_location, "1,2,3,33,35,5,6,8,9,11,12,7,14,15,37,16,17,36,21,18,19,20,22,23,24,25,26,27,29,31,30,10,28,4")
        self.assertFalse(card.any_version)
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
            "any_version": True,
            "seller": "1"
        }
        card = Card("testname", fields)
        self.assertEqual(card.to_dict(), fields)

if __name__ == '__main__':
    unittest.main()