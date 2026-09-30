from app.services.voice.voice_input import voice_input_service
from app.services.rag.rag_service import rag_service


AUDIO_PATH = (
    r"C:\Users\ayush\Downloads\WhatsApp Audio 2026-09-25 at 10.08.20 PM.mp4"
)


def main():
    print("=" * 60)
    print("INTERVOX VOICE → RAG INTEGRATION TEST")
    print("=" * 60)

    # -------------------------------------------------
    # 1. Voice → Transcript
    # -------------------------------------------------

    print("\n[1] Processing voice input...")

    transcript = voice_input_service.process_audio(
        AUDIO_PATH
    )

    print(f"\nTranscript: {transcript}")

    if not transcript:
        print("\nNo speech detected.")
        return

    # -------------------------------------------------
    # 2. Transcript → RAG
    # -------------------------------------------------

    print("\n[2] Sending transcript to RAG...")

    result = rag_service.ask(
        query=transcript
    )

    # -------------------------------------------------
    # 3. Display answer
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("RAG ANSWER")
    print("=" * 60)

    print(f"\n{result['answer']}")

    # -------------------------------------------------
    # 4. Display sources
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result["sources"]:
        print(source)

    print("\n" + "=" * 60)
    print("VOICE → RAG TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()