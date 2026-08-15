def clean_text(text):

    text = text.strip()

    if len(text) == 0:
        return ""

    text = text.lower()

    text = text.capitalize()

    if not text.endswith((".", "!", "?")):
        text += "."

    return text


if __name__ == "__main__":

    text = "hello how are you"

    result = clean_text(text)

    print(result)