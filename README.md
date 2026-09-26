# 🎙️ InterVox — AI Research Assistant

> **A voice-first AI Research Assistant that lets users have natural, real-time conversations with their own documents.**

InterVox is a **RAG-powered AI Research Assistant** designed to make document-based information retrieval more natural through **real-time voice interaction**.

Users can upload documents, ask questions using their voice, and receive AI-generated answers based on the information contained in their uploaded files.

The key feature of InterVox is **real-time voice interruption (barge-in)** — users can interrupt the AI while it is speaking, causing the current response to stop and allowing the assistant to immediately process the new request.

---

##  Key Features

* 📄 **Document Upload** — Upload research papers, PDFs, resumes, notes, and other supported documents.
* 🔍 **RAG-based Question Answering** — Retrieves relevant document context before generating an answer.
* 🧠 **Semantic Search** — Finds relevant information based on meaning rather than simple keyword matching.
* 🎙️ **Voice-first Interaction** — Ask questions naturally using your microphone.
* 🔊 **Real-time Voice Responses** — AI responses are converted into speech for a conversational experience.
* ⚡ **Low-latency Response Pipeline** — Designed around streaming and fast time-to-first-response.
* 🛑 **Voice Interruption / Barge-in** — Interrupt the assistant while it is speaking and immediately start a new request.
* 🔄 **Turn Management** — Prevents stale or interrupted AI responses from continuing after a new user request.
* 📚 **Document-grounded Answers** — Responses are generated using information retrieved from the user's uploaded documents.

---

##  System Architecture

```text
                         ┌─────────────────────┐
                         │       Frontend      │
                         │                     │
                         │  Voice / Documents  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             ┌──────────────┐               ┌──────────────┐
             │   Document   │               │ Voice Input  │
             │   Pipeline   │               │   Pipeline   │
             └──────┬───────┘               └──────┬───────┘
                    │                               │
                    ▼                               ▼
             ┌──────────────┐               ┌──────────────┐
             │ Text         │               │ Speech-to-   │
             │ Extraction   │               │ Text (STT)   │
             └──────┬───────┘               └──────┬───────┘
                    │                               │
                    ▼                               ▼
             ┌──────────────┐               ┌──────────────┐
             │ Chunking &   │               │ User Query   │
             │ Embeddings   │               └──────┬───────┘
             └──────┬───────┘                      │
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │   Semantic Retrieval│
                         │   / Vector Search   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        LLM          │
                         │ Context + Question  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      TTS / Audio    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Voice Response    │
                         │  + Barge-in Control │
                         └─────────────────────┘
```

---

##  How It Works

### 1. Upload Documents

The user uploads a supported document through the application.

```text
Document
   ↓
Validation
   ↓
Text Extraction
   ↓
Text Chunking
   ↓
Embeddings
   ↓
Vector Store
```

### 2. Ask a Question

The user can ask a question through voice.

```text
User Speech
     ↓
Voice Activity Detection
     ↓
Speech-to-Text
     ↓
User Query
```

### 3. Retrieve Relevant Context

The query is converted into an embedding and used to find the most relevant document chunks.

```text
User Query
     ↓
Embedding
     ↓
Semantic Search
     ↓
Relevant Document Chunks
```

### 4. Generate the Answer

The retrieved context is provided to the LLM along with the user's question.

```text
Question + Retrieved Context
             ↓
            LLM
             ↓
       Generated Answer
```

### 5. Convert Answer to Voice

The generated response is converted into speech and streamed back to the user.

```text
LLM Response
     ↓
Text-to-Speech
     ↓
Audio Stream
     ↓
User
```

---

##  Voice Interruption / Barge-in

The most important differentiating feature of InterVox is its **barge-in mechanism**.

Traditional voice assistants may continue speaking even when the user starts talking. InterVox is designed to behave more naturally.

When the user interrupts:

```text
AI is speaking
      ↓
User starts speaking
      ↓
Barge-in detected
      ↓
Stop TTS playback
      ↓
Cancel current AI turn
      ↓
Discard stale response
      ↓
Process new user request
```

Each conversation turn is associated with a **turn ID**, allowing the system to identify and discard responses belonging to previous interrupted turns.

This helps prevent problems such as:

* Old responses continuing after an interruption
* Audio from multiple responses playing simultaneously
* Stale LLM results being displayed
* Unnecessary processing after the user changes the question

