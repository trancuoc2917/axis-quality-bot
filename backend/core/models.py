from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TrajectoryCheckRequest(BaseModel):
    trajectory: Any          # ← Cho phép bất kỳ kiểu nào (list, dict, string...)
    filename: str = "web_input.txt"
    mode: str = "full"

class QualityResponse(BaseModel):
    score: float
    issues: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    timestamp: str