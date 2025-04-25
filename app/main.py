from fastapi import FastAPI, HTTPException
from app.scraper import fetch_trending_repos, compute_edges
from app.models import GraphData
from app.cache import get_cache, set_cache
from app.utils import compute_semantic_similarity
import logging  # Add logging for better debugging
from time import time
from typing import List

app = FastAPI()

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Root route (to avoid 404 error)
@app.get("/")
def read_root():
    return {"message": "Welcome to the GitHub Trending Scraper API"}

# Health check route
@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.get("/analyze/github/trending/{language}", response_model=GraphData)
def analyze_trending(language: str):
    """
    API endpoint to analyze GitHub trending repositories for a given language.
    It scrapes the GitHub trending page and returns a graph-like JSON format.
    """
    # Construct the cache key based on the language
    key = f"trending_{language}"

    # Clear cache (for testing purposes) - You can remove this later
    set_cache(key, None)

    # Check if the result is cached
    cache_data = get_cache(key)
    if cache_data:
        logging.info(f"Cache hit for language: {language}")
        return cache_data

    try:
        logging.info(f"Fetching trending repositories for {language}...")
        repos = fetch_trending_repos(language)

        if not repos:
            logging.warning(f"No repositories found for {language}")
            raise HTTPException(status_code=404, detail=f"No trending repositories found for language: {language}")

        # Process repos into nodes
        nodes = [
            {
                "id": repo["id"],
                "description": repo.get("description", "No description available"),
                "stars": repo["stars"],
                "forks": repo["forks"],
                "language": repo["language"]
            }
            for repo in repos
        ]

        # Compute the edges (similarity between repositories)
        edges = compute_edges(repos)

        # Structure the result
        result = GraphData(nodes=nodes, edges=edges)

        logging.info(f"Caching result for {language}")
        set_cache(key, result)

        return result

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
