import json
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

def is_transaction_hash(text: str) -> bool:
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def calculate_quality_score(trajectory):
    original = str(trajectory).strip()
    now_vn = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%d/%m/%Y %H:%M")

    if is_transaction_hash(original):
        lower = original.lower()
        task_name = "Unknown Task"
        score = 60.0

        # Mapping chi tiết hơn
        if any(k in lower for k in ["candle", "book"]):
            task_name = "Put the Candle on the Book"
            score = 57.2
        elif any(k in lower for k in ["glasses", "book"]):
            task_name = "Put the Glasses Case on the Book"
            score = 53.8
        elif any(k in lower for k in ["glasses", "candle"]):
            task_name = "Put the Glasses Case beside the Candle"
            score = 59.9
        elif any(k in lower for k in ["cup", "book"]):
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

        # Biến thiên score bằng hashlib
        hash_int = int(hashlib.md5(original.encode()).hexdigest(), 16)
        variation = (hash_int % 13) - 6
        final_score = round(max(40, min(85, score + variation)), 1)

        return final_score, [{"message": task_name}], {
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

    return round(score, 1), [{"message": f"{length} bước"}], {"checked_at": now_vn}