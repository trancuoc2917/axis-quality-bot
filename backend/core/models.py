from pydantic import BaseModel
from typing import List, Dict, Any

class TrajectoryCheckRequest(BaseModel):
    trajectory: List[Dict[str, Any]]
    mode: str = "normal"
    filename: str

class QualityResponse(BaseModel):
    score: float
    issues: List[str]
    metrics: Dict[str, Any]
    timestamp: str