from app.services.llm.gemini import gemini_service
from app.services.conversation.models import Conversation


QUERY_REWRITE_INSTRUCTION = """
You are a query rewriting component for a document-grounded
AI research assistant.

Your job is to rewrite the user's latest question into a
standalone search query that can be understood without
conversation history.

Rules:

1. Preserve the user's original intent.
2. Resolve references such as:
   - it
   - they
   - them
   - this
   - that
   - these
   - those
3. Use previous conversation only when necessary to resolve
   the meaning of the latest question.
4. Do not answer the question.
5. Do not add information that is not present in the conversation.
6. If the latest question is already standalone, return it
   unchanged.
7. Return ONLY the rewritten query.
"""


class QueryRewriter:

    def rewrite(
        self,
        conversation: Conversation,
        latest_query: str,
    ) -> str:

        if not latest_query.strip():
            raise ValueError(
                "Latest query cannot be empty"
            )

        if not conversation.turns:
            return latest_query.strip()

        history_parts = []

        for turn in conversation.turns:

            history_parts.append(
                f"User: {turn.user_message}\n"
                f"Assistant: {turn.assistant_message}"
            )

        history = "\n\n".join(
            history_parts
        )

        prompt = f"""
{QUERY_REWRITE_INSTRUCTION}

Conversation history:

{history}

Latest user question:

{latest_query}

Standalone search query:
"""

        rewritten_query = gemini_service.generate(
            prompt
        )

        return rewritten_query.strip()


query_rewriter = QueryRewriter()