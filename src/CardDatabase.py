from src.Helpers import load_json, save_json
from src.Card import Card

class CardDatabase():
    def __init__(self, cards_file: str, data_file: str):
        self.files = {
            "cards": cards_file,
            "data": data_file,
        }
        self.cards = []
        self.load_all()

    def load_all(self):
        self.load_cards()
        self.load_data()

    def save_all(self):
        self.save_cards()
        self.save_data()
    
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
            card.data = raw_data.get(card.name, {}).get("data", {})
    
    def save_data(self):
        raw_data = {card.name: {"data": card.data} for card in self.cards}
        save_json(self.files["data"], raw_data)
    
    @property
    def longest_card_name(self):
        if len(self.cards) == 0:
            return 0
        return max(len(card.name) for card in self.cards)
    
    def sort_cards(self):
        self.cards.sort(key=lambda card: card.order)
    
    @property
    def card_names(self):
        return [card.name for card in self.cards]

