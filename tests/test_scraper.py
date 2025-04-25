from app.scraper import fetch_trending_repos

def test_fetch_trending_repos():
    repos = fetch_trending_repos("python")
    assert isinstance(repos, list)
    assert len(repos) > 0
    assert all("id" in repo for repo in repos)
    assert all("stars" in repo for repo in repos)
    assert all("forks" in repo for repo in repos)
