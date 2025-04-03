from typing import List
from pydantic import BaseModel

class Node(BaseModel):
    node_id: str
    name: str
    severity: str
    children: List['Node'] = []