import unittest
from src.Card import Card

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        fields = {
            "link": "http://example.com",
            "note": "Test note",
            "alert": 1,
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "any_version": True
        }
        card = Card("testcard", fields)
        self.assertEqual(card.links[0], "http://example.com")
        self.assertEqual(card.note, "Test note")
        self.assertEqual(card.alert, 1)
        self.assertEqual(card.product, "Pokemon")
        self.assertEqual(card.condition, "1")
        self.assertEqual(card.language, "2")
        self.assertEqual(card.channels, ["email", "sms"])
        self.assertTrue(card.any_version)
        self.assertEqual(card.name, "testcard")

    def test_card_default_values(self):
        fields = {
            "link": "http://example.com"
        }
        card = Card("testcard", fields)
        self.assertEqual(card.links[0], "http://example.com")
        self.assertEqual(card.note, "")
        self.assertEqual(card.alert, 0)
        self.assertEqual(card.product, "Digimon")
        self.assertEqual(card.condition, "2")
        self.assertEqual(card.language, "1")
        self.assertEqual(card.channels, ["default"])
        self.assertFalse(card.any_version)
        self.assertEqual(card.name, "testcard")
    
    def test_card_to_dict(self):
        fields = {
            "links": ["http://example.com"],
            "note": "Test note",
            "alert": 1,
            "product": "Pokemon",
            "condition": "1",
            "language": "2",
            "channels": ["email", "sms"],
            "any_version": True
        }
        card = Card("testname", fields)
        self.assertEqual(card.to_dict(), fields)

if __name__ == '__main__':
    unittest.main()