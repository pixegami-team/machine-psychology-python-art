import colorsys
import json
from typing import List, Tuple
from color import Color


class ColorNameMapper:
    def __init__(self, hex_color_map: str) -> None:
        self.color_names: List[Color] = []

        with open(hex_color_map, "r") as f:
            color_names_raw = json.load(f)
            self.color_names = [Color(c[0], c[1]) for c in color_names_raw]

    def get(self, rgb_color: Tuple[int]):

        hls_color = colorsys.rgb_to_hls(*rgb_color)
        best_distance = None
        best_color = None

        for color_name in self.color_names:

            color_dist_rgb = self.color_dist(rgb_color, color_name.rgb)
            color_dist_hls = self.color_dist(hls_color, color_name.hls)
            combined_delta = color_dist_rgb + color_dist_hls * 2

            if best_distance is None or combined_delta < best_distance:
                best_distance = combined_delta
                best_color = color_name

        print(f"Best match is: {best_color.name}")
        return best_color

    def color_dist(self, c1: Tuple[int], c2: Tuple[int]):
        delta = sum([pow(c1[i] - c2[i], 2) for i in range(3)])
        return delta
