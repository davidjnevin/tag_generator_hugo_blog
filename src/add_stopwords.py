import argparse
import json
import os


def add_stop_words(file_path, file_name, words):
    """Create the directory if it doesn't exist."""
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name_path = os.path.join(file_path, file_name)

    """Create the file if it doesn't exist."""
    if not os.path.exists(file_name_path):
        with open(file_name_path, "w") as f:
            json.dump({"stop_words": []}, f, indent=4)

    """Append the new stop words to the file."""
    with open(file_name_path, "r+") as f:
        data = json.load(f)
        data["stop_words"].extend(words)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def user_input():
    parser = argparse.ArgumentParser(description="Add stop words to a JSON file")
    parser.add_argument("words", nargs="+", help="Words to be added to the stop words list")
    parser.add_argument(
        "--file-path",
        default="./stopwords",
        help="Path to the directory for the JSON file (default: ./stopwords)",
    )
    parser.add_argument(
        "--file-name",
        default="stop_words.json",
        help="Name of the JSON file (default: stop_words.json)",
    )
    args = parser.parse_args()
    file_path = os.path.join(args.file_path, "stop_words.json")
    return (file_path, args.file_path, args.file_name, args.words)


if __name__ == "__main__":  # pragma: no cover
    file_path, arg_filepath, arg_filename, arg_words = user_input()
    add_stop_words(arg_filepath, arg_filename, arg_words)


