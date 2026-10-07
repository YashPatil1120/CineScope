from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    metadata: dict | None = None


class GraphLink(BaseModel):
    source: str
    target: str
    relationship: str
    metadata: dict | None = None


class MovieGraphResponse(BaseModel):
    movie_id: int
    movie_title: str
    nodes: list[GraphNode]
    links: list[GraphLink]