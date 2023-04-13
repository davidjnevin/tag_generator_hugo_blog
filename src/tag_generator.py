import os
import re
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from heapq import nlargest

from tags_db import get_stop_words

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('wordnet')


def remove_markdown_headers(text):
    # Remove lines between --- (Markdown headers)
    header_pattern = re.compile(r'---[\s\S]*?---')
    text = re.sub(header_pattern, '', text)
    return text


def remove_code_blocks(text):
    # Remove lines between ``` (code blocks)
    code_block_pattern = re.compile(r'```[\s\S]*?```')
    text = re.sub(code_block_pattern, '', text)
    return text


def preprocess_text(text, custom_stopwords={}):
    """
    Allow for custom stop words
    """
    # Ignore headers in markdown files "---" to "---"
    text = remove_markdown_headers(text)

    # Ignore code blocks in markdown file "```" to "```"
    text = remove_code_blocks(text)

    # Tokenize
    tokens = word_tokenize(text.lower())

    # Add custom stopwords if provided
    stop_words = set(stopwords.words("english"))
    existing_custom_stopwords = set(get_stop_words())
    if existing_custom_stopwords:
        stop_words.update(existing_custom_stopwords)
    if custom_stopwords:
        stop_words.update(custom_stopwords)

    # Remove stop words and punctuation
    clean_tokens = [token for token in tokens if token.isalnum()]
    lemmatizer = WordNetLemmatizer()

    words = [lemmatizer.lemmatize(token) for token in clean_tokens]
    words_without_stop_words = [word for word in words if word not in stop_words]

    return words_without_stop_words


def calculate_word_freq(words):
    return FreqDist(words)


def extract_top_tags(word_freq, n_top=5):
    return nlargest(n_top, word_freq, key=word_freq.get)


def extract_words_from_directory(markdown_directory):
    tags_dict = defaultdict(list)
    # Iterate through the Markdown files and generate tags
    for file_name in os.listdir(markdown_directory):
        # "Python conditions added to limit responses in early development."
        if file_name.endswith(".md"):
            file_path = os.path.join(markdown_directory, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                words = preprocess_text(content)
                word_freq = calculate_word_freq(words)
                tags_dict[file_name] = extract_top_tags(word_freq, n_top=5)
    return tags_dict


def print_tags_per_post(tags_dict):
    # Print tags for each file
    for file_name, tags in tags_dict.items():
        print(f'{file_name}: {", ".join(tags)}')


if __name__ == "__main__":  # pragma: no cover
    MARKDOWN_DIR = "/Users/Communitymanager-work/Google Drive/DJNWebsite/djnProfessional/djnevinProfessional/content/code"
    tags = extract_words_from_directory(MARKDOWN_DIR)
    print_tags_per_post(tags)
