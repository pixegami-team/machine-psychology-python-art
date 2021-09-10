from src.art_name_generator import generate_name


def test_generate_title():
    test_name = generate_name("Electric Violet", "San Marino")
    print(f"Test name: {test_name}")
