import argparse
from generate_collection import generate_collection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str)
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    collection = args.collection
    n = args.n

    collection_path = f"collection_output"
    generate_collection(collection, collection_path, n)


if __name__ == "__main__":
    main()
