
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


# class RAGService:

#     def ask(
#         self,
#         query: str,
#         top_k: int = 5,
#     ) -> dict:

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
#             return {
#                 "answer": (
#                     "I could not find relevant information "
#                     "in the available documents."
#                 ),
#                 "sources": [],
#             }

#         # ---------------------------------------------
#         # 2. Cross-encoder reranking
#         # ---------------------------------------------

#         reranked_results = reranker.rerank(
#             query=query,
#             results=hybrid_results,
#             top_k=top_k,
#         )

#         if not reranked_results:
#             return {
#                 "answer": (
#                     "I could not find relevant information "
#                     "in the available documents."
#                 ),
#                 "sources": [],
#             }

#         # ---------------------------------------------
#         # 3. Build context
#         # ---------------------------------------------

#         context = build_context(
#             reranked_results
#         )

#         # ---------------------------------------------
#         # 4. Build grounded prompt
#         # ---------------------------------------------

#         prompt = f"""
# {RAG_SYSTEM_INSTRUCTION}

# Retrieved document context:

# {context}

# User question:
# {query}

# Answer:
# """

#         # ---------------------------------------------
#         # 5. Generate answer
#         # ---------------------------------------------

#         answer = gemini_service.generate(
#             prompt
#         )

#         # ---------------------------------------------
#         # 6. Prepare sources
#         # ---------------------------------------------

#         sources = []

#         for result in reranked_results:

#             metadata = result.get(
#                 "metadata",
#                 {}
#             )

#             sources.append({
#                 "filename": metadata.get(
#                     "filename"
#                 ),
#                 "page_number": metadata.get(
#                     "page_number"
#                 ),
#                 "chunk_id": result.get(
#                     "chunk_id"
#                 ),
#                 "rerank_score": result.get(
#                     "rerank_score"
#                 ),
#             })

#         return {
#             "answer": answer.strip(),
#             "sources": sources,
#         }


# rag_service = RAGService()

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

    def ask(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:

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
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------
        # 2. Cross-encoder reranking
        # ---------------------------------------------

        reranked_results = reranker.rerank(
            query=query,
            results=hybrid_results,
            top_k=top_k,
        )

        if not reranked_results:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------
        # 3. Build context
        # ---------------------------------------------

        context = build_context(
            reranked_results
        )

        if not context:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------
        # 4. Build grounded prompt
        # ---------------------------------------------

        prompt = f"""
{RAG_SYSTEM_INSTRUCTION}

Retrieved document context:

{context}

User question:
{query}

Answer:
"""

        # ---------------------------------------------
        # 5. Generate answer
        # ---------------------------------------------

        answer = gemini_service.generate(
            prompt
        )

        # ---------------------------------------------
        # 6. Deduplicate citations
        # ---------------------------------------------

        sources = build_unique_sources(
            reranked_results
        )

        return {
            "answer": answer.strip(),
            "sources": sources,
        }


rag_service = RAGService()