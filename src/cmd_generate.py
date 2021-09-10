import argparse
from generate_collection import generate_collection


def main():
    """
    Generate a collection of machine-generated art.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str)
    parser.add_argument("-n", type=int)
    parser.add_argument("-i", type=int, default=1)
    args = parser.parse_args()

    collection = args.collection
    n = args.n
    i = args.i

    collection_path = f"collection_output"
    generate_collection(collection, collection_path, n, start_index=i)


if __name__ == "__main__":
    main()
