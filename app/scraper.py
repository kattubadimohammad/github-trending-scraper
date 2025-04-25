import requests
from bs4 import BeautifulSoup
from time import sleep

# GitHub headers to avoid getting blocked
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_trending_repos(language: str):
    """
    Fetches trending repositories for a specific language from GitHub.
    """
    url = f"https://github.com/trending/{language.lower()}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch GitHub trending page for {language}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    repo_items = soup.find_all("article", class_="Box-row")
    repos = []

    for item in repo_items:
        try:
            # Extract repository details
            full_name = item.h2.a.get("href").strip("/")
            description = item.find("p").text.strip() if item.find("p") else ""
            stars = int(item.find("a", href=lambda href: href and href.endswith("/stargazers")).text.strip().replace(",", ""))
            forks = int(item.find("a", href=lambda href: href and "/network/members" in href).text.strip().replace(",", ""))
            repos.append({
                "id": full_name,
                "description": description,
                "stars": stars,
                "forks": forks,
                "language": language
            })
            sleep(1)  # Rate limiting to avoid GitHub blocking requests
        except Exception as e:
            continue

    return repos

def compute_edges(repos):
    """
    Compute edges based on shared topics between repositories.
    """
    edges = []
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            shared_topics = set(repos[i].get('topics', [])) & set(repos[j].get('topics', []))
            weight = len(shared_topics)
            if weight > 0:
                edges.append({
                    "source": repos[i]["id"],
                    "target": repos[j]["id"],
                    "weight": weight
                })
    return edges
