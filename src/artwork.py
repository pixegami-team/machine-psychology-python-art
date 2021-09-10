from art_node import ArtNode
from typing import List
from color import Color


class Artwork:
    def __init__(self) -> None:
        self.start_color: tuple = (0, 0, 0)
        self.end_color: tuple = (0, 0, 0)
        self.nodes: List[ArtNode] = []
        self.size: int = 0

    def serialize(self) -> str:
        """
        Serialize artwork into a string.
        """
        start_color_hex = Color.rgb_to_hex(self.start_color).strip("#")
        end_color_hex = Color.rgb_to_hex(self.end_color).strip("#")
        code = f"A:{self.size}:{start_color_hex}:{end_color_hex}:" + ":".join(
            [node.serialize() for node in self.nodes]
        )
        return code

    @staticmethod
    def deserialize(code: str) -> "Artwork":
        """
        Convert a code string back into an artwork.
        """

        art = Artwork()

        code_arr = code.split(":")
        art.size = int(code_arr[1])
        art.start_color = Color.hex_to_rgb(code_arr[2])
        art.end_color = Color.hex_to_rgb(code_arr[3])

        node_str_arr = code_arr[4:]
        for node_str in node_str_arr:
            art.nodes.append(ArtNode.deserialize(node_str))

        return art
