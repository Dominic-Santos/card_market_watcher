from .Discord import Discord
from .Config import Config
from .Helpers import (
    pc_alert,
    create_logger,
    get_wait_time,
    get_sleep_time,
    pretty_price,
    get_formatted_time,
    get_cards_location,
    get_data_location,
)
from .CardDatabase import CardDatabase
from .XPath import XPath
from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

class MarketWatcher():
    def __init__(self):
        self.logger = create_logger("MarketWatcher", "logs/market_watcher.log")
        self.config = Config()
        self.discord = Discord(self.config.discord_token)
        self.running = False
        self._wait_time = get_wait_time()
        self.card_db = CardDatabase(get_cards_location(), get_data_location())
        self.reload_db()

    def reload_db(self):
        self.card_db.load_all()
        self.card_db.save_all()

    def send_alert(self, title: str = "title", message: str = "message", alert: list = [], channels: list = ["default"], link: str = ""):
        if "discord" in alert:
            for channel in channels:
                msg = message if link == "" else f"{message}\n{link}"
                ok = self.discord.send_message(msg, self.config.discord_channel_by_name(channel))
                if not ok:
                    self.logger.error("Failed to send discord message")
        if "pc" in alert:
            pc_alert(title, message, link)
    
    @staticmethod
    def get_card_market_values(driver, cm_url):
        retry_limit = 1
        for i in range(retry_limit + 1):
            driver.get(cm_url)
            sleep(0.5)
            try:
                any_version = "/Cards/" in cm_url
                product = "Magic" if "/Magic/" in cm_url else "Other"
                if any_version:
                    padding = False
                else:
                    check = driver.find_element(By.XPATH, XPath.padding_check[0]).get_attribute(XPath.padding_check[1]).strip()
                    padding = check.lower() != "available items"

                xpath = XPath(product, any_version=any_version, padding=padding)

                trend_price = driver.find_element(By.XPATH, xpath.trend_price[0]).get_attribute(xpath.trend_price[1]).strip()
                from_price = driver.find_element(By.XPATH, xpath.lowest_price[0]).get_attribute(xpath.lowest_price[1]).strip()
                seller_location = driver.find_element(By.XPATH, xpath.seller_location[0]).get_attribute(xpath.seller_location[1]).split(": ")[1].strip()
                version = driver.find_element(By.XPATH, xpath.card_version[0]).get_attribute(xpath.card_version[1]).strip()
                card_condition = driver.find_element(By.XPATH, xpath.card_condition[0]).get_attribute(xpath.card_condition[1]).strip()
                card_language = driver.find_element(By.XPATH, xpath.card_language[0]).get_attribute(xpath.card_language[1]).strip()
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print("get price exception", e)
                print(traceback.format_exc())
                if i < retry_limit:
                    sleep(get_sleep_time())
                    continue
                trend_price = ""
                from_price = ""
                seller_location = ""
                version = ""
                card_condition = ""
                card_language = ""
            break

        min_price = 0
        avg_price = 0

        if trend_price not in ["", "N/A"]:
            avg_price = float(trend_price.split(" ")[0].replace(".", "").replace(",", "."))

        if from_price not in ["", "N/A"]:
            min_price = float(from_price.split(" ")[0].replace(".", "").replace(",", "."))

        return {
            "min": min_price,
            "avg": avg_price,
            "seller_location": seller_location,
            "version": version,
            "condition": card_condition,
            "language": card_language,
            "url": cm_url
        }

    @staticmethod
    def create_cardmarket_link(product: str, card: str, language: str, condition: str, seller_location: str):
        if "/" in card:
            # single version of the card
            url = f"https://www.cardmarket.com/en/{product}/Products/Singles/{card}?sellerCountry={seller_location}"
        else:
            # any version of the card
            url = f"https://www.cardmarket.com/en/{product}/Cards/{card}?sellerCountry={seller_location}"
        
        if language != "any":
            url += f"&language={language}"
        
        if condition != "any":
            url += f"&minCondition={condition}"
        
        return url
    
    def get_card_values(self, driver, card) -> dict:
        new_prices = None
        for i, card_link in enumerate(card.links):
            cm_url = self.create_cardmarket_link(card.product, card_link, card.language, card.condition, card.seller_location)

            prices = self.get_card_market_values(driver, cm_url)
            if prices is None:
                self.running = False
                return
            if prices["min"] == 0:
                raise Exception("no price found")

            if new_prices is None:
                new_prices = prices
            elif prices["min"] <= new_prices["min"]:
                new_prices = prices

            if i + 1 < len(card.links):
                sleep(get_sleep_time())
        return new_prices
    
    @staticmethod
    def get_price_change_message(card, new_prices: dict, max_length: int):
        last_prices = card.last_data
        min_price = card.min_data
        msg = None

        to_log = "{card}{padding} | Low {lowest} | Min {minimum}, Avg {average}".format(
            card=card.name,
            padding=" " * (max(max_length, len(card.name)) - len(card.name)),
            minimum=pretty_price(last_prices["min"]),
            average=pretty_price(last_prices["avg"]),
            lowest=pretty_price(min_price)
        )

        changes = last_prices["min"] != new_prices["min"] or last_prices["avg"] != new_prices["avg"]

        if changes:

            if new_prices["min"] < last_prices["min"] or last_prices["min"] == 0:
                compare = "Down"
                msg = "%s went down, is currently %s" % (
                    card.name,
                    new_prices["min"]
                )
                if new_prices["min"] <= min_price:
                    msg += ", lowest seen" if new_prices["min"] == min_price else ", NEW LOWEST!!!"

                msg += f"\n(lowest seen: {min_price})"
                msg += f"\n{new_prices['version']}\n[{new_prices['condition']}] {new_prices['language']} from {new_prices['seller_location']}"

            elif new_prices["min"] == last_prices["min"] and new_prices["avg"] < last_prices["avg"]:
                compare = "Down"
            else:
                compare = " Up "

            to_log = "{start} | {compare} | Min {new_mininum}, Avg {new_average}".format(
                start=to_log,
                compare=compare,
                new_mininum=pretty_price(new_prices["min"]),
                new_average=pretty_price(new_prices["avg"]),
            )
        return changes, msg, to_log

    def single_run_main(self, driver):
        longest_card = self.card_db.longest_card_name
        self.card_db.sort_cards()

        cards = self.card_db.card_names
        self.logger.info(f"{cards}, {len(cards)}")

        for card in self.card_db.cards:
            new_prices = self.get_card_values(driver, card)
            if new_prices is None:
                return
            
            changes, msg, to_log = self.get_price_change_message(card, new_prices, longest_card)
            if changes:
                if msg is not None:
                    self.send_alert(
                        "market watcher",
                        msg,
                        alert=card.alert,
                        link=new_prices["url"],
                        channels=card.channels
                    )

                card.data[get_formatted_time()] = {
                    "min": new_prices["min"],
                    "avg": new_prices["avg"],
                }
                self.card_db.save_data()

            self.logger.info(to_log)
            sleep(get_sleep_time())

        self.logger.info("Run Done")

    def single_run(self):
        driver = webdriver.Chrome(options=CHROME_OPTIONS)
        driver.set_window_position(-2000,0)
        self.reload_db()
        try:
            self.single_run_main(driver)
        except KeyboardInterrupt:
            self.running = False
        else:
            driver.quit()
    
    def run(self):
        self.logger.info("Starting MarketWatcher")
        self.running = True
        while self.running:
            self.single_run()
            if self.running:
                try:
                    sleep(self._wait_time)
                except KeyboardInterrupt:
                    self.running = False
        
        self.logger.info("Stopping MarketWatcher")
