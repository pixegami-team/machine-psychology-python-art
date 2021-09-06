from src.generate_collection import generate_collection
import uuid


def test_generate_collection():
    collection_id = "test"
    collection_path = f"tst_output"
    generate_collection(collection_id, collection_path, 3)


def test_generate_collection_skip_ai():
    collection_id = "test"
    collection_path = f"tst_output"
    generate_collection(collection_id, collection_path, 32, use_ai=False)
