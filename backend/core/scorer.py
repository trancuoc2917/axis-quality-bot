import json
from typing import Any, List, Dict

def is_transaction_hash(text: str) -> bool:
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def calculate_quality_score(trajectory: Any, mode: str = "full"):
    original_input = str(trajectory).strip()

    # === XỬ LÝ TRANSACTION HASH ===
    if is_transaction_hash(original_input):
        return 75.0, [
            {"message": "Đã nhận diện Transaction Hash", "type": "tx_detected"},
            {"message": "Hiện tại chưa fetch được dữ liệu chi tiết (API hạn chế)", "type": "tx_note"},
            {"message": "Score tạm tính dựa trên format hash hợp lệ", "type": "tx_format"}
        ], {
            "is_transaction": True,
            "hash": original_input,
            "mode": mode
        }

    # === XỬ LÝ JSON STRING ===
    if isinstance(trajectory, str):
        try:
            trajectory = json.loads(trajectory)
        except:
            pass

    if not trajectory:
        return 0.0, [{"message": "Trajectory rỗng hoặc không hợp lệ", "type": "empty"}], {}

    if isinstance(trajectory, dict):
        trajectory = [trajectory]

    length = len(trajectory)
    score = 100.0
    issues = []

    if length < 5:
        score -= 25
        issues.append({"message": f"Trajectory quá ngắn (chỉ {length} bước)", "type": "short"})

    score = max(0, min(100, round(score, 1)))

    metrics = {
        "length": length,
        "is_transaction": False,
        "mode": mode
    }

    return score, issues, metrics