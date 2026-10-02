# import re


# def clean_response_text(text: str) -> str:
#     """
#     Convert an AI response into short, TTS-friendly plain text.
#     """

#     if not text:
#         return ""

#     # Remove bold / italic markdown markers.
#     text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
#     text = re.sub(r"__(.*?)__", r"\1", text)

#     # Remove remaining asterisks.
#     text = text.replace("*", "")

#     # Remove inline code markers.
#     text = text.replace("`", "")

#     # Remove markdown headings.
#     text = re.sub(
#         r"^\s*#+\s*",
#         "",
#         text,
#         flags=re.MULTILINE,
#     )

#     # Convert markdown bullets into plain text.
#     text = re.sub(
#         r"^\s*[-•]\s*",
#         "",
#         text,
#         flags=re.MULTILINE,
#     )

#     # Remove excessive whitespace.
#     text = re.sub(
#         r"[ \t]+",
#         " ",
#         text,
#     )

#     # Normalize excessive newlines.
#     text = re.sub(
#         r"\n{2,}",
#         "\n",
#         text,
#     )

#     return text.strip()


import re


def clean_response_text(text: str) -> str:
    """
    Convert an AI response into clean,
    natural, TTS-friendly plain text.
    """

    if not text:
        return ""

    # Remove code blocks
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )

    # Remove inline code markers
    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text,
    )

    # Remove Markdown links
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    # Remove bold Markdown
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
    )

    # Remove italic Markdown
    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
    )

    # Remove single asterisk emphasis
    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
        text,
    )

    # Remove underscore emphasis
    text = re.sub(
        r"_(.*?)_",
        r"\1",
        text,
    )

    # Remove Markdown headings
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove bullet markers
    text = re.sub(
        r"^\s*[-•+]\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove numbered list formatting
    text = re.sub(
        r"^\s*\d+\.\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove blockquote markers
    text = re.sub(
        r"^\s*>\s?",
        "",
        text,
        flags=re.MULTILINE,
    )

    # Remove remaining Markdown characters
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")

    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Normalize excessive newlines
    text = re.sub(
        r"\n{2,}",
        "\n",
        text,
    )

    return text.strip()