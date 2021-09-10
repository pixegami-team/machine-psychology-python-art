import openai
import os


def _new_example(c1: str, c2: str, name: str):
    return f"[{c1}, {c2}]: {name} #"


def generate_name_with_retry(
    start_color: str, end_color: str, name_set: set = None, max_retry: int = 3
):
    for _ in range(max_retry):
        name = generate_name(start_color, end_color, name_set=name_set)
        if name is not None:
            return name

    raise Exception(f"Unable to find name after {max_retry} retries")


def generate_name(start_color: str, end_color: str, name_set: set = None):

    if openai.api_key is None:
        if "OPENAI_API_KEY" not in os.environ:
            return "Untitled"
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    examples = [
        _new_example("Black", "Red Ochre", "Give love a chance"),
        _new_example("Ocean Blue", "Emerald", "Patterns of thought"),
        _new_example("Gold", "Picton Blue", "Royal Tsunami"),
        _new_example("Malachite", "Spring Green", "Crystalline Havana"),
        _new_example("Purple", "Deep Koamaru", "The silent void"),
        _new_example("Clementine", "Red", "Flamingo sunset"),
        _new_example("Zest", "Bright Turquoise", "Lullaby"),
    ]

    prompt = (
        f"Poetic titles of abstract artwork based on color: \n\n"
        + "\n".join(examples)
        + f"\n[{start_color}, {end_color}]:"
    )

    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=24,
        stop=["#"],
        temperature=0.9,
        presence_penalty=0.7,
        frequency_penalty=0.7,
        n=2,
    )

    titles = [r["text"].strip("\n").strip(" ") for r in response["choices"]]
    titles.sort(key=lambda x: len(x))
    print(f"Possible Names: {titles}")

    if name_set is not None:
        # Avoid naming collisions.
        for title in titles:
            if title not in name_set:
                name_set.add(title)
                return title
        return None
    else:
        art_title = titles[0]
        return art_title
