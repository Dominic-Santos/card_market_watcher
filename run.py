from src.CardDatabase import CardDatabase


def main():
    print("Hello, World!")
    database = CardDatabase()
    database.load_cards()
    database.save_cards()

if __name__ == "__main__":
    main()
