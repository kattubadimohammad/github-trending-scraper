from fastapi import FastAPI, HTTPException
from app import models, scraper, utils, cache

# --- FastAPI Application ---
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/")  # Add this route
async def root():
    return {"message": "Welcome to the GitHub Trending Analyzer API"}

@app.get("/analyze/github/trending/{language}", response_model=models.GraphData)
async def analyze_trending_repositories(language: str):
    """
    Fetches trending GitHub repositories for a given language,
    analyzes their relationships based on shared topics, and
    returns the data in a graph-like JSON format.
    """
    try:
        cached_data = cache.get_cache().get(language)
        if cached_data:
            return cached_data

        html_content = scraper.fetch_trending_page(language)
        if not html_content:
            raise HTTPException(status_code=500, detail=f"Failed to fetch trending page for {language}")

        repositories_data = scraper.extract_repository_data(html_content)
        nodes = [
            models.RepositoryNode(
                id=repo["id"],
                description=repo.get("description"),
                stars=repo.get("stars"),
                forks=repo.get("forks"),
                language=repo.get("language"),
            )
            for repo in repositories_data
        ]
        edges = utils.analyze_repository_relationships(repositories_data)
        graph_data = models.GraphData(nodes=nodes, edges=edges)

        cache.get_cache()[language] = graph_data
        return graph_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error processing request for {language}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

