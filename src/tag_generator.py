import os
import re
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

nltk.download("punkt")
nltk.download("averaged_preceptron_tagger")
nltk.download("stopwords")


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


def generate_tags(text, num_tags=5, custom_stopwords=None, bigram_limit=1):
    """
    Allow for custom stop words
    and avoids multiple tags being joined using underscores. (bigram_limit)
    """
    # Ignore headers in markdown files "---" to "---"
    text = remove_markdown_headers(text)

    # Ignore code blocks in markdown file "```" to "```"
    text = remove_code_blocks(text)

    # Preprocess text
    # text = text.lower()
    text = re.sub(r"\W+", " ", text)

    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))

    # Add custom stopwords if provided
    if custom_stopwords:
        stop_words.update(custom_stopwords)

    words = [token for token in tokens if token.isalpha and token not in stop_words]

    # Calculate word frequencies
    unigram_freq = nltk.FreqDist(words)

    # Find bigrams
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = nltk.BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(2)
    finder.apply_word_filter(lambda w: len(w) < 3)
    bigram_freq = finder.score_ngrams(bigram_measures.raw_freq)

    # Select top N unigrams
    top_unigrams = [word for word, _ in unigram_freq.most_common(num_tags)]

    # Select top N bigrams (limited by bigram_limit)
    top_bigrams = ['_'.join(words) for words, _ in bigram_freq[:bigram_limit]]

    # Combine unigrams and bigrams
    tags = top_unigrams + top_bigrams
    tags = tags[:num_tags]

    return tags


def print_tags_per_post(tags_dict):
    # Print tags for each file
    for file_name, tags in tags_dict.items():
        print(f'{file_name}: {", ".join(tags)}')


def get_tags_for_directory(markdown_directory):
    tags_dict = defaultdict(list)
    # Iterate through the Markdown files and generate tags
    for file_name in os.listdir(markdown_directory):
        # "Python conditions added to limit responses in early development."
        if file_name.endswith(".md") and "python" in file_name:
            file_path = os.path.join(markdown_directory, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                tags = generate_tags(content)
                tags_dict[file_name] = tags
    return tags_dict


def start_tag_generator():
    MARKDOWN_DIR = "/Users/Communitymanager-work/Google Drive/DJNWebsite/djnProfessional/djnevinProfessional/content/code"
    tags = get_tags_for_directory(MARKDOWN_DIR)
    print_tags_per_post(tags)


if __name__ == "__main__":
    start_tag_generator()
