from app.services.tts.text_cleaner import (
    clean_text_for_tts,
)


def main():
    print("=" * 60)
    print("INTERVOX TTS TEXT CLEANER TEST")
    print("=" * 60)

    text = """
## Technologies

The project uses **MediaPipe** for pose tracking.

* **MediaPipe**
* **IDM-VTON**
* **OOTDiffusion**

You can read the `documentation` for more details.

[Project Repository](https://github.com/example/project)
"""

    print("\nORIGINAL TEXT:")
    print(text)

    cleaned = clean_text_for_tts(text)

    print("\nCLEANED TEXT:")
    print(cleaned)

    print("\n" + "=" * 60)
    print("TTS TEXT CLEANER TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()