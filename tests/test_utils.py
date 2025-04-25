from app.utils import compute_semantic_similarity

def test_compute_semantic_similarity():
    similarity_score = compute_semantic_similarity("AI for healthcare", "Machine learning for health")
    assert 0 <= similarity_score <= 1
