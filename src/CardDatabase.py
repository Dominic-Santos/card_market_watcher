from src.Helpers import load_json, save_json
from src.Card import Card

DATABASE_FILE = "data/cards.json"

class CardDatabase():
    def __init__(self):
        self.cards = []
        self.load_cards()
    
    def load_cards(self):
        raw_cards = load_json(DATABASE_FILE)
        self.cards = [Card(name, fields) for name, fields in raw_cards.items()]
    
    def save_cards(self):
        raw_cards = {card.name: card.to_dict() for card in self.cards}
        save_json(DATABASE_FILE, raw_cards)