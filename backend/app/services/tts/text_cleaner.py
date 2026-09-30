import re


def clean_text_for_tts(text: str) -> str:
    """
    Convert Markdown-style LLM output into
    clean natural-language text for TTS.
    """

    if not text:
        return ""

    # Remove code blocks.
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )

    # Remove inline code markers.
    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text,
    )

    # Convert Markdown links:
    # [text](url) -> text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    # Remove bold/italic markers.
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
    )

    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"_(.*?)_",
        r"\1",
        text,
    )

    # Remove Markdown headings.
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove bullet markers.
    text = re.sub(
        r"^\s*[-*+]\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove numbered-list formatting.
    text = re.sub(
        r"^\s*\d+\.\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove blockquote marker.
    text = re.sub(
        r"^\s*>\s?",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove remaining Markdown emphasis characters.
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")

    # Normalize whitespace.
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Avoid excessive blank lines.
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()