---

##  RAG Pipeline

InterVox follows a Retrieval-Augmented Generation architecture:

```text
             ┌──────────────┐
             │ User Document│
             └──────┬───────┘
                    ↓
             Text Extraction
                    ↓
                Chunking
                    ↓
               Embeddings
                    ↓
              Vector Store
                    │
                    │
User Question ──────┤
                    ↓
             Semantic Search
                    ↓
          Relevant Context
                    ↓
                   LLM
                    ↓
             Final Response
```

Instead of relying only on the model's pre-trained knowledge, InterVox retrieves relevant information from the user's documents before generating an answer.

---

##  Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Pydantic / Pydantic Settings**
* **PyMuPDF** for PDF text extraction
* **uv** for Python environment and dependency management

### AI / RAG

* Retrieval-Augmented Generation (RAG)
* Text chunking
* Embeddings
* Semantic search
* Vector database / vector store
* Large Language Model (LLM)

### Voice

* Voice Activity Detection (VAD)
* Speech-to-Text (STT)
* Text-to-Speech (TTS)
* Streaming audio
* Voice interruption / barge-in
* Turn cancellation

### Frontend

* React
* Vite
* Browser microphone/audio APIs

---

## Project Structure

```text
InterVox/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── uploads/
│   ├── pyproject.toml
│   └── ...
│
├── frontend/
│   └── ...
│
├── .gitignore
└── README.md
```

> Project structure will evolve as additional RAG and real-time voice modules are implemented.

---

##  Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.11+
* Node.js
* Git
* `uv`

### Clone the Repository

```bash
git clone https://github.com/<your-username>/InterVox.git
cd InterVox
```

### Backend Setup

```bash
cd backend
```

Create/sync the project environment:

```bash
uv sync
```

Run the development server:

```bash
uv run fastapi dev app/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

##  Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
APP_NAME=InterVox
APP_ENV=development

# Add required AI / database / voice service keys here
```

> Never commit API keys or secrets to GitHub.

---

##  Current Development Status

InterVox is actively under development.

### Completed

* [x] FastAPI backend setup
* [x] Application configuration
* [x] Document upload API
* [x] Uploaded document metadata model
* [x] PDF text extraction
* [x] Basic backend API documentation

### In Progress

* [ ] Document chunking
* [ ] Embedding generation
* [ ] Vector database integration
* [ ] Semantic retrieval
* [ ] RAG pipeline
* [ ] LLM integration
* [ ] Speech-to-text pipeline
* [ ] Text-to-speech streaming
* [ ] Voice Activity Detection
* [ ] Barge-in / interruption handling
* [ ] Turn cancellation
* [ ] Real-time frontend voice interface

---

##  Project Goals

InterVox is being developed with a focus on:

* **Low-latency voice interaction**
* **Reliable document-grounded answers**
* **Streaming AI responses**
* **Natural conversational behavior**
* **Robust interruption handling**
* **Scalable backend architecture**
* **Clean separation between document, retrieval, AI, and voice pipelines**

---

##  Future Improvements

* Support for additional document formats
* Conversation history and session management
* Multi-document research
* Source/citation references for generated answers
* Improved streaming architecture
* Advanced retrieval and reranking
* Conversation memory
* User authentication
* Cloud deployment
* Performance monitoring and latency metrics
* Evaluation pipeline for RAG answer quality

---

##  Why InterVox?

Most document-based AI applications focus primarily on text-based question answering.

InterVox explores a different interaction model:

> **Upload your knowledge → Ask naturally → Get a grounded answer → Interrupt whenever you want.**

The project combines **RAG, LLMs, speech processing, streaming systems, and real-time interaction** into a single application.

---

##  Learning & Engineering Focus

This project is being built to explore practical concepts in:

* Retrieval-Augmented Generation
* Large Language Models
* Vector Search
* Embeddings
* Natural Language Processing
* Speech Recognition
* Text-to-Speech
* Real-time streaming
* Async backend systems
* API design
* AI application architecture
* Concurrency and cancellation
* Latency optimization

---

##  Author

**Rishika Rajput**

B.Tech Student | AI/ML & Full-Stack Development

---

##  Support

If you find this project interesting, consider giving the repository a ⭐.

Feedback, suggestions, and contributions are welcome.

