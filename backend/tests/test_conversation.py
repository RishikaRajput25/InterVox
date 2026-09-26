from app.services.conversation.models import Conversation
from app.services.conversation.query_rewriter import query_rewriter


def main():

    conversation = Conversation(
        conversation_id="conversation-001",
        turns=[],
    )

    # ---------------------------------------------
    # Turn 1
    # ---------------------------------------------

    conversation.add_turn(
        turn_id="turn-001",
        user_message="What is StyleMirror?",
        assistant_message=(
            "StyleMirror is an AI-powered "
            "virtual fashion assistant."
        ),
    )

    # ---------------------------------------------
    # Turn 2
    # ---------------------------------------------

    latest_query = (
        "What technologies does it use?"
    )

    rewritten_query = query_rewriter.rewrite(
        conversation=conversation,
        latest_query=latest_query,
    )

    print("Original query:")
    print(latest_query)

    print("\nRewritten query:")
    print(rewritten_query)


if __name__ == "__main__":
    main()