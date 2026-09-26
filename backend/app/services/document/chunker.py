# import re
# from uuid import uuid4


# DEFAULT_CHUNK_SIZE = 800
# DEFAULT_CHUNK_OVERLAP = 150


# def find_chunk_end(
#     text: str,
#     start: int,
#     chunk_size: int,
# ) -> int:
#     """
#     Find a natural place to end the chunk.

#     Preference:
#     1. Paragraph boundary
#     2. Sentence boundary
#     3. Word boundary
#     4. Hard character limit
#     """

#     target_end = min(
#         start + chunk_size,
#         len(text)
#     )

#     if target_end >= len(text):
#         return len(text)

#     # Look for a paragraph boundary.
#     paragraph_break = text.rfind(
#         "\n\n",
#         start,
#         target_end
#     )

#     if paragraph_break > start:
#         return paragraph_break

#     # Look for a sentence boundary.
#     sentence_matches = list(
#         re.finditer(
#             r"[.!?](?=\s|$)",
#             text[start:target_end]
#         )
#     )

#     if sentence_matches:
#         match = sentence_matches[-1]
#         return start + match.end()

#     # Look for a word boundary.
#     space_position = text.rfind(
#         " ",
#         start,
#         target_end
#     )

#     if space_position > start:
#         return space_position

#     # Last option: hard character limit.
#     return target_end

# def chunk_text(
#     text: str,
#     chunk_size: int = DEFAULT_CHUNK_SIZE,
#     chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
# ) -> list[str]:

#     if not text.strip():
#         return []

#     if chunk_overlap >= chunk_size:
#         raise ValueError(
#             "chunk_overlap must be smaller than chunk_size"
#         )

#     chunks = []

#     start = 0
#     text_length = len(text)

#     while start < text_length:

#         end = find_chunk_end(
#             text,
#             start,
#             chunk_size
#         )

#         chunk = text[start:end].strip()

#         if chunk:
#             chunks.append(chunk)

#         if end >= text_length:
#             break

#         # Calculate desired overlap position.
#         overlap_start = max(
#             start,
#             end - chunk_overlap
#         )

#         # Move forward to the beginning of the next word.
#         while (
#             overlap_start < end
#             and overlap_start > start
#             and not text[overlap_start].isspace()
#         ):
#             overlap_start += 1

#         # Skip whitespace.
#         while (
#             overlap_start < text_length
#             and text[overlap_start].isspace()
#         ):
#             overlap_start += 1

#         if overlap_start <= start:
#             overlap_start = end

#         start = overlap_start

#     return chunks

# def create_chunk_records(
#     pages: list[dict],
#     document_id: str,
#     filename: str,
#     chunk_size: int = DEFAULT_CHUNK_SIZE,
#     chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
# ) -> list[dict]:

#     chunk_records = []

#     for page in pages:

#         page_number = page["page_number"]
#         text = page["text"]

#         chunks = chunk_text(
#             text,
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#         )

#         for chunk in chunks:

#             chunk_records.append({
#                 "chunk_id": str(uuid4()),
#                 "document_id": document_id,
#                 "filename": filename,
#                 "page_number": page_number,
#                 "text": chunk,
#             })

#     return chunk_records







import re
from uuid import uuid4


DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 150


def find_chunk_end(
    text: str,
    start: int,
    chunk_size: int,
) -> int:
    """
    Find a natural place to end a chunk.

    Preference:
    1. Paragraph boundary
    2. Sentence boundary
    3. Word boundary
    4. Hard character limit
    """

    target_end = min(
        start + chunk_size,
        len(text)
    )

    if target_end >= len(text):
        return len(text)

    # 1. Prefer paragraph boundary
    paragraph_break = text.rfind(
        "\n\n",
        start,
        target_end
    )

    if paragraph_break > start:
        return paragraph_break

    # 2. Prefer sentence boundary
    sentence_matches = list(
        re.finditer(
            r"[.!?](?=\s|$)",
            text[start:target_end]
        )
    )

    if sentence_matches:
        match = sentence_matches[-1]

        return start + match.end()

    # 3. Prefer word boundary
    space_position = text.rfind(
        " ",
        start,
        target_end
    )

    if space_position > start:
        return space_position

    # 4. Hard character limit
    return target_end


def find_overlap_start(
    text: str,
    start: int,
    end: int,
    chunk_overlap: int,
) -> int:
    """
    Find a word-safe starting position for the next chunk.

    We try to keep approximately chunk_overlap characters,
    but never start in the middle of a word.
    """

    overlap_start = max(
        start,
        end - chunk_overlap
    )

    # If overlap starts in the middle of a word,
    # move forward until the next whitespace.
    while (
        overlap_start < end
        and overlap_start > start
        and not text[overlap_start].isspace()
    ):
        overlap_start += 1

    # Skip whitespace before the next word.
    while (
        overlap_start < len(text)
        and text[overlap_start].isspace()
    ):
        overlap_start += 1

    if overlap_start <= start:
        return end

    return overlap_start


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:

    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = find_chunk_end(
            text,
            start,
            chunk_size
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = find_overlap_start(
            text,
            start,
            end,
            chunk_overlap
        )

    return chunks


def create_chunk_records(
    pages: list[dict],
    document_id: str,
    filename: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """
    Convert cleaned page text into chunk records
    with metadata required for RAG and citations.
    """

    chunk_records = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk in chunks:

            chunk_records.append({
                "chunk_id": str(uuid4()),
                "document_id": document_id,
                "filename": filename,
                "page_number": page_number,
                "text": chunk,
            })

    return chunk_records