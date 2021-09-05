import os
import json

from PIL import Image, ImageFont, ImageDraw

from src.art_name_generator import generate_name

from src.color_name import ColorNameMapper
from src.generate_art import (
    generate_art_by_color,
    generate_end_color,
    generate_starting_color,
)

COLOR_NAME_MAPPER = ColorNameMapper("src/color_names.json")


class ArtworkMetadata:
    def __init__(self) -> None:
        self.item_id: str = ""
        self.title: str = ""
        self.start_color_name: str = ""
        self.end_color_name: str = ""

    def serialize(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "start_color_name": self.start_color_name,
            "end_color_name": self.end_color_name,
        }


def generate_collection(
    collection_id: str, folder_path: str, n: int, start_index: int = 1
):
    collection_path = os.path.join(folder_path, collection_id)
    os.makedirs(collection_path, exist_ok=True)

    for i in range(start_index, start_index + n):
        generate_single_artwork(collection_id, collection_path, i)


def generate_single_artwork(collection_id: str, collection_path: str, item_id: int):

    art_path = os.path.join(collection_path, "art")
    os.makedirs(art_path, exist_ok=True)

    meta_path = os.path.join(collection_path, "meta")
    os.makedirs(meta_path, exist_ok=True)

    preview_path = os.path.join(collection_path, "preview")
    os.makedirs(preview_path, exist_ok=True)

    item_id_str = str(item_id).zfill(3)
    item_name = f"{collection_id}_{item_id_str}"
    item_art_path = os.path.join(art_path, f"{item_name}.png")

    # Generate the actual artwork.
    start_color = generate_starting_color()
    end_color = generate_end_color(start_color)
    image = generate_art_by_color(start_color, end_color, item_art_path)

    # Generate the meta-data.
    metadata = ArtworkMetadata()
    metadata.start_color_name = COLOR_NAME_MAPPER.get(start_color).name
    metadata.end_color_name = COLOR_NAME_MAPPER.get(end_color).name
    metadata.title = "Untitled"
    metadata.item_id = item_id_str

    # Generate the name
    title = generate_name(metadata.start_color_name, metadata.end_color_name)
    metadata.title = title.upper()

    # Save the meta-data.
    metadata_file_path = os.path.join(meta_path, f"{item_id_str}.json")
    with open(metadata_file_path, "w") as f:
        json.dump(metadata.serialize(), f, indent=4)

    # Save meta-data preview as well.
    preview = generate_preview_image(image, metadata)
    item_preview_path = os.path.join(preview_path, f"{item_name}_preview.png")
    preview.save(item_preview_path)


def generate_preview_image(image: Image, metadata: ArtworkMetadata):
    card_width = 512
    card_padding = 32
    preview_color = (255, 255, 255)
    text_id_color = (150, 150, 180)
    text_meta_data_color = (120, 120, 140)
    font_name = "font/RobotoMono-Regular.ttf"

    im_width, im_height = image.size

    preview_width = 3 * card_padding + card_width + im_width
    preview_height = 2 * card_padding + im_height
    preview = Image.new("RGB", (preview_width, preview_height), color=preview_color)

    # Add the original image.
    preview.paste(image, (card_padding, card_padding))

    # Draw meta-data.
    font = ImageFont.truetype(font_name, 24)
    color_font = ImageFont.truetype(font_name, 16)
    draw = ImageDraw.Draw(preview)

    tx = 2 * card_padding + im_width
    ty = card_padding

    # Image ID
    draw.text((tx, ty), metadata.item_id, fill=text_id_color, font=font)
    _, id_height = font.getsize(metadata.item_id)
    ty += id_height + 4

    # Image title
    title_font_size = get_best_font_size(
        font_name, metadata.title, card_width, max_size=24
    )
    title_font = ImageFont.truetype(font_name, title_font_size)
    _, title_height = title_font.getsize(metadata.title)
    draw.text((tx, ty), metadata.title, fill=(10, 10, 15), font=title_font)
    ty += title_height + 4

    # Colors
    color_set = set([metadata.start_color_name, metadata.end_color_name])
    color_set_str = ", ".join(color_set)
    color_text = f"Colors: {color_set_str}"
    _, color_height = color_font.getsize(color_text)
    ty = preview_height - card_padding - color_height
    draw.text((tx, ty), color_text, fill=text_meta_data_color, font=color_font)

    return preview


def get_best_font_size(font, word: str, screen_width: int, max_size: int) -> int:

    # Pick the one that minimizes the delta.
    delta = None
    best_delta = None
    best_size = None
    mid = max_size // 2
    lower = 0
    upper = max_size

    while (upper - 1) > lower:

        mid = (lower + upper) // 2
        test_font = ImageFont.truetype(font, mid)
        max_line_length, _ = test_font.getsize(word)
        delta = max_line_length - screen_width

        print(f"Font: {mid}, Delta: {delta}")
        if best_delta is None or abs(delta) < best_delta:
            best_delta = abs(delta)
            best_size = mid

        if delta > 0:
            upper = mid
        else:
            lower = mid

    print(f"Best size: {best_size}")
    return best_size
