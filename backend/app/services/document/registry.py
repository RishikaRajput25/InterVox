from app.models.document import Document


class DocumentRegistry:
    def __init__(self):
        self._documents: dict[str, Document] = {}

    def add(self, document: Document) -> None:
        self._documents[document.document_id] = document

    def get(self, document_id: str) -> Document | None:
        return self._documents.get(document_id)

    def update(self, document: Document) -> None:
        self._documents[document.document_id] = document


document_registry = DocumentRegistry()