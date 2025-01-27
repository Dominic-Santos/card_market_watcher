from .Discord import Discord
from .Config import Config
from .Helpers import pc_alert, create_logger, get_wait_time, get_sleep_time, pretty_price, get_formatted_time
from .CardDatabase import CardDatabase
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
        self.card_db = CardDatabase("data/cards.json", "data/data.json")
        self.reload_db()

    def reload_db(self):
        self.card_db.load_all()
        self.card_db.save_all()

    def send_alert(self, title: str = "title", message: str = "message", alert: list = [], channels: list = ["default"], link: str = ""):
        if "discord" in alert:
            for channel in channels:
                ok = self.discord.send_message(message, self.config.discord_channel_by_name(channel))
                if not ok:
                    self.logger.error("Failed to send discord message")
        if "pc" in alert:
            pc_alert(title, message, link)
    
    def get_card_market_values(self, driver, cm_url):
        retry_limit = 1
        for i in range(retry_limit + 1):
            try:
                driver.get(cm_url)
                sleep(0.5)
                
                xpath_prefix = '//*[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/'
                check = driver.find_element(By.XPATH, xpath_prefix + 'dt[4]').get_attribute("innerHTML").strip()
                if check.lower() == "available items":
                    trend_price = driver.find_element(By.XPATH, xpath_prefix + 'dd[6]/span').get_attribute("innerHTML").strip()
                    from_price = driver.find_element(By.XPATH, xpath_prefix + 'dd[5]').get_attribute("innerHTML").strip()
                else:
                    trend_price = driver.find_element(By.XPATH, xpath_prefix + 'dd[7]/span').get_attribute("innerHTML").strip()
                    from_price = driver.find_element(By.XPATH, xpath_prefix + 'dd[6]').get_attribute("innerHTML").strip()

            except Exception as e:
                print("get price exception", e)
                if i < retry_limit:
                    sleep(get_sleep_time())
                    continue
                trend_price = ""
                from_price = ""
            break

        min_price = 0
        avg_price = 0

        if trend_price not in ["", "N/A"]:
            avg_price = float(trend_price.split(" ")[0].replace(".", "").replace(",", "."))

        if from_price not in ["", "N/A"]:
            min_price = float(from_price.split(" ")[0].replace(".", "").replace(",", "."))

        return {"min": min_price, "avg": avg_price}

    def single_run_main(self, driver):
        longest_card = self.card_db.longest_card_name
        self.card_db.sort_cards()

        cards = self.card_db.card_names
        self.logger.info(f"{cards}, {len(cards)}")

        for card in self.card_db.cards:
            padding = " " * (longest_card - len(card.name))
            cm_url = f"https://www.cardmarket.com/en/{card.product}/Products/Singles/{card.links[0]}?language={card.language}&minCondition={card.condition}&sellerCountry={card.seller_location}"
            try:
                new_prices = self.get_card_market_values(driver, cm_url)
                if new_prices["min"] == 0:
                    raise Exception("no price found")
            except KeyboardInterrupt:
                self.running = False
                return
            except Exception as e:
                self.logger.info(f"{card.name}{padding} | Failed {str(e)}")
                # msg = "-- Script Error - {} - {} -- {} --".format(card, str(e), traceback.format_exc())
                sleep(get_sleep_time() * 3)
                continue
            
            last_prices = card.last_data
            min_price = card.min_data

            to_log = "{card}{padding} | Low {lowest} | Min {minimum}, Avg {average}".format(
                card=card.name,
                padding=" " * (longest_card - len(card.name)),
                minimum=pretty_price(last_prices["min"]),
                average=pretty_price(last_prices["avg"]),
                lowest=pretty_price(min_price)
            )

            if last_prices["min"] != new_prices["min"] or last_prices["avg"] != new_prices["avg"]:

                if new_prices["min"] < last_prices["min"] or last_prices["min"] == 0:
                    compare = "Down"
                    msg = "%s went down, is currently %s" % (
                        card.name,
                        new_prices["min"]
                    )
                    if new_prices["min"] <= min_price:
                        msg += ", lowest seen" if new_prices["min"] == min_price else ", NEW LOWEST!!!"

                    msg += f"\n(lowest seen: {min_price})"
                    self.send_alert(
                        "market watcher",
                        msg,
                        alert=card.alert,
                        link=cm_url,
                        channels=card.channels
                    )

                elif new_prices["min"] == last_prices["min"] and new_prices["avg"] < last_prices["avg"]:
                    compare = "Down"
                else:
                    compare = " Up "
                print("HERERRER", card.data)
                card.data[get_formatted_time()] = new_prices
                to_log = "{start} | {compare} | Min {new_mininum}, Avg {new_average}".format(
                    start=to_log,
                    compare=compare,
                    new_mininum=pretty_price(new_prices["min"]),
                    new_average=pretty_price(new_prices["avg"]),
                )
                self.card_db.save_data()

            self.logger.info(to_log)
        
            sleep(get_sleep_time())

            self.logger.info("Run Done")

    def single_run(self):
        driver = webdriver.Chrome(options=CHROME_OPTIONS)
        try:
            self.reload_db()
            self.single_run_main(driver)
        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.logger.info(f"general error {e}")
            print(traceback.format_exc())
            msg = "-- Script General Error -  {} --".format(str(e))
            self.send_alert(message=msg, alert=["discord"], channels=["default"])
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            print(e)
    
    def run(self):
        self.logger.info("Starting MarketWatcher")
        self.running = True
        while self.running:
            self.single_run()
            if self.running is False:
                break
            sleep(self._wait_time)
        
        self.logger.info("Stopping MarketWatcher")
