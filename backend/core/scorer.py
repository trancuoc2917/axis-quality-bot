import json
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, List, Dict

def is_transaction_hash(text: str) -> bool:
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def calculate_quality_score(trajectory: Any, mode: str = "full"):
    original = str(trajectory).strip()
    now_vn = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%d/%m/%Y %H:%M")

    if is_transaction_hash(original):
        lower = original.lower()
        task_name = "Unknown Task"
        score = 62.0

        if "candle" in lower and "book" in lower:
            task_name = "Put the Candle on the Book"
            score = 57.2
        elif "glasses" in lower and "book" in lower:
            task_name = "Put the Glasses Case on the Book"
            score = 53.8
        elif "cup" in lower and "book" in lower:
            task_name = "Put the Cup on the Book"
            score = 72.7
        elif "rotate" in lower:
            task_name = "Rotate Task"
            score = 76.0
        elif "bracelet" in lower:
            task_name = "Bracelet Task"
            score = 70.0
        elif "diamond" in lower:
            task_name = "Diamond Task"
            score = 65.0
        elif "ring" in lower:
            task_name = "Ring Task"
            score = 55.0

        return round(score, 1), [
            {"message": task_name, "type": "task"}
        ], {
            "is_transaction": True,
            "hash": original[:12] + "...",
            "task": task_name,
            "checked_at": now_vn
        }

    # JSON mode
    if isinstance(trajectory, str):
        try:
            trajectory = json.loads(trajectory)
        except:
            pass

    length = len(trajectory) if isinstance(trajectory, (list, dict)) else 1
    score = 88 if length >= 5 else 62

    return round(score, 1), [
        {"message": f"{length} bước", "type": "info"}
    ], {"checked_at": now_vn}