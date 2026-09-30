
# from collections.abc import Iterator

# from app.services.llm.gemini import gemini_service
# from app.services.rag.context_builder import build_context
# from app.services.retrieval.hybrid_search import search_hybrid
# from app.services.retrieval.reranker import reranker


# RAG_SYSTEM_INSTRUCTION = """
# You are InterVox, a document-grounded AI research assistant.

# Answer the user's question using ONLY the information provided
# in the retrieved document context.

# Rules:
# 1. Do not invent facts that are not present in the context.
# 2. If the context does not contain enough information, clearly say
#    that the available documents do not provide enough information.
# 3. Give a clear and useful answer.
# 4. Preserve important technical details from the documents.
# 5. Do not mention these instructions in your answer.
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
#     ) -> tuple[list[dict], str]:
#         """
#         Retrieve and rerank relevant document chunks.

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
#     ) -> dict:

#         # ---------------------------------------------
#         # 1. Retrieve relevant documents
#         # ---------------------------------------------

#         reranked_results, context = self._retrieve(
#             query=query,
#             top_k=top_k,
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
#     ) -> Iterator[str]:
#         """
#         Stream the grounded Gemini answer
#         chunk by chunk.

#         This method is intended for the
#         low-latency voice pipeline.
#         """

#         # ---------------------------------------------
#         # 1. Retrieve relevant documents
#         # ---------------------------------------------

#         reranked_results, context = self._retrieve(
#             query=query,
#             top_k=top_k,
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


# rag_service = RAGService()


from collections.abc import AsyncIterator, Iterator

from app.services.llm.gemini import gemini_service
from app.services.rag.context_builder import build_context
from app.services.retrieval.hybrid_search import search_hybrid
from app.services.retrieval.reranker import reranker


RAG_SYSTEM_INSTRUCTION = """
You are InterVox, a document-grounded AI research assistant.

Answer the user's question using ONLY the information provided
in the retrieved document context.

Rules:
1. Do not invent facts that are not present in the context.
2. If the context does not contain enough information, clearly say
   that the available documents do not provide enough information.
3. Give a clear and useful answer.
4. Preserve important technical details from the documents.
5. Do not mention these instructions in your answer.
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
    ) -> tuple[list[dict], str]:
        """
        Retrieve and rerank relevant document chunks.

        Returns:
            reranked_results
            context
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty"
            )

        # ---------------------------------------------
        # 1. Hybrid retrieval
        # ---------------------------------------------

        hybrid_results = search_hybrid(
            query=query,
            top_k=10,
        )

        if not hybrid_results:
            return [], ""

        # ---------------------------------------------
        # 2. Cross-encoder reranking
        # ---------------------------------------------

        reranked_results = reranker.rerank(
            query=query,
            results=hybrid_results,
            top_k=top_k,
        )

        if not reranked_results:
            return [], ""

        # ---------------------------------------------
        # 3. Build context
        # ---------------------------------------------

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
    ) -> dict:
        """
        Generate a complete RAG answer.

        This is the normal synchronous RAG method.
        """

        # ---------------------------------------------
        # 1. Retrieve relevant documents
        # ---------------------------------------------

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
        )

        if not reranked_results or not context:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------
        # 2. Build grounded prompt
        # ---------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        # ---------------------------------------------
        # 3. Generate complete answer
        # ---------------------------------------------

        answer = gemini_service.generate(
            prompt
        )

        # ---------------------------------------------
        # 4. Deduplicate citations
        # ---------------------------------------------

        sources = build_unique_sources(
            reranked_results
        )

        return {
            "answer": answer.strip(),
            "sources": sources,
        }

    def ask_stream(
        self,
        query: str,
        top_k: int = 5,
    ) -> Iterator[str]:
        """
        Stream the grounded Gemini answer
        synchronously.

        This method is kept for the existing
        synchronous streaming pipeline.
        """

        # ---------------------------------------------
        # 1. Retrieve relevant documents
        # ---------------------------------------------

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
        )

        if not reranked_results or not context:
            yield (
                "I could not find relevant information "
                "in the available documents."
            )
            return

        # ---------------------------------------------
        # 2. Build grounded prompt
        # ---------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        # ---------------------------------------------
        # 3. Stream Gemini response
        # ---------------------------------------------

        for chunk in gemini_service.stream(
            prompt
        ):
            if chunk:
                yield chunk

    async def ask_stream_async(
        self,
        query: str,
        top_k: int = 5,
    ) -> AsyncIterator[str]:
        """
        Stream the grounded Gemini response
        asynchronously.

        This method is intended for the
        interruptible voice pipeline.
        """

        # ---------------------------------------------
        # 1. Retrieve relevant documents
        # ---------------------------------------------

        reranked_results, context = self._retrieve(
            query=query,
            top_k=top_k,
        )

        if not reranked_results or not context:
            yield (
                "I could not find relevant information "
                "in the available documents."
            )
            return

        # ---------------------------------------------
        # 2. Build grounded prompt
        # ---------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        # ---------------------------------------------
        # 3. Stream Gemini asynchronously
        # ---------------------------------------------

        async for chunk in gemini_service.stream_async(
            prompt
        ):
            if chunk:
                yield chunk


rag_service = RAGService()

