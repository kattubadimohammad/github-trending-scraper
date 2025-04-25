# GitHub Trending Scraper & Analyzer

A **FastAPI application** to fetch and analyze trending GitHub repositories based on a specified programming language. It scrapes repository details, identifies relationships based on shared topics, and outputs a structured JSON format ideal for graph-based visualizations.

## Developed By

**Mohammad Kattubadi**  
Email: miraclemohammad786@gmail.com  
GitHub: [kattubadimohammad](https://github.com/kattubadimohammad)  
Location: Bengaluru, Karnataka

---

## Features

- Fetches GitHub trending repositories by language
- Extracts metadata like stars, forks, and topics
- Builds a relationship graph using shared topics
- Returns structured data as JSON
- Modular design with unit tests
- Dockerized for ease of deployment

---

## Tech Stack

- Python 3.10+
- FastAPI
- Requests
- Uvicorn
- Pytest
- Docker

---

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/kattubadimohammad/github-trending-scraper.git
cd github-trending-scraper

Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate    # On Windows

Install Dependencies

pip install -r requirements.txt


---

Running the Application

Start the FastAPI server using Uvicorn:

uvicorn app.main:app --reload

Visit in your browser or via API tools at:
http://127.0.0.1:8000/analyze/github/trending/{language}

Example:

http://127.0.0.1:8000/analyze/github/trending/python


---

Project Structure

github-trending-scraper/
├── app/
│   ├── main.py
│   ├── scraper.py
│   ├── models.py
│   ├── cache.py
│   └── utils.py
├── tests/
│   ├── test_main.py
│   ├── test_scraper.py
│   └── test_utils.py
├── requirements.txt
├── Dockerfile
└── README.md


---

Run Tests

pytest tests/


---

Run via Docker

docker build -t github-trending-scraper .
docker run -p 8000:8000 github-trending-scraper


---

License

MIT License

---

Let me know if you'd like to include deployment links, a sample API response, or even a video demo link.

