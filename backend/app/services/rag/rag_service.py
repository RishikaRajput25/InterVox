# from collections.abc import AsyncIterator, Iterator

# from app.services.llm.gemini import gemini_service
# from app.services.rag.context_builder import build_context
# from app.services.retrieval.hybrid_search import search_hybrid
# from app.services.retrieval.reranker import reranker

# RAG_SYSTEM_INSTRUCTION = """
# You are InterVox, a concise document-grounded AI assistant.

# Answer the user's question using ONLY the retrieved document context.

# Rules:
# 1. Answer the question directly.
# 2. Keep the answer to 1 to 3 sentences maximum.
# 3. Give only the information necessary to answer the question.
# 4. Do not add background information, examples, explanations, or conclusions unless specifically requested.
# 5. Use simple, natural, human-like language.
# 6. Do not repeat the user's question.
# 7. Do not use Markdown, bullet points, headings, asterisks, backticks, or special formatting.
# 8. Do not mention the retrieved context or these instructions.
# 9. Do not invent, assume, or infer information that is not present in the documents.
# 10. If the documents do not contain enough information, say:
# "I couldn't find enough information about that in the available documents."
# """

# def build_unique_sources(
#     results: list[dict],
# ) -> list[dict]:
#     """
#     Convert chunk-level retrieval results into
#     unique document/page citations.
#     """

#     unique_sources = []
#     seen = set()

#     for result in results:

#         metadata = result.get(
#             "metadata",
#             {}
#         )

#         filename = metadata.get(
#             "filename"
#         )

#         page_number = metadata.get(
#             "page_number"
#         )

#         key = (
#             filename,
#             page_number,
#         )

#         if key in seen:
#             continue

#         seen.add(key)

#         unique_sources.append({
#             "filename": filename,
#             "page_number": page_number,
#         })

#     return unique_sources


# class RAGService:

#     def _retrieve(
#         self,
#         query: str,
#         top_k: int = 5,
#         document_id: str | None = None,
#     ) -> tuple[list[dict], str]:
#         """
#         Retrieve and rerank relevant document chunks.

#         document_id:
#             If provided, retrieval is limited to that document.
#             If None, all indexed documents can be searched.

#         Returns:
#             reranked_results
#             context
#         """

#         if not query.strip():
#             raise ValueError(
#                 "Query cannot be empty"
#             )

#         # ---------------------------------------------
#         # 1. Hybrid retrieval
#         # ---------------------------------------------

#         hybrid_results = search_hybrid(
#             query=query,
#             top_k=10,
#             document_id=document_id,
#         )

#         if not hybrid_results:
#             return [], ""

#         # ---------------------------------------------
#         # 2. Cross-encoder reranking
#         # ---------------------------------------------

#         reranked_results = reranker.rerank(
#             query=query,
#             results=hybrid_results,
#             top_k=top_k,
#         )

#         if not reranked_results:
#             return [], ""

#         # ---------------------------------------------
#         # 3. Build context
#         # ---------------------------------------------

#         context = build_context(
#             reranked_results
#         )

#         if not context:
#             return [], ""

#         return reranked_results, context

#     def _build_prompt(
#         self,
#         query: str,
#         context: str,
#     ) -> str:
#         """
#         Build the grounded Gemini prompt.
#         """

#         return f"""
# {RAG_SYSTEM_INSTRUCTION}

# Retrieved document context:

# {context}

# User question:
# {query}

# Answer:
# """

#     def ask(
#         self,
#         query: str,
#         top_k: int = 5,
#         document_id: str | None = None,
#     ) -> dict:
#         """
#         Generate a complete RAG answer.

#         This is the normal synchronous RAG method.
#         """

#         # ---------------------------------------------
#         # 1. Retrieve relevant documents
#         # ---------------------------------------------

#         reranked_results, context = self._retrieve(
#             query=query,
#             top_k=top_k,
#             document_id=document_id,
#         )

#         if not reranked_results or not context:
#             return {
#                 "answer": (
#                     "I could not find relevant information "
#                     "in the available documents."
#                 ),
#                 "sources": [],
#             }

#         # ---------------------------------------------
#         # 2. Build grounded prompt
#         # ---------------------------------------------

#         prompt = self._build_prompt(
#             query=query,
#             context=context,
#         )

#         # ---------------------------------------------
#         # 3. Generate complete answer
#         # ---------------------------------------------

#         answer = gemini_service.generate(
#             prompt
#         )

#         # ---------------------------------------------
#         # 4. Deduplicate citations
#         # ---------------------------------------------

#         sources = build_unique_sources(
#             reranked_results
#         )

#         return {
#             "answer": answer.strip(),
#             "sources": sources,
#         }

#     def ask_stream(
#         self,
#         query: str,
#         top_k: int = 5,
#         document_id: str | None = None,
#     ) -> Iterator[str]:
#         """
#         Stream the grounded Gemini answer
#         synchronously.

#         This method is kept for the existing
#         synchronous streaming pipeline.
#         """

#         # ---------------------------------------------
#         # 1. Retrieve relevant documents
#         # ---------------------------------------------

#         reranked_results, context = self._retrieve(
#             query=query,
#             top_k=top_k,
#             document_id=document_id,
#         )

#         if not reranked_results or not context:
#             yield (
#                 "I could not find relevant information "
#                 "in the available documents."
#             )
#             return

