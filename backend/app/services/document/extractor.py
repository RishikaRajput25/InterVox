# from pathlib import Path

# import pymupdf


# def extract_pdf_text(file_path: Path) -> list[dict]:
#     pages = []

#     document = pymupdf.open(file_path)

#     try:
#         for page_number, page in enumerate(document, start=1):
#             text = page.get_text()

#             pages.append({
#                 "page_number": page_number,
#                 "text": text.strip(),
#             })
#     finally:
#         document.close()

#     return pages



from pathlib import Path

import pymupdf
from docx import Document as DocxDocument


def extract_pdf_text(file_path: Path) -> list[dict]:
    pages = []

    document = pymupdf.open(file_path)

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text().strip()

            # pages.append({
            #     "page_number": page_number,
            #     "text": text,
            # })
            text = page.get_text().strip()

            if text:
              pages.append({
               "page_number": page_number,
               "text": text,
            })
    finally:
        document.close()

    return pages


def extract_docx_text(file_path: Path) -> list[dict]:
    document = DocxDocument(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    full_text = "\n".join(paragraphs)

    return [
        {
            "page_number": 1,
            "text": full_text,
        }
    ]


def extract_txt_text(file_path: Path) -> list[dict]:
    text = file_path.read_text(
        encoding="utf-8",
        errors="replace",
    ).strip()

    return [
        {
            "page_number": 1,
            "text": text,
        }
    ]


def extract_document(file_path: Path) -> list[dict]:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    if extension == ".txt":
        return extract_txt_text(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )