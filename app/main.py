from fastapi import FastAPI, HTTPException
from app.scraper import fetch_trending_repos, compute_edges
from app.models import GraphData
from app.cache import get_cache, set_cache
from app.utils import compute_semantic_similarity
from time import time

app = FastAPI()

@app.get("/analyze/github/trending/{language}", response_model=GraphData)
def analyze_trending(language: str):
    """
    API endpoint to analyze GitHub trending repositories for a given language.
    It scrapes the GitHub trending page and returns a graph-like JSON format.
    """
    key = f"trending_{language}"
    
    # Check if the result is cached
    cache_data = get_cache(key)
    if cache_data:
        return cache_data

    # Fetch data from GitHub
    repos = fetch_trending_repos(language)
    nodes = [{"id": repo["id"], "description": repo["description"], "stars": repo["stars"], "forks": repo["forks"], "language": repo["language"]} for repo in repos]

    # Compute edges based on shared topics and semantic similarity
    edges = compute_edges(repos)

    # Create a graph-like structure
    result = GraphData(nodes=nodes, edges=edges)

    # Cache the result
    set_cache(key, result)
    
    return result

