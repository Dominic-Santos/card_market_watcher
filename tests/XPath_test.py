import unittest

from src.XPath import XPath

class TestXPath(unittest.TestCase):
    def test_any_version(self):
        xpath = XPath("test", any_version=True)
        self.assertEqual(xpath.trend_price, ('//div[contains(@class, "infoContainer")]/dl/dd[4]/span', "innerHTML"))
        self.assertEqual(xpath.lowest_price, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[4]/div[1]/div/div/span', "innerHTML"))
        self.assertEqual(xpath.seller_location, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div[1]/div[1]/span/span/span[2]', "aria-label"))
        self.assertEqual(xpath.card_version, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/a[1]', "aria-label"))
        self.assertEqual(xpath.card_condition, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/a[2]', "data-bs-original-title"))
        self.assertEqual(xpath.card_language, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/span', "aria-label"))
        self.assertEqual(xpath.padding_check, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dt[4]', "innerHTML"))

    def test_single(self):
        xpath = XPath("test")
        self.assertEqual(xpath.trend_price, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dd[6]/span', "innerHTML"))
        self.assertEqual(xpath.lowest_price, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div[1]/div[1]/div[1]/span', "innerHTML"))
        self.assertEqual(xpath.seller_location, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[1]/span/span/span[2]', "aria-label"))
        self.assertEqual(xpath.card_version, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dd[2]/div/a', "innerHTML"))
        self.assertEqual(xpath.card_condition, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[2]/div/div[1]/a', "data-bs-original-title"))
        self.assertEqual(xpath.card_language, ('//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[2]/div/div[1]/span', "aria-label"))
        self.assertEqual(xpath.padding_check, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dt[4]', "innerHTML"))
    
    def test_single_padding(self):
        xpath = XPath("test", padding=True)
        self.assertEqual(xpath.trend_price, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dd[7]/span', "innerHTML"))
        self.assertEqual(xpath.card_version, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dd[3]/div/a', "innerHTML"))
    
    def test_magic_version(self):
        xpath = XPath("Magic")
        self.assertEqual(xpath.card_version, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dd[2]/div/a[2]', "innerHTML"))
    
    def test_static_property(self):
        self.assertEqual(XPath.padding_check, ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dt[4]', "innerHTML"))
        