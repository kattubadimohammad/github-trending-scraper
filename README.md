# GitHub Trending Scraper and Analyzer

This FastAPI application fetches trending repositories from GitHub for a specified programming language and analyzes the relationships between them based on shared topics. The output is a JSON format suitable for graph visualization.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your_repository_url>
    cd github-trending-scraper
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate   # On Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Navigate to the project root directory.
2.  Run the FastAPI application using Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

    This will start the server, usually at `http://127.0.0.1:8000`.

## API Endpoint

`/analyze/github/trending/{language}`

* **Method:** `GET`
* **Path Parameter:** `{language}` - The programming language for which to fetch trending repositories (e.g., `python`, `javascript`, `java`).

## Example Usage

To analyze trending Python repositories, you can access the following URL in your browser or using a tool like `curl`:
