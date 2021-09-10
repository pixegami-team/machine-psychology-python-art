import os
import json

from PIL import Image, ImageFont, ImageDraw

from art_name_generator import generate_name_with_retry
from artwork_metadata import ArtworkMetadata

from color_name import ColorNameMapper
from generate_art import (
    generate_art_code,
    generate_art_from_code,
    generate_end_color,
    generate_starting_color,
)

COLOR_NAME_MAPPER = ColorNameMapper("src/color_names.json")


def generate_collection(
    collection_id: str,
    folder_path: str,
    n: int,
    start_index: int = 1,
    use_ai: bool = True,
):
    collection_path = os.path.join(folder_path, collection_id)
    os.makedirs(collection_path, exist_ok=True)

    for i in range(start_index, start_index + n):
        generate_single_artwork(collection_id, collection_path, i, use_ai)


def generate_single_artwork(
    collection_id: str, collection_path: str, item_id: int, use_ai: bool = True
):

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
    code = generate_art_code(start_color, end_color)
    image = generate_art_from_code(code, item_art_path)

    # Generate the meta-data.
    metadata = ArtworkMetadata()
    metadata.start_color_name = COLOR_NAME_MAPPER.get(start_color).name
    metadata.end_color_name = COLOR_NAME_MAPPER.get(end_color).name
    metadata.title = "Untitled 404"
    metadata.item_id = item_id_str
    metadata.code = code

    # Generate the name
    if use_ai:
        title = generate_name_with_retry(
            metadata.start_color_name, metadata.end_color_name
        )
    else:
        title = "Untitled"
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
    card_padding = 64
    preview_color = (255, 255, 255)
    text_id_color = (150, 150, 180)
    text_meta_data_color = (120, 120, 140)
    text_code_color = (190, 190, 210)
    font_name = "font/RobotoMono-Regular.ttf"
    font_bold_name = "font/RobotoMono-Bold.ttf"

    im_size = 256

    preview_width = 3 * card_padding + card_width + im_size
    preview_height = 2 * card_padding + im_size
    preview = Image.new("RGB", (preview_width, preview_height), color=preview_color)

    # Add the original image.
    image_resized = image.resize((im_size, im_size), resample=Image.ANTIALIAS)
    preview.paste(image_resized, (card_padding, card_padding))

    # Draw meta-data.
    font = ImageFont.truetype(font_name, 24)
    color_font = ImageFont.truetype(font_name, 16)
    code_font = ImageFont.truetype(font_bold_name, 14)
    draw = ImageDraw.Draw(preview)

    tx = 2 * card_padding + im_size
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
    ty += title_height + 8

    # Colors
    color_set = set([metadata.start_color_name, metadata.end_color_name])
    color_set_str = ", ".join(color_set)
    color_text = f"Colors: {color_set_str}"
    draw.text((tx, ty), color_text, fill=text_meta_data_color, font=color_font)

    # Art Code
    code_char_w, code_char_h = code_font.getsize("A")
    max_code_chars = card_width // code_char_w
    code_text_arr = []
    code_pointer = max_code_chars
    previous_pointer = 0

    for _ in range(1 + len(metadata.code) // code_pointer):
        code_part = metadata.code[previous_pointer:code_pointer]
        code_text_arr.append(code_part)
        previous_pointer = code_pointer
        code_pointer += max_code_chars

    code_text = "\n".join(code_text_arr)
    code_height = code_char_h * (len(code_text_arr) + 1)
    ty = preview_height - card_padding - code_height
    draw.text((tx, ty), code_text, fill=text_code_color, font=code_font)

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

        if best_delta is None or abs(delta) < best_delta:
            best_delta = abs(delta)
            best_size = mid

        if delta > 0:
            upper = mid
        else:
            lower = mid

    return best_size
