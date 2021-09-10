"""A single Node in the graph of the art."""


class ArtNode:
    def __init__(self, x: int, y: int, thickness: int) -> None:
        self.x = x
        self.y = y
        self.thickness: int = thickness

    def xy(self, factor: int = 1):
        """
        Gets the xy position of this node, but also allow for
        scaling it (for upscaling or downscaling resolution.
        """
        return (self.x * factor, self.y * factor)

    def serialize(self):
        return f"{self.x}.{self.y}.{self.thickness}"

    @staticmethod
    def deserialize(code: str) -> "ArtNode":
        code_arr = code.split(".")
        x = int(code_arr[0])
        y = int(code_arr[1])
        thickness = int(code_arr[2])
        return ArtNode(x, y, thickness)

    def clone(self) -> "ArtNode":
        return ArtNode(self.x, self.y, self.thickness)
