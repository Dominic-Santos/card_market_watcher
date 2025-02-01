import unittest

from src.CardDatabase import CardDatabase
from unittest.mock import patch

TEST_CARDS_FILE = "tests/testdata/cards.json"
TEST_DATA_FILE = "tests/testdata/data.json"

class TestCardDatabase(unittest.TestCase):
    def test_card_database_initialization(self,):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        self.assertEqual(len(card_database.cards), 2)
        card = card_database.cards[0]
        self.assertEqual(card.links, ["http://example.com"])
        self.assertEqual(card.note, "Test note")
        self.assertEqual(card.alert, ["pc", "discord"])
        self.assertEqual(card.product, "Pokemon")
        self.assertEqual(card.condition, "1")
        self.assertEqual(card.language, "2")
        self.assertEqual(card.channels, ["default"])
        self.assertEqual(card.seller_location, "1")
        self.assertEqual(card.name, "testcard")
        self.assertEqual(card.data, {})

    def test_card_database_save_load(self):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        card_database.cards[0].data = {"2021-01-01": {"min": 1, "avg": 2}}
        card_database.save_all()
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        self.assertEqual(card_database.cards[0].data, {"2021-01-01": {"min": 1, "avg": 2}})
        card_database.cards[0].data = {}
        card_database.save_all()
    
    def test_card_names(self):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        self.assertEqual(card_database.card_names, ['testcard', 'testcard2'])
    
    def test_longest_card_name(self):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        self.assertEqual(card_database.longest_card_name, 9)
    
    def test_longest_card_name_no_cards(self):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        card_database.cards = []
        self.assertEqual(card_database.longest_card_name, 0)
    
    def test_sort_cards(self):
        card_database = CardDatabase(TEST_CARDS_FILE, TEST_DATA_FILE)
        card_database.cards[0].product = "Magic"
        card_database.sort_cards()
        self.assertEqual(card_database.cards[0].product, "Magic")
