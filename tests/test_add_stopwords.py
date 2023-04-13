import os
import json
import pytest
import argparse

from src.add_stopwords import add_stop_words, user_input


def test_user_input(monkeypatch, custom_args):
    # Replace the original parse_args method with the custom implementation
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", lambda *args, **kwargs: custom_args)

    # Call the user_input function
    result = user_input()

    # Define the expected output
    expected_file_path = os.path.join("./custom_stopwords", "stop_words.json")
    expected_result = (expected_file_path, "./custom_stopwords", "custom_stop_words.json", ["word1", "word2"])

    # Check if the result matches the expected output
    assert result == expected_result


def test_user_input_missing_args(capsys, monkeypatch, custom_args_missing):
    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", lambda *args, **kwargs: custom_args_missing)

    if custom_args_missing.words == "":

        with pytest.raises(argparse.ArgumentError) as e:
            user_input()

        captured = capsys.readouterr()
        assert "error: the following arguments are required: words" in captured.err
        assert e.type == SystemExit
        assert e.value.code == 2  # Exit code 2 for argparse error

    else:
        result = user_input()
        expected_file_path = os.path.join(custom_args_missing.file_path, "stop_words.json")
        expected_result = (expected_file_path, custom_args_missing.file_path, custom_args_missing.file_name, custom_args_missing.words)
        assert result == expected_result


def test_add_stop_words_to_json(tmp_path, tmp_stop_words):
    file_path = tmp_path
    file_name = "stop_words.json"
    words = ["cat", "dog", "bird"]
    add_stop_words(file_path, file_name, words)
    with open(tmp_stop_words) as f:
        data = json.load(f)
        assert data.get("stop_words") == [
            "words",
            "provided",
            "by",
            "the",
            "fixture",
            "cat",
            "dog",
            "bird"
        ]
