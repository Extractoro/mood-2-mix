import re


def contains_banned_word(text: str, banned_words: set[str]) -> bool:
    words = re.findall(r'\w+', text.lower())
    return any(word in banned_words for word in words)
