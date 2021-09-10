from src.color_name import ColorNameMapper


def test_color_name():
    color_mapper = ColorNameMapper("src/color_names.json")

    assert color_mapper.get((255, 0, 0)).name == "Red"
    assert color_mapper.get((0, 255, 0)).name == "Green"
    assert color_mapper.get((0, 0, 255)).name == "Blue"
    assert color_mapper.get((0, 0, 0)).name == "Black"
    assert color_mapper.get((255, 255, 255)).name == "White"
    assert color_mapper.get((255, 150, 0)).name == "Pizazz"
    assert color_mapper.get((0, 200, 200)).name == "Robin's Egg Blue"
