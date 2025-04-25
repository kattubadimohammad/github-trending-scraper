from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from models.graph import GraphData, RepositoryNode, Edge
from utils.scraping import fetch_trending_page, extract_repository_data
from utils.data_processing import analyze_repository_relationships
from cachetools import TTLCache

# --- Configuration ---
CACHE_TTL = 3600  # seconds (1 hour)
cache = TTLCache(maxsize=128, ttl=CACHE_TTL)

# --- FastAPI Application ---
app = FastAPI()

@app.get("/analyze/github/trending/{language}", response_model=GraphData)
async def analyze_trending_repositories(language: str):
    """
    Fetches trending GitHub repositories for a given language,
    analyzes their relationships based on shared topics, and
    returns the data in a graph-like JSON format.
    """
    cached_data = cache.get(language)
    if cached_data:
        return cached_data

    html_content = fetch_trending_page(language)
    if not html_content:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trending page for {language}")

    repositories_data = extract_repository_data(html_content)
    nodes = [
        RepositoryNode(
            id=repo["id"],
            description=repo.get("description"),
            stars=repo.get("stars"),
            forks=repo.get("forks"),
            language=repo.get("language"),
        )
        for repo in repositories_data
    ]
    edges = analyze_repository_relationships(repositories_data)
    graph_data = GraphData(nodes=nodes, edges=edges)

    cache[language] = graph_data
    return graph_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
