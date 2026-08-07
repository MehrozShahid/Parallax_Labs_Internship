import re

MAX_TEXT_LENGTH = 100000

def remove_html(text):
    return re.sub(r'<.*?>', '', text)


def remove_special_chars(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()


def clean_text(text):

    # Handle None or non-string values
    if not isinstance(text, str):
        return ""

    # Handle empty strings
    if text.strip() == "":
        return ""

    # Handle extremely long text
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    # Clean text
    text = remove_html(text)
    text = remove_special_chars(text)
    text = normalize_whitespace(text)

    return text