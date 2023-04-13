import json

import pytest


# Used to test add stopwords
@pytest.fixture
def tmp_stop_words(tmp_path):
    stop_words_file = tmp_path / "stop_words.json"
    stop_words = ["words", "provided", "by", "the", "fixture"]
    with open(stop_words_file, "w") as f:
        json.dump({"stop_words": stop_words}, f, indent=4)
    return stop_words_file


# Used to test user input of add stopwords
@pytest.fixture
def custom_args():
    class CustomNamespace:
        def __init__(self, words, file_path, file_name):
            self.words = words
            self.file_path = file_path
            self.file_name = file_name

    custom_args = CustomNamespace(
        words=["word1", "word2"],
        file_path="./custom_stopwords",
        file_name="custom_stop_words.json",
    )

    return custom_args


@pytest.fixture(params=[
    ("", "./custom_stopwords", "custom_stop_words.json"),
    (["word1", "word2"], "", "custom_stop_words.json"),
    (["word1", "word2"], "./custom_stopwords", "")
], ids=["no_words_raises_error", "no_file_path", "no_file_name"])
def custom_args_missing(request):
    class CustomNamespace:
        def __init__(self, words, file_path, file_name):
            self.words = words or []
            self.file_path = file_path or "./stopwords"
            self.file_name = file_name or "stop_words.json"

    return CustomNamespace(*request.param)
