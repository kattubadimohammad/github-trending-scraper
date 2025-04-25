from fastapi import FastAPI, HTTPException
from app.scraper import fetch_trending_repos, compute_edges
from app.models import GraphData
from app.cache import get_cache, set_cache
from app.utils import compute_semantic_similarity
from time import time
from typing import List

app = FastAPI()

@app.get("/analyze/github/trending/{language}", response_model=GraphData)
def analyze_trending(language: str):
    """
    API endpoint to analyze GitHub trending repositories for a given language.
    It scrapes the GitHub trending page and returns a graph-like JSON format.
    """
    # Construct the cache key based on the language
    key = f"trending_{language}"
    
    # Check if the result is cached
    cache_data = get_cache(key)
    if cache_data:
        return cache_data
    
    try:
        # Fetch data from GitHub
        repos = fetch_trending_repos(language)
        
        if not repos:
            raise HTTPException(status_code=404, detail=f"No trending repositories found for language: {language}")

        # Create nodes from the fetched repositories
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

        # Compute edges based on shared topics and semantic similarity
        edges = compute_edges(repos)

        # Create a graph-like structure (nodes and edges)
        result = GraphData(nodes=nodes, edges=edges)

        # Cache the result for faster subsequent requests
        set_cache(key, result)
        
        return result
    
    except Exception as e:
        # Handle any errors that might occur during the fetching or processing of data
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching data: {str(e)}")
