import json
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, List, Dict

def is_transaction_hash(text: str) -> bool:
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def calculate_quality_score(trajectory: Any, mode: str = "full"):
    original = str(trajectory).strip()
    now_vn = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%d/%m/%Y %H:%M:%S")

    if is_transaction_hash(original):
        lower = original.lower()
        task_name = "Unknown Task"
        score = 62.0

        # Tăng khả năng nhận task
        if any(x in lower for x in ["candle", "book"]):
            task_name = "Put the Candle on the Book"
            score = 57.2
        elif any(x in lower for x in ["glasses", "book"]):
            task_name = "Put the Glasses Case on the Book"
            score = 53.8
        elif any(x in lower for x in ["glasses", "candle"]):
            task_name = "Put the Glasses Case beside the Candle"
            score = 59.9
        elif any(x in lower for x in ["cup", "book"]):
            task_name = "Put the Cup on the Book"
            score = 72.7
        elif "rotate" in lower and "cup" in lower:
            task_name = "Rotate the Cup"
            score = 77.9
        elif "rotate" in lower and "glasses" in lower:
            task_name = "Rotate the Glasses Case"
            score = 72.2
        elif "bracelet" in lower and "plate" in lower:
            task_name = "Put the Bracelet on the Plate"
            score = 73.1
        elif "diamond" in lower and "plate" in lower:
            task_name = "Put the Diamond on the Plate"
            score = 69.6
        elif "ring" in lower:
            task_name = "Ring / Bracelet Task"
            score = 65.0

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
    score = 85 if length >= 5 else 60

    return round(score, 1), [{"message": f"{length} bước", "type": "info"}], {
        "length": length,
        "checked_at": now_vn
    }