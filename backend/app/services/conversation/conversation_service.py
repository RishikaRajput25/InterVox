from uuid import uuid4

from app.services.conversation.models import Conversation
from app.services.conversation.query_rewriter import query_rewriter
from app.services.rag.rag_service import rag_service


class ConversationService:

    def ask(
        self,
        conversation: Conversation,
        user_message: str,
    ) -> dict:

        if not user_message.strip():
            raise ValueError(
                "User message cannot be empty"
            )

        # Step 1: Rewrite the user's query
        # using previous conversation context.
        rewritten_query = query_rewriter.rewrite(
            conversation=conversation,
            latest_query=user_message,
        )

        # Step 2: Send rewritten query to RAG.
        rag_result = rag_service.ask(
            query=rewritten_query,
            top_k=5,
        )

        assistant_message = rag_result["answer"]

        # Step 3: Create a unique ID for this conversation turn.
        turn_id = str(uuid4())

        # Step 4: Save the conversation turn.
        conversation.add_turn(
            turn_id=turn_id,
            user_message=user_message,
            assistant_message=assistant_message,
        )

        # Step 5: Return everything useful to the caller.
        return {
            "turn_id": turn_id,
            "user_message": user_message,
            "rewritten_query": rewritten_query,
            "assistant_message": assistant_message,
            "sources": rag_result["sources"],
        }


conversation_service = ConversationService()