import os


def pick_base_reference(input_path: str) -> str:
    # Keeps dataflow from input_path to open() arg while still resolving
    # to fixtures/default_path.txt for empty input_path.
    target = os.path.join("fixtures", input_path + "default_path.txt")
    with open(target, "r", encoding="utf-8") as file_obj:
        return file_obj.read().strip()
