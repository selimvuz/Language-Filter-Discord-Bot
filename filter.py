def filter_content(text):
    bad_words = ["fuck"]
    text_words = text.lower().split()

    return bool(set(text_words) & set(bad_words))