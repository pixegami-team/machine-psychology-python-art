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

class Art:
    def __init__(self) -> None:
        self.start_color: tuple = (0, 0, 0)
        self.end_color: tuple = (0, 0, 0)
        self.art_nodes: List[ArtNode] = []
    
    def serialize(self) -> str:
        start_color_hex = rgb_to_hex(self.start_color)
        end_color_hex = rgb_to_hex(self.end_color)
        code = f"000:{start_color_hex}:{end_color_hex}:" + ":".join([node.serialize() for node in self.art_nodes])
        return code

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

    black = (0, 0, 0)
    default_color = (12, 16, 36)

    scale_factor = 2

    image_size_px = 256 * scale_factor
    padding_px = 32 * scale_factor
    iterations = 9
    max_thickness = 6 * scale_factor
    min_thickness = 2 * scale_factor
    thickness_delta = 1 * scale_factor
    shape_close_off = 4

    print(f"start color: {rgb_to_hex(start_color)}")
    print(f"end color: {rgb_to_hex(end_color)}")

    image = Image.new("RGB", (image_size_px, image_size_px), color=default_color)

    # Generate a bunch of random points.
    min_p = padding_px
    max_p = image_size_px - padding_px
    art_nodes = []
    thickness = min_thickness
    thickness_mod = thickness_delta

    for i in range(iterations):
        x = random.randint(min_p, max_p)
        y = random.randint(min_p, max_p)

        # Get the thickness
        thickness = thickness + thickness_mod
        if thickness == max_thickness:
            thickness_mod = -thickness_delta
        if thickness == min_thickness:
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
    art.art_nodes = art_nodes
    art.start_color = start_color
    art.end_color = end_color
    print(f"Serialized art: {art.serialize()}")

    # Draw the artwork.
    n_points = len(art_nodes)
    for i in range(n_points):

        node = art_nodes[i]
        if i == n_points - 1:
            next_node = art_nodes[0]
        else:
            next_node = art_nodes[i + 1]

        # Get the right color.
        color_factor = abs(((i * 2) / n_points) - 1)
        line_color = interpolate(art.end_color, art.start_color, color_factor)

        overlay = Image.new("RGB", (image_size_px, image_size_px), color=black)
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

