from typing import Tuple
from PIL import Image, ImageDraw, ImageChops
import random
import colorsys
from color import Color
from art_node import ArtNode
from artwork import Artwork


def generate_starting_color():

    # Choose starting HSV values.
    h = random.random()
    s = random.choice([0.3, 0.5, 1, 1])  # Favor saturated colors.
    v = random.choice([0.2, 0.8])  # Either dark or bright.

    return Color.hsv_float_to_rgb_int((h, s, v))


def generate_end_color(start_color):
    h, s, v = colorsys.rgb_to_hsv(*map(lambda x: x / 255, start_color))

    h += random.random() * 0.3  # Don't offset hue by too much.
    v = 1  # Set value to max.
    s = min(1, s + random.choice([0.2, 0.5, 1.0]))  # Saturation will only increase.

    return Color.hsv_float_to_rgb_int((h, s, v))


def generate_art(output_path: str):
    start_color = generate_starting_color()
    end_color = generate_end_color(start_color)
    generate_art_from_color(start_color, end_color, output_path)


def generate_art_from_color(start_color, end_color, output_path: str):
    print(f"Generating art with colors: {start_color}, {end_color} to {output_path}")
    code = generate_art_code(start_color, end_color)
    image = generate_art_from_code(code, output_path=output_path)
    return image


def generate_art_code(start_color: Tuple[int], end_color: Tuple[int]):
    """
    This is the algorithm to generate the artwork.
    We will aim to generate at terminal_size_px resolution, but will double
    it so we can anti-alias it back down.
    """

    # Image size.
    terminal_size_px = 512
    scale_factor = terminal_size_px // 128
    image_size_px = (
        terminal_size_px * 2
    )  # We will scale it up so we can anti-alias it later.

    # Padding from edge of image.
    padding_px = 32 * scale_factor

    # How many nodes to generate (not included inserted nodes)
    iterations = random.choice([7, 8, 9])

    # Line thickness and delta.
    max_thickness = 10 * scale_factor
    min_thickness = 3 * scale_factor
    thickness_delta = 1 * scale_factor

    shape_close_off = random.choice(
        [4, 7]
    )  # Every X nodes, insert another node to close off the shape.

    # Generate a bunch of random points.
    min_p = padding_px
    max_p = image_size_px - padding_px
    art_nodes = []
    thickness = min_thickness
    thickness_mod = random.choice([thickness_delta])

    for i in range(iterations):

        # Everytime we close off a shape, we add the starting point.
        if i % shape_close_off == 0 and i != 0:
            art_nodes.append(art_nodes[-shape_close_off].clone())

        # Put it in a random spot.
        x = random.randint(min_p, max_p)
        y = random.randint(min_p, max_p)

        # Create the node.
        node = ArtNode(x=x, y=y, thickness=thickness)
        art_nodes.append(node)

        # Change the thickness.
        thickness += thickness_mod
        thickness = max(thickness, min_thickness)
        thickness = min(thickness, max_thickness)

        # Cap the thickness.
        if thickness >= max_thickness:
            thickness_mod = -thickness_delta
        if thickness <= min_thickness:
            thickness_mod = thickness_delta

    # Add the first point back to the end, so it closes the shape.
    art_nodes.append(art_nodes[0].clone())

    # Center the shape.
    min_x = min([n.x for n in art_nodes])
    max_x = max([n.x for n in art_nodes])
    x_offset = ((image_size_px - max_x) - min_x) // 2

    min_y = min([n.y for n in art_nodes])
    max_y = max([n.y for n in art_nodes])
    y_offset = ((image_size_px - max_y) - min_y) // 2

    for node in art_nodes:
        node.x = (node.x + x_offset) // 2
        node.y = (node.y + y_offset) // 2

    # Serialize the artwork.
    art = Artwork()
    art.size = terminal_size_px
    art.nodes = art_nodes
    art.start_color = start_color
    art.end_color = end_color
    print(f"Serialized art: {art.serialize()}")
    return art.serialize()


def generate_art_from_code(code: str, output_path: str):

    # Deserialize the art from the code.
    art = Artwork.deserialize(code)

    # Generate the background.
    image_size_px = art.size * 2
    BG_COLOR = (12, 16, 36)
    BLACK = (0, 0, 0)
    image = Image.new("RGB", (image_size_px, image_size_px), color=BG_COLOR)

    # Start drawing the artwork by connecting the nodes and changing the colors.
    n_points = len(art.nodes)
    for i in range(n_points):

        node = art.nodes[i]
        if i == n_points - 1:
            next_node = art.nodes[0]
        else:
            next_node = art.nodes[i + 1]

        # Get the right color.
        color_factor = abs(((i * 2) / n_points) - 1)
        line_color = Color.interpolate(art.end_color, art.start_color, color_factor)

        # Overlay the image so it looks like 'light'.
        overlay = Image.new("RGB", (image_size_px, image_size_px), color=BLACK)
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.line(
            [node.xy(2), next_node.xy(2)],
            fill=line_color,
            width=node.thickness,
        )
        image = ImageChops.add(image, overlay)

    # Anti-alias the image.
    image = image.resize(
        (image_size_px // 2, image_size_px // 2), resample=Image.ANTIALIAS
    )
    image.save(output_path)
    return image
