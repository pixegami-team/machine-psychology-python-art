from typing import Tuple
from PIL import Image, ImageDraw, ImageChops
import random


def interpolate(c1: Tuple[int], c2: Tuple[int], f: float):
    rf = 1 - f
    return tuple([int((f * c1[i] + rf * c2[i])) for i in range(3)])


def generate_art(output_path: str):
    print("Generating art!")

    default_color = (25, 15, 35)
    black = (0, 0, 0)

    # line_color = (0, 150, 30)

    start_color = (0, 150, 50)
    end_color = (50, 50, 150)

    image_size_px = 512
    padding_px = 64
    iterations = 12
    max_thickness = 12
    min_thickness = 2
    shape_close_off = 3

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
    thickness_mod = 1

    n_points = len(points)
    for i in range(n_points):

        current_thickness = current_thickness + thickness_mod
        if current_thickness == max_thickness:
            thickness_mod = -1
        if current_thickness == min_thickness:
            thickness_mod = 1
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
