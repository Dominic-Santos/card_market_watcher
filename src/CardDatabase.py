from src.Helpers import load_json, save_json
from src.Card import Card

class CardDatabase():
    def __init__(self, cards_file: str, data_file: str):
        self.files = {
            "cards": cards_file,
            "data": data_file,
        }
        self.cards = []
        self.load_cards()
        self.load_data()
    
    def load_cards(self):
        raw_cards = load_json(self.files["cards"])
        self.cards = self.cards_from_json(raw_cards)
    
    def save_cards(self):
        raw_cards = self.cards_to_json(self.cards)
        save_json(self.files["cards"], raw_cards)
    
    def cards_to_json(self, cards: list[Card]):
        return {card.name: card.to_dict() for card in cards}

    def cards_from_json(self, card_json: dict):
        return [Card(name, fields) for name, fields in card_json.items()]

    def load_data(self):
        raw_data = load_json(self.files["data"])
        for card in self.cards:
            card.data = raw_data.get(card.name, [])
    
    def save_data(self):
        raw_data = {card.name: card.data for card in self.cards}
        save_json(self.files["data"], raw_data)
