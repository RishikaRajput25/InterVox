from app.services.conversation.models import Conversation
from app.services.conversation.conversation_service import conversation_service


def main():

    conversation = Conversation(
        conversation_id="test-conversation-001",
        turns=[],
    )

    print("\n" + "=" * 70)
    print("INTERVOX CONVERSATION + RAG TEST")
    print("=" * 70)

    # First question
    first_question = "What is StyleMirror?"

    print("\nUSER:")
    print(first_question)

    first_result = conversation_service.ask(
        conversation=conversation,
        user_message=first_question,
    )

    print("\nREWRITTEN QUERY:")
    print(first_result["rewritten_query"])

    print("\nASSISTANT:")
    print(first_result["assistant_message"])

    print("\nSOURCES:")

    for source in first_result["sources"]:
        print(
            f"- {source['filename']} "
            f"(Page {source['page_number']})"
        )

    # Follow-up question
    second_question = "What technologies does it use?"

    print("\n" + "-" * 70)

    print("\nUSER:")
    print(second_question)

    second_result = conversation_service.ask(
        conversation=conversation,
        user_message=second_question,
    )

    print("\nREWRITTEN QUERY:")
    print(second_result["rewritten_query"])

    print("\nASSISTANT:")
    print(second_result["assistant_message"])

    print("\nSOURCES:")

    for source in second_result["sources"]:
        print(
            f"- {source['filename']} "
            f"(Page {source['page_number']})"
        )

    print("\n" + "=" * 70)

    print("\nTOTAL CONVERSATION TURNS:")
    print(len(conversation.turns))


if __name__ == "__main__":
    main()