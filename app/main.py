import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import time

app = FastAPI()

# Simple cache to store results for each language
cache = {}

# Helper function to fetch trending repositories
def fetch_trending_repositories(language: str):
    url = f'https://github.com/trending/{language}'
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch trending repositories.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    repos = []
    for repo_item in soup.find_all('article', class_='Box-row'):
        repo_name = repo_item.find('h1').get_text(strip=True)
        description = repo_item.find('p', class_='col-9 color-text-secondary my-1 pr-4')
        description = description.get_text(strip=True) if description else "No description"
        stars = repo_item.find('a', class_='Link--primary')
        stars = stars.get_text(strip=True).replace(',', '') if stars else '0'
        forks = repo_item.find('a', class_='Link--secondary')
        forks = forks.get_text(strip=True).replace(',', '') if forks else '0'
        
        # Additional logic to extract topics (if available)
        repo_url = f'https://github.com{repo_item.find("a", class_="Link--primary")["href"]}'
        repo_details = requests.get(repo_url)
        repo_soup = BeautifulSoup(repo_details.content, 'html.parser')
        topics = []
        for topic in repo_soup.find_all('span', class_='topic-tag'):
            topics.append(topic.get_text(strip=True))
        
        repos.append({
            "name": repo_name,
            "description": description,
            "stars": int(stars),
            "forks": int(forks),
            "topics": topics
        })
    return repos

# Helper function to perform similarity analysis
def analyze_relationships(repos: List[Dict]):
    edges = []
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            common_topics = set(repos[i]['topics']).intersection(repos[j]['topics'])
            if common_topics:
                edges.append({
                    "source": repos[i]['name'],
                    "target": repos[j]['name'],
                    "weight": len(common_topics)
                })
    return edges

# Data model for the response
class RepoNode(BaseModel):
    id: str
    description: str
    stars: int
    forks: int
    language: str

class GraphResponse(BaseModel):
    nodes: List[RepoNode]
    edges: List[Dict[str, str]]

@app.get("/analyze/github/trending/{language}", response_model=GraphResponse)
def analyze_trending(language: str):
    # Check cache first
    if language in cache and time.time() - cache[language]['timestamp'] < 3600:
        return cache[language]['data']

    # Fetch and process data
    repos = fetch_trending_repositories(language)
    nodes = [RepoNode(id=repo['name'], description=repo['description'], stars=repo['stars'], forks=repo['forks'], language=language) for repo in repos]
    edges = analyze_relationships(repos)
    
    result = GraphResponse(nodes=nodes, edges=edges)
    
    # Cache the result
    cache[language] = {
        "timestamp": time.time(),
        "data": result
    }
    
    return result
