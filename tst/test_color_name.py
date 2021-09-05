from src.color_name import ColorNameMapper


def test_color_name():
    color_mapper = ColorNameMapper("src/color_names.json")
    color_mapper.get((255, 100, 10))
    color_mapper.get((0, 100, 10))
    color_mapper.get((255, 0, 0))
    color_mapper.get((0, 255, 0))
    color_mapper.get((0, 0, 255))
    color_mapper.get((0, 0, 0))
    color_mapper.get((255, 255, 255))
