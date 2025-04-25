from pydantic import BaseModel
from typing import List

class RepoNode(BaseModel):
    id: str
    description: str
    stars: int
    forks: int
    language: str

class RepoEdge(BaseModel):
    source: str
    target: str
    weight: int

class GraphData(BaseModel):
    nodes: List[RepoNode]
    edges: List[RepoEdge]
