ALERTS = {
    0: [],
    1: ["pc", "discord"],
    2: ["discord"],
}

class Card():
    def __init__(self, cardname: str, fields: dict):
        self.name = cardname
        link = fields.get("link", None)
        self.links = fields.get("links", [])
        if link is not None:
            self.links.append(link)
        if len(self.links) == 0:
            raise ValueError("Card must have at least one link")

        self.note = fields.get("note", "")
        self._alert = fields.get("alert", 0)
        self.product = fields.get("product", "Digimon")
        self.condition = fields.get("condition", "2")
        self.language = fields.get("language", "1")
        self.channels = fields.get("channels", ["default"])
        self.seller_location = fields.get("seller", "1,2,3,33,35,5,6,8,9,11,12,7,14,15,37,16,17,36,21,18,19,20,22,23,24,25,26,27,29,31,30,10,28,4")
        self.any_version = fields.get("any_version", False)
        self.data = {}

    def to_dict(self):
        return {
            "links": self.links,
            "note": self.note,
            "alert": self.alert,
            "product": self.product,
            "condition": self.condition,
            "language": self.language,
            "channels": self.channels,
            "seller": self.seller_location,
            "any_version": self.any_version
        }

    @property
    def order(self):
        return {"magic": 0, "digimon": 1}.get(self.product.lower(), 9)
    
    @property
    def last_data(self):
        if len(self.data.keys()) == 0:
            return {"min": 0, "avg": 0}
        return self.data[sorted(self.data.keys())[-1]]

    @property
    def min_data(self):
        if len(self.data) == 0:
            return 0
        return min([entry["min"] for entry in self.data.values()])

    @property
    def alert(self):
        if type(self._alert) == list:
            return self._alert
        return ALERTS.get(self._alert, [])
