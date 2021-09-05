from typing import Tuple
from PIL import Image, ImageDraw, ImageChops
import random
import colorsys


def interpolate(c1: Tuple[int], c2: Tuple[int], f: float):
    rf = 1 - f
    return tuple([int((f * c1[i] + rf * c2[i])) for i in range(3)])


def generate_starting_color():
    h = random.random()
    s = 0.7 + 0.3 * random.random()
    v = 0.7 + 0.3 * random.random()
    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple(map(lambda x: int(x * 255), float_rgb))


def generate_end_color(start_color):
    # Convert color into HSV.
    h, s, v = colorsys.rgb_to_hsv(*map(lambda x: x / 255, start_color))
    h += 0.1 + random.random() * 0.5
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
    print("Generating art!")

    black = (0, 0, 0)

    start_color = generate_starting_color()
    end_color = generate_end_color(start_color)
    default_color = (25, 28, 42)

    image_size_px = 512
    padding_px = 50
    iterations = 12
    max_thickness = 12
    min_thickness = 2
    shape_close_off = 4

    image = Image.new("RGB", (image_size_px, image_size_px), color=default_color)
    # draw = ImageDraw.Draw(image)

    points = []

    # Generate a bunch of random points.
    min_p = padding_px
    max_p = image_size_px - padding_px

    for i in range(iterations):
        x = random.randint(min_p, max_p)
        y = random.randint(min_p, max_p)
        new_point = (x, y)
        points.append(new_point)

        # Everytime we close off a shape, we add the starting point.
        if i % shape_close_off == 0 and i != 0:
            points.append(points[-shape_close_off])

    # Add the first point back to the end, so it closes the shape.
    points.append(points[0])

    # Center the shape.
    min_x = min([x for x, _ in points])
    min_y = min([y for _, y in points])
    max_x = max([x for x, _ in points])
    max_y = max([y for _, y in points])
    x_offset = ((image_size_px - max_x) - min_x) // 2
    y_offset = ((image_size_px - max_y) - min_y) // 2
    points = [(x + x_offset, y + y_offset) for x, y in points]

    current_thickness = min_thickness
    thickness_mod = 2

    n_points = len(points)
    for i in range(n_points):

        current_thickness = current_thickness + thickness_mod
        if current_thickness == max_thickness:
            thickness_mod = -2
        if current_thickness == min_thickness:
            thickness_mod = 2
        current_point = points[i]
        if i == n_points - 1:
            next_point = points[0]
        else:
            next_point = points[i + 1]

        # Get the right color.
        color_factor = abs(((i * 2) / n_points) - 1)
        line_color = interpolate(end_color, start_color, color_factor)

        overlay = Image.new("RGB", (image_size_px, image_size_px), color=black)
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.line(
            [current_point, next_point],
            fill=line_color,
            width=current_thickness,
        )
        image = ImageChops.add(image, overlay)

    # draw.line(points, fill=line_color, width=4, joint="curve")
    image = image.resize(
        (image_size_px // 2, image_size_px // 2), resample=Image.ANTIALIAS
    )
    image.save(output_path)
    overlay.save("tst_output/overlay.png")


if __name__ == "__main__":
    generate_art()
