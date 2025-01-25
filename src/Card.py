class Card():
    def __init__(self, cardname: str, fields: dict):
        self.name = cardname
        self.link = fields["link"]
        self.note = fields.get("note", "")
        self.alert = fields.get("alert", 0)
        self.product = fields.get("product", "Digimon")
        self.condition = fields.get("condition", "2")
        self.language = fields.get("language", "1")
        self.channels = fields.get("channels", [])
        self.any_version = fields.get("any_version", False)

    def to_dict(self):
        return {
            "link": self.link,
            "note": self.note,
            "alert": self.alert,
            "product": self.product,
            "condition": self.condition,
            "language": self.language,
            "channels": self.channels,
            "any_version": self.any_version
        }
