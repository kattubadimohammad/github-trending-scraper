# GitHub Trending Scraper

A FastAPI application that fetches and analyzes trending GitHub repositories for a specified programming language. The application scrapes GitHub's trending page and provides a graph-like JSON output with repository details, such as description, stars, forks, and more.

## Features

- Fetches and analyzes trending repositories from GitHub for a given programming language.
- Provides a graph-like JSON output with repository details (id, description, stars, forks, language).
- Computes edges based on shared topics and semantic similarity between repositories.
- Caching mechanism to store results for faster responses.
- Built using FastAPI, Pydantic, and BeautifulSoup.

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/kattubadimohammad/github-trending-scraper.git
cd github-trending-scraper
