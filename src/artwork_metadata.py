class ArtworkMetadata:
    def __init__(self) -> None:
        self.item_id: str = ""
        self.title: str = ""
        self.start_color_name: str = ""
        self.end_color_name: str = ""
        self.code: str = ""

    def serialize(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "start_color_name": self.start_color_name,
            "end_color_name": self.end_color_name,
            "code": self.code,
        }