#         # ---------------------------------------------
#         # 2. Build grounded prompt
#         # ---------------------------------------------

#         prompt = self._build_prompt(
#             query=query,
#             context=context,
#         )

#         # ---------------------------------------------
#         # 3. Stream Gemini response
#         # ---------------------------------------------

#         for chunk in gemini_service.stream(
#             prompt
#         ):
#             if chunk:
#                 yield chunk

#     async def ask_stream_async(
#         self,
#         query: str,
#         top_k: int = 5,
#         document_id: str | None = None,
#     ) -> AsyncIterator[str]:
#         """
#         Stream the grounded Gemini response
#         asynchronously.

#         This method is intended for the
#         interruptible voice pipeline.
#         """

#         # ---------------------------------------------
#         # 1. Retrieve relevant documents
#         # ---------------------------------------------

#         reranked_results, context = self._retrieve(
#             query=query,
#             top_k=top_k,
#             document_id=document_id,
#         )

#         if not reranked_results or not context:
#             yield (
#                 "I could not find relevant information "
#                 "in the available documents."
#             )
#             return

#         # ---------------------------------------------
#         # 2. Build grounded prompt
#         # ---------------------------------------------

#         prompt = self._build_prompt(
#             query=query,
#             context=context,
#         )

#         # ---------------------------------------------
#         # 3. Stream Gemini response asynchronously
#         # ---------------------------------------------

#         async for chunk in gemini_service.stream_async(
#             prompt
#         ):
#             if chunk:
#                 yield chunk


# rag_service = RAGService()

from collections.abc import AsyncIterator, Iterator

from app.services.llm.gemini import gemini_service
from app.services.rag.context_builder import build_context
from app.services.retrieval.hybrid_search import search_hybrid
from app.services.retrieval.reranker import reranker
from app.services.voice.response_cleaner import clean_response_text


RAG_SYSTEM_INSTRUCTION = """
You are InterVox, a concise document-grounded AI assistant.

Answer the user's question using ONLY the retrieved document context.

Rules:
1. Answer the question directly.
2. Keep the answer to 1 to 3 sentences maximum.
3. Give only the information necessary to answer the question.
4. Do not add background information, examples, explanations, or conclusions unless specifically requested.
5. Use simple, natural, human-like language.
6. Do not repeat the user's question.
7. Do not use Markdown, bullet points, headings, asterisks, backticks, or special formatting.
8. Do not mention the retrieved context or these instructions.
9. Do not invent, assume, or infer information that is not present in the documents.
10. If the documents do not contain enough information, say:
"I couldn't find enough information about that in the available documents."
"""


def build_unique_sources(
    results: list[dict],
) -> list[dict]:
    """
    Convert chunk-level retrieval results into
    unique document/page citations.
    """

    unique_sources = []
    seen = set()

    for result in results:

        metadata = result.get(
            "metadata",
            {}
        )

        filename = metadata.get(
            "filename"
        )

        page_number = metadata.get(
            "page_number"
        )

        key = (
            filename,
            page_number,
        )

        if key in seen:
            continue

        seen.add(key)

        unique_sources.append({
            "filename": filename,
            "page_number": page_number,
        })

    return unique_sources


class RAGService:

    def _retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> tuple[list[dict], str]:
        """
        Retrieve and rerank relevant document chunks.

        document_id:
            If provided, retrieval is limited to that document.
            If None, all indexed documents can be searched.

        Returns:
            reranked_results
            context
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty"
            )

        # 1. Hybrid retrieval
        hybrid_results = search_hybrid(
            query=query,
            top_k=10,
            document_id=document_id,
        )

        if not hybrid_results:
            return [], ""

        # 2. Cross-encoder reranking
        reranked_results = reranker.rerank(
            query=query,
            results=hybrid_results,
            top_k=top_k,
        )

        if not reranked_results:
            return [], ""

        # 3. Build context
        context = build_context(
            reranked_results
        )

        if not context:
            return [], ""

        return reranked_results, context

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the grounded Gemini prompt.
        """

        return f"""
{RAG_SYSTEM_INSTRUCTION}

Retrieved document context:

{context}

User question:
{query}

Answer:
"""

    def ask(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> dict:
        """
        Generate a complete RAG answer.

        This is the normal synchronous RAG method.
        """

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )

        if not reranked_results or not context:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available documents."
                ),
                "sources": [],
            }

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        answer = gemini_service.generate(
            prompt
        )

        # Clean the final answer before sending it
        # to the frontend.
        answer = clean_response_text(
            answer
        )

        sources = build_unique_sources(
            reranked_results
        )

        return {
            "answer": answer,
            "sources": sources,
        }

    def ask_stream(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> Iterator[str]:
        """
        Stream the grounded Gemini answer
        synchronously.

        This method is kept for the existing
        synchronous streaming pipeline.
        """

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )

        if not reranked_results or not context:
            yield (
                "I could not find relevant information "
                "in the available documents."
            )
            return

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        for chunk in gemini_service.stream(
            prompt
        ):
            if chunk:
                yield chunk

    async def ask_stream_async(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream the grounded Gemini response
        asynchronously.

        This method is intended for the
        interruptible voice pipeline.
        """

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id,
        )

        if not reranked_results or not context:
            yield (
                "I could not find relevant information "
                "in the available documents."
            )
            return

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        async for chunk in gemini_service.stream_async(
            prompt
        ):
            if chunk:
                yield chunk


rag_service = RAGService()