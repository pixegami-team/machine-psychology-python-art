import argparse
import os
import json


def main():
    """
    Check for duplicate names in the collection.
    """

    # Get the collection argument.
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str)
    args = parser.parse_args()
    collection = args.collection
    meta_folder = f"collection_output/{collection}/meta/"
    files = os.listdir(meta_folder)

    # Keep a record.
    registry = {}

    for file_name in files:
        file_path = os.path.join(meta_folder, file_name)

        with open(file_path, "r") as f:
            data = json.load(f)

        item_id = data["item_id"]
        title = data["title"]

        if title not in registry:
            registry[title] = []

        registry[title].append(item_id)

    # Print the duplicates.
    for k, v in registry.items():
        if len(v) > 1:
            print(f"Duplicate: {k, v}")


if __name__ == "__main__":
    main()
