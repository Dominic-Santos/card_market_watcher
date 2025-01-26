from time import sleep
from src.MarketWatcher import MarketWatcher


def main():
    print("Hello, World!")
    watcher = MarketWatcher()
    watcher.send_alert(title="Hello", message="World", alert=["discord", "pc"], link="http://example.com")
    sleep(5)

if __name__ == "__main__":
    main()
