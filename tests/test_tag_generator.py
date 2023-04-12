import os
import tempfile
from collections import defaultdict

import pytest
from src.tag_generator import (generate_tags, get_tags_for_directory,
                               remove_code_blocks, remove_markdown_headers)


def test_remove_markdown_headers():
    sample_text = '''
    This is a sample text.

    ---
    This is a header that should be removed.
    ---

    This is another sample text.
    ---
    Another header to remove.
    ---
    '''

    removed_texts = [
        "This is a header that should be removed.",
        "Another header to remove."
    ]

    expected_texts = [
        "This is a sample text.",
        "This is another sample text."
    ]

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
    sample_text = '''
    This is a sample text.

    ```
    This is a code block that should be removed.
    ```

    This is another sample text.
    ```
    Another code block to remove.
    ```
    '''
    removed_texts = [
        "This is a code block that should be removed.",
        "Another code block to remove."
    ]
    expected_texts = [
        "This is a sample text.",
        "This is another sample text."
    ]

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


def test_generate_tags():
    sample_text = """
    This is a sample text for testing the tag generator.
    The tag generator should return the most relevant tags for this text.
    """
    # expected_tags = ["tag", "generator", "text", "sample", "testing"]
    generated_tags = generate_tags(sample_text, num_tags=5)
    assert len(generated_tags) == 5
    assert "tag" in generated_tags
    assert "generator" in generated_tags
    assert "text" in generated_tags
    assert "sample" in generated_tags
    assert "testing" in generated_tags


def test_get_tags_for_directory(tmp_path):
    # Create a temporary directory with sample Markdown files
        sample_files = {
            "file1.md": "This is a sample text in file1.",
            "file2.md": "This is another sample text in file2.",
        }
        for file_name, content in sample_files.items():
            file_path = tmp_path / file_name
            with open(file_path, "w") as file:
                file.write(content)
        print(tmp_path)

        # Test get_tags_for_directory function
        tags_dict = defaultdict(list)
        tags_dict = get_tags_for_directory(tmp_path)
        assert len(tags_dict) == 2
        assert tags_dict["file1.md"] == ["sample", "text", "file1"]
        assert tags_dict["file2.md"] == ["another", "sample", "text", "file2"]


if __name__ == "__main__":
    pytest.main()
