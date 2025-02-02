import os
import win32con
import unittest
from unittest.mock import patch, mock_open
from src.Helpers import (
    load_json,
    check_dir,
    get_sleep_time,
    get_wait_time,
    pretty_price,
    create_logger,
    get_formatted_time,
    get_cards_location,
    get_data_location,
)

class TestHelpers(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"testcard": {"data": {}}, "testcard2": {"data": {}}}')
    def test_load_json(self, mock_file):
        json = load_json('tests/test_data.json')
        self.assertEqual(json, {
            "testcard": {
                "data": {}
            },
            "testcard2": {
                "data": {}
            }
        })

    @patch('builtins.open', new_callable=mock_open, read_data='{"invalid_json": ')
    def test_load_json_empty(self, mock_file):
        json = load_json('tests/test_data.json')
        self.assertEqual(json, {})

    def test_check_dir(self):
        tmp_dir = "tests/tmp"
        self.assertFalse(os.path.exists(tmp_dir))
        check_dir(tmp_dir)
        self.assertTrue(os.path.exists(tmp_dir))
        os.rmdir(tmp_dir)
    
    @patch('src.Helpers.random.randint', return_value=5)
    def test_get_sleep_time(self, mock_randint):
        self.assertEqual(get_sleep_time(), 65)
    
    def test_get_wait_time(self):
        self.assertEqual(get_wait_time(), 900)

    def test_pretty_price(self):
        self.assertEqual(pretty_price(1.2345), "01.23")
        self.assertEqual(pretty_price(1.2), "01.20")
        self.assertEqual(pretty_price(1), "01.00")
        self.assertEqual(pretty_price(1.23456789), "01.23")
    
    def test_create_logger(self):
        logger = create_logger("test_logger", "tests/test.log")
        self.assertEqual(logger.name, "test_logger")
        self.assertTrue(logger.handlers[0].baseFilename, "tests/test.log")
        self.assertEqual(logger.level, 10)
    
    @patch('src.Helpers.datetime')
    def test_get_formatted_time(self, mock_datetime):
        mock_datetime.now.return_value = "2021-02-01 00:00:00.000000"
        self.assertEqual(get_formatted_time(), "2021-02-01 00:00")

    def test_get_cards_location(self):
        self.assertEqual("data/cards.json", "data/cards.json")
    
    def test_get_data_location(self):
        self.assertEqual("data/data.json", "data/data.json")
