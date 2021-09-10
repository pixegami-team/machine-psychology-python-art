from typing import Tuple
import colorsys


class Color:
    def __init__(self, hex: str, name: str) -> None:
        self.hex = hex
        self.name = name
        self.rgb = Color.hex_to_rgb(hex)
        self.hls = colorsys.rgb_to_hls(*self.rgb)

    @staticmethod
    def hex_to_rgb(hexcode: str):
        hexcode = hexcode.strip("#")
        return (int(hexcode[0:2], 16), int(hexcode[2:4], 16), int(hexcode[4:6], 16))

    @staticmethod
    def rgb_to_hex(color: Tuple[int]):
        return "#{:02x}{:02x}{:02x}".format(*color)

    @staticmethod
    def hsv_float_to_rgb_int(hsv: Tuple[int]):
        float_rgb = colorsys.hsv_to_rgb(*hsv)
        return tuple(map(lambda x: int(x * 255), float_rgb))

    @staticmethod
    def interpolate(c1: Tuple[int], c2: Tuple[int], f: float):
        rf = 1 - f
        return tuple([int((f * c1[i] + rf * c2[i])) for i in range(3)])
