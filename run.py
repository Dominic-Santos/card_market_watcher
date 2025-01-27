from time import sleep
from src.MarketWatcher import MarketWatcher


def main():
    watcher = MarketWatcher()
    watcher.run()    

if __name__ == "__main__":
    main()
