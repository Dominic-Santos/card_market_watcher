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
        self.alert = fields.get("alert", 0)
        self.product = fields.get("product", "Digimon")
        self.condition = fields.get("condition", "2")
        self.language = fields.get("language", "1")
        self.channels = fields.get("channels", ["default"])
        self.seller_location = fields.get("seller", "1,2,3,33,35,5,6,8,9,11,12,7,14,15,37,16,17,36,21,18,19,20,22,23,24,25,26,27,29,31,30,10,28,4")
        self.any_version = fields.get("any_version", False)
        self.data = []

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
