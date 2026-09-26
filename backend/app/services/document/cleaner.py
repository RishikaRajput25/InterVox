import re


def clean_text(text: str) -> str:
    # Replace non-breaking spaces with normal spaces
    text = text.replace("\xa0", " ")

    # Normalize Windows and old-style line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove spaces/tabs at the beginning and end of each line
    lines = [
        line.strip()
        for line in text.split("\n")
    ]

    # Remove completely empty lines
    lines = [
        line
        for line in lines
        if line
    ]

    # Join lines back together
    text = "\n".join(lines)

    # Replace multiple spaces/tabs inside a line with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Limit excessive consecutive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()