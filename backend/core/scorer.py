import json
from typing import Any, List, Dict

def is_transaction_hash(text: str) -> bool:
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def calculate_quality_score(trajectory: Any, mode: str = "full"):
    original = str(trajectory).strip()

    # === TRANSACTION HASH MODE - TÍNH ĐỘNG ===
    if is_transaction_hash(original):
        # Tính điểm dựa trên độ phức tạp của hash
        hash_str = original[2:]  # bỏ 0x
        length_score = len(hash_str) / 64 * 30          # tối đa 30 điểm
        hex_score = sum(1 for c in hash_str if c in "abcdef") / 64 * 25   # tối đa 25 điểm
        variety_score = len(set(hash_str)) / 16 * 20     # tối đa 20 điểm

        base_score = 45 + length_score + hex_score + variety_score

        # Bonus theo một số pattern task Axis
        lower = hash_str.lower()
        bonus = 0
        task_name = "Generic Task"

        if any(x in lower for x in ["candle", "book", "put"]):
            bonus += 12
            task_name = "Put the Candle on the Book"
        elif any(x in lower for x in ["pick", "place", "move", "robot"]):
            bonus += 18
            task_name = "Pick & Place / Robot Task"
        elif any(x in lower for x in ["sign", "verify"]):
            bonus += 8
            task_name = "Sign / Verify Task"

        final_score = round(min(95, max(40, base_score + bonus)), 1)

        issues = [
            {"message": f"Đã nhận diện Transaction Hash - Task: {task_name}", "type": "tx_detected"},
            {"message": f"Điểm số được tính động dựa trên hash (độ phức tạp + pattern)", "type": "dynamic_score"}
        ]

        return final_score, issues, {
            "is_transaction": True,
            "hash": original,
            "task": task_name,
            "complexity": round(base_score, 1),
            "mode": mode
        }

    # === JSON MODE ===
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

    return score, issues, {"length": length, "is_transaction": False, "mode": mode}