def build_context(
    search_results: list[dict],
) -> str:

    if not search_results:
        return ""

    context_parts = []

    for index, result in enumerate(
        search_results,
        start=1,
    ):
        metadata = result.get("metadata", {})

        filename = metadata.get(
            "filename",
            "Unknown document"
        )

        page_number = metadata.get(
            "page_number",
            "Unknown"
        )

        text = result.get(
            "text",
            ""
        ).strip()

        if not text:
            continue

        context_parts.append(
            f"""SOURCE {index}
Document: {filename}
Page: {page_number}

Content:
{text}
"""
        )

    return "\n\n".join(context_parts)