import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_stop_words():
    file_path = os.getenv("STOPWORDS_PATH", "../stopwords")
    file_pathname = os.path.join(file_path, "stop_words.json")
    if not os.path.exists(file_pathname):
        return []

    with open(file_pathname) as f:
        data = json.load(f)
        return data.get("stop_words", [])


if __name__ == "__main__":  # pragma: no cover
    stop_words = get_stop_words()
    print(stop_words)
