from src.generate_art import generate_art
import os

OUTPUT_FOLDER = "tst_output"
OUTPUT_PATH = f"{OUTPUT_FOLDER}/test_image.png"


def test_generate_art():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    generate_art(OUTPUT_PATH)
