import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional

GITHUB_TRENDING_BASE_URL = "https://github.com/trending"
REQUEST_DELAY = 0.5  # Reduced delay slightly

def fetch_trending_page(language: str) -> Optional[str]:
    """Fetches the GitHub trending page for a given language."""
    url = f"{GITHUB_TRENDING_BASE_URL}/{language}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending page for {language}: {e}")
        return None

def extract_repository_data(html_content: str) -> List[Dict]:
    """Extracts relevant repository information from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    repo_items = soup.find_all('article', class_='Box-row')
    repositories = []

    for item in repo_items:
        try:
            repo_info = {"id": None, "description": None, "stars": 0, "forks": 0, "language": None, "topics": []}

            # Repository Name
            header = item.find('h2', class_='h3 lh-condensed')
            if header and header.a:
                repo_name_parts = [part.strip() for part in header.a.text.split('/')]
                if len(repo_name_parts) == 2:
                    owner, repo = repo_name_parts
                    repo_info["id"] = f"{owner}/{repo}"
                else:
                    print(f"Unexpected repository name format: {header.a.text}")
                    continue  # Skip if the name format is unexpected
            else:
                print("Could not find repository header.")
                continue

            # Description
            description_element = item.find('p', class_='col-9 color-fg-muted my-1 pr-4')
            repo_info["description"] = description_element.text.strip() if description_element else None

            # Stars and Forks
            stats = item.find_all('a', class_='Link--muted')
            if len(stats) >= 2:
                stars_text = stats[0].text.strip()
                forks_text = stats[1].text.strip()
                repo_info["stars"] = parse_github_number(stars_text)
                repo_info["forks"] = parse_github_number(forks_text)
            else:
                print(f"Could not find stars/forks for {repo_info['id']}")

            # Language
            language_span = item.find('span', class_='d-inline-block ml-0 mr-2')
            repo_info["language"] = language_span.text.strip() if language_span else None

            # Topics
            topics_element = item.find('div', class_='f6 color-fg-muted mt-2')
            if topics_element:
                topics_links = topics_element.find_all('a', class_='topic-tag topic-tag-link')
                repo_info["topics"] = [topic.text.strip() for topic in topics_links]

            repositories.append(repo_info)
            time.sleep(REQUEST_DELAY) # Be respectful to GitHub
        except Exception as e:
            print(f"Error extracting data from a repository item: {e}")
            continue

    return repositories

def parse_github_number(text: str) -> int:
    """Parses GitHub's abbreviated number format (e.g., '1.2k')."""
    text = text.lower()
    multiplier = 1
    if 'k' in text:
        multiplier = 1000
        text = text.replace('k', '')
    elif 'm' in text:
        multiplier = 1000000
        text = text.replace('m', '')
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0
