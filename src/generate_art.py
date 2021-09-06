from typing import List, Tuple
from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


class ArtNode:
    def __init__(self, x: int, y: int, thickness: int) -> None:
        self.x = x
        self.y = y
        self.line_thickness: int = thickness

    def xy(self):
        return (self.x, self.y)

    def serialize(self):
        return f"{self.x}.{self.y}.{self.line_thickness}"

    @staticmethod
    def deserialize(code: str) -> "ArtNode":
        code_arr = code.split(".")
        x = int(code_arr[0])
        y = int(code_arr[1])
        line_thickness = int(code_arr[2])
        return ArtNode(x, y, line_thickness)


class Art:
    def __init__(self) -> None:
        self.start_color: tuple = (0, 0, 0)
        self.end_color: tuple = (0, 0, 0)
        self.nodes: List[ArtNode] = []
        self.size: int = 0

    def serialize(self) -> str:
        start_color_hex = rgb_to_hex(self.start_color).strip("#")
        end_color_hex = rgb_to_hex(self.end_color).strip("#")
        code = f"A:{self.size}:{start_color_hex}:{end_color_hex}:" + ":".join(
            [node.serialize() for node in self.nodes]
        )
        return code

    @staticmethod
    def deserialize(code: str) -> "Art":
        art = Art()
        code_arr = code.split(":")
        art.size = int(code_arr[1])
        art.start_color = _hex_to_rgb(code_arr[2])
        art.end_color = _hex_to_rgb(code_arr[3])

        node_str_arr = code_arr[4:]
        for node_str in node_str_arr:
            art.nodes.append(ArtNode.deserialize(node_str))

        return art


def interpolate(c1: Tuple[int], c2: Tuple[int], f: float):
    rf = 1 - f
    return tuple([int((f * c1[i] + rf * c2[i])) for i in range(3)])


def generate_starting_color():
    h = random.random()
    s = 0.8 + 0.2 * random.random()
    v = 0.8 + 0.2 * random.random()
    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple(map(lambda x: int(x * 255), float_rgb))


def rgb_to_hex(color: Tuple[int]):
    return "#{:02x}{:02x}{:02x}".format(*color)


def _hex_to_rgb(hexcode: str):
    hexcode = hexcode.strip("#")
    return (int(hexcode[0:2], 16), int(hexcode[2:4], 16), int(hexcode[4:6], 16))


def generate_end_color(start_color):
    # Convert color into HSV.
    h, s, v = colorsys.rgb_to_hsv(*map(lambda x: x / 255, start_color))

    h += random.choice([0.2, 0.4])

    v = min(1, v + random.random() * 0.5)
    s = min(1, s + random.random() * 0.5)
    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple(map(lambda x: int(x * 255), float_rgb))


def generate_bg_color(start_color):
    # Convert color into HSV.
    h, s, v = colorsys.rgb_to_hsv(*map(lambda x: x / 255, start_color))

    h += 0.2 * random.random()

    # Make it dark.
    v = 0.15

    # De-saturate.
    s = 0.3

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple(map(lambda x: int(x * 255), float_rgb))


def generate_art(output_path: str):
    start_color = generate_starting_color()
    end_color = generate_end_color(start_color)
    generate_art_by_color(start_color, end_color, output_path)


def generate_art_by_color(start_color, end_color, output_path: str):
    print("Generating art!")

    print(f"start color: {rgb_to_hex(start_color)}")
    print(f"end color: {rgb_to_hex(end_color)}")

    code = generate_art_code(start_color, end_color)
    image = generate_art_from_code(code, output_path=output_path)
    return image


def generate_art_code(start_color, end_color):

    # Settings
    terminal_size_px = 512
    scale_factor = terminal_size_px // 128
    image_size_px = terminal_size_px * 2
    padding_px = 32 * scale_factor
    iterations = random.choice([7, 8, 9])
    max_thickness = 10 * scale_factor
    min_thickness = 2 * scale_factor
    thickness_delta = 1 * scale_factor
    shape_close_off = 4

    # Generate a bunch of random points.
    min_p = padding_px
    max_p = image_size_px - padding_px
    art_nodes = []
    thickness = random.randint(
        min_thickness + thickness_delta, max_thickness - thickness_delta
    )
    thickness_mod = random.choice([thickness_delta, -thickness_delta])

    for i in range(iterations):
        x = random.randint(min_p, max_p)
        y = random.randint(min_p, max_p)

        # Get the thickness
        thickness = thickness + thickness_mod
        thickness = max(thickness, min_thickness)
        thickness = min(thickness, max_thickness)

        if thickness >= max_thickness:
            thickness_mod = -thickness_delta
        if thickness <= min_thickness:
            thickness_mod = thickness_delta

        # Create the node.
        node = ArtNode(x=x, y=y, thickness=thickness)
        art_nodes.append(node)

        # Everytime we close off a shape, we add the starting point.
        if i % shape_close_off == 0 and i != 0:
            art_nodes.append(art_nodes[-shape_close_off])

    # Add the first point back to the end, so it closes the shape.
    art_nodes.append(art_nodes[0])

    # Center the shape.
    min_x = min([n.x for n in art_nodes])
    min_y = min([n.y for n in art_nodes])
    max_x = max([n.x for n in art_nodes])
    max_y = max([n.y for n in art_nodes])
    x_offset = ((image_size_px - max_x) - min_x) // 2
    y_offset = ((image_size_px - max_y) - min_y) // 2

    for node in art_nodes:
        node.x += x_offset
        node.y += y_offset

    # Serialize the artwork.
    art = Art()
    art.size = terminal_size_px
    art.nodes = art_nodes
    art.start_color = start_color
    art.end_color = end_color
    print(f"Serialized art: {art.serialize()}")
    return art.serialize()


def generate_art_from_code(code: str, output_path: str):

    art = Art.deserialize(code)

    image_size_px = art.size * 2
    BG_COLOR = (12, 16, 36)
    BLACK = (0, 0, 0)

    image = Image.new("RGB", (image_size_px, image_size_px), color=BG_COLOR)
    # Draw the artwork.
    n_points = len(art.nodes)
    for i in range(n_points):

        node = art.nodes[i]
        if i == n_points - 1:
            next_node = art.nodes[0]
        else:
            next_node = art.nodes[i + 1]

        # Get the right color.
        color_factor = abs(((i * 2) / n_points) - 1)
        line_color = interpolate(art.end_color, art.start_color, color_factor)

        overlay = Image.new("RGB", (image_size_px, image_size_px), color=BLACK)
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.line(
            [node.xy(), next_node.xy()],
            fill=line_color,
            width=node.line_thickness,
        )
        image = ImageChops.add(image, overlay)

    # draw.line(points, fill=line_color, width=4, joint="curve")
    image = image.resize(
        (image_size_px // 2, image_size_px // 2), resample=Image.ANTIALIAS
    )
    image.save(output_path)

    return image
