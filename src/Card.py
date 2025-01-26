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
            "any_version": self.any_version
        }
