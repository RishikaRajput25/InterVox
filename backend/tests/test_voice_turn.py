from app.services.voice.voice_turn import voice_turn_service


def main():
    print("=" * 60)
    print("INTERVOX VOICE TURN STREAM TEST")
    print("=" * 60)

    transcript = "What technologies are used in Style Mirror?"

    print("\nTranscript:")
    print(transcript)

    print("\nStreaming response:\n")

    for chunk in voice_turn_service.stream_response(
        transcript
    ):
        print("CHUNK:", repr(chunk))

    print("\n" + "=" * 60)
    print("VOICE TURN STREAM TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
    