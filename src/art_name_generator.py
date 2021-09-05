import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def new_example(c1: str, c2: str, name: str):
    return f"[{c1}, {c2}]: {name} #"


def generate_name(start_color: str, end_color: str, name_set: set = None):

    examples = [
        new_example("Black", "Red Ochre", "Waiting for death"),
        new_example("Ocean Blue", "Emerald", "Outworn patterns of thought"),
        new_example("Gold", "Picton Blue", "Royal ocean"),
        new_example("Malachite", "Spring Green", "The beauty of organic shapes"),
        new_example("Purple", "Deep Koamaru", "Void vector"),
        new_example("Clementine", "Red", "Flamingo sunset"),
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
        temperature=0.8,
        presence_penalty=0.5,
        frequency_penalty=0.5,
        n=3,
    )

    titles = [r["text"].strip("\n").strip(" ") for r in response["choices"]]

    if name_set is not None:
        # Avoid naming collisions.
        for title in titles:
            art_title = title
            if art_title not in name_set:
                break
        name_set.add(art_title)
    else:
        art_title = titles[0]

    print(art_title)
    return art_title
