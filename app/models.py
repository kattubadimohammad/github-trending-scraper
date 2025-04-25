from pydantic import BaseModel
from typing import List, Optional

class RepositoryNode(BaseModel):
    id: str
    description: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    language: Optional[str] = None

class Edge(BaseModel):
    source: str
    target: str
    weight: int

class GraphData(BaseModel):
    nodes: List[RepositoryNode]
    edges: List[Edge]
