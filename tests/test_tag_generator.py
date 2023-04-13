from nltk import FreqDist
import pytest
from src.tag_generator import (calculate_word_freq, extract_words_from_directory, preprocess_text, extract_top_tags,
                               remove_code_blocks, remove_markdown_headers)
from heapq import nlargest


def test_remove_markdown_headers():
    sample_text = """
    This is a sample text.

    ---
    This is a header that should be removed.
    ---

    This is another sample text.
    ---
    Another header to remove.
    ---
    """

    removed_texts = [
        "This is a header that should be removed.",
        "Another header to remove.",
    ]

    expected_texts = ["This is a sample text.", "This is another sample text."]

    cleaned_text = remove_markdown_headers(sample_text)

    all_removed = True
    for removed_text in removed_texts:
        if removed_text in cleaned_text:
            all_removed = False
            break

    all_expected_present = True
    for expected_text in expected_texts:
        if expected_text not in cleaned_text:
            all_expected_present = False
            break

    assert all_removed
    assert all_expected_present


def test_remove_code_blocks():
    sample_text = """
    This is a sample text.

    ```
    This is a code block that should be removed.
    ```

    This is another sample text.
    ```
    Another code block to remove.
    ```
    """
    removed_texts = [
        "This is a code block that should be removed.",
        "Another code block to remove.",
    ]
    expected_texts = ["This is a sample text.", "This is another sample text."]

    cleaned_text = remove_code_blocks(sample_text)

    all_removed = True
    for removed_text in removed_texts:
        if removed_text in cleaned_text:
            all_removed = False
            break

    all_expected_present = True
    for expected_text in expected_texts:
        if expected_text not in cleaned_text:
            all_expected_present = False
            break

    assert all_removed
    assert all_expected_present


def test_preprocess_text_without_stop_words():
    sample_text = """
    This is a sample text for testing the tag generator.
    The tag generator should return the most relevant tags for this text.
    """
    test_stop_words = []
    generated_tags = preprocess_text(sample_text, custom_stopwords=test_stop_words)

    expected_tags = ['sample', 'text', 'testing', 'tag', 'generator', 'tag', 'generator', 'return', 'relevant', 'tag', 'text']
    assert len(generated_tags) == 11
    assert "sample" in generated_tags
    assert "text" in generated_tags
    assert "testing" in generated_tags
    assert "tag" in generated_tags
    assert "generator" in generated_tags
    assert "return" in generated_tags
    assert "relevant" in generated_tags


def test_extract_top_tags():
    words = ["sample", "text", "testing", "tag", "generator", "tag", "generator", "return", "relevant", "tag", "text"]
    word_freq = calculate_word_freq(words)
    top_tags = extract_top_tags(n_top=5, word_freq=word_freq)
    assert top_tags == ['tag', 'text', 'generator', 'sample', 'testing']


def test_preprocess_text_with_stop_words():
    sample_text = """
    This is a sample text for testing the tag generator.
    The tag generator should return the most relevant tags for this text.
    """
    test_stop_words = {"tag", "sample"}

    generated_tags = preprocess_text(sample_text, custom_stopwords=test_stop_words)
    expected_tags = ['text', 'testing', 'generator', 'generator', 'return', 'relevant',  'text']

    assert len(generated_tags) == len(expected_tags)
    assert "sample" not in generated_tags
    assert "tag" not in generated_tags

    assert "text" in generated_tags
    assert "testing" in generated_tags
    assert "generator" in generated_tags
    assert "return" in generated_tags
    assert "relevant" in generated_tags


def test_extract_content_from_directory(tmp_path):
    # Create a temporary directory with sample Markdown files
    sample_files = {
        "file1.md": "This is a sample text in file1.",
        "file2.md": "This is another sample text in file2.",
    }
    for file_name, content in sample_files.items():
        file_path = tmp_path / file_name
        with open(file_path, "w") as file:
            file.write(content)

    # Test get_tags_for_directory function
    tags_dict = extract_words_from_directory(tmp_path)
    assert len(tags_dict) == 2
    assert tags_dict["file1.md"] != []
    assert tags_dict["file2.md"] != []


if __name__ == "__main__":
    pytest.main()
