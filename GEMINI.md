# GEMINI.md

## Project Overview

This is a full-stack Retrieval-Augmented Generation (RAG) web application. Its purpose is to answer questions about course materials. The application is built with a Python backend and a simple HTML/CSS/JavaScript frontend.

**Backend:**
*   **Framework:** FastAPI
*   **Core Logic:** The `RAGSystem` class in `backend/rag_system.py` orchestrates the RAG pipeline.
*   **AI/ML:**
    *   **AI Generation:** Uses Google's Gemini model (specifically `gemini-1.5-pro-latest`) via the `google-generativeai` library.
    *   **Embeddings:** Uses the `all-MiniLM-L6-v2` model from `sentence-transformers` to create text embeddings.
    *   **Vector Store:** ChromaDB is used for storing and retrieving vector embeddings.
*   **APIs:**
    *   `POST /api/query`: The main endpoint for asking questions.
    *   `GET /api/courses`: Retrieves statistics about the loaded courses.
*   **Data:** The application processes `.txt`, `.pdf`, and `.docx` files from the `docs/` directory.

**Frontend:**
*   A single-page application built with vanilla HTML, CSS, and JavaScript.
*   Provides a chat interface for interacting with the backend.
*   Displays course statistics and suggested questions.
*   Uses the `marked.js` library to render Markdown responses from the AI.

## Building and Running

1.  **Prerequisites:**
    *   Python 3.13+
    *   `uv` package manager
    *   A Google API key

2.  **Installation:**
    *   Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    *   Install dependencies: `uv sync`

3.  **Environment Setup:**
    *   Create a `.env` file in the root directory.
    *   Add your Google API key to the `.env` file:
        ```
        GEMINI_API_KEY=your_gemini_api_key_here
        ```

4.  **Running the Application:**
    *   The easiest way to run the application is to use the provided shell script:
        ```bash
        chmod +x run.sh
        ./run.sh
        ```
    *   Alternatively, you can run the backend server manually:
        ```bash
        cd backend
        uv run uvicorn app:app --reload --port 8000
        ```
    *   The web interface will be available at `http://localhost:8000`.

## Development Conventions

*   **Configuration:** The application's configuration is centralized in the `backend/config.py` file. This is the best place to adjust settings like the AI model, chunk size, and database path.
*   **Dependencies:** Python dependencies are managed with `uv` and are listed in the `pyproject.toml` file.
*   **Modular Structure:** The backend code is organized into modules with clear responsibilities (e.g., `document_processor.py`, `vector_store.py`, `ai_generator.py`).
*   **Frontend Logic:** All frontend JavaScript is contained in `frontend/script.js`.
*   **Styling:** All frontend styles are in `frontend/style.css`.
