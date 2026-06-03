def calculate_quality_score(trajectory: list, mode: str = "normal"):
    if not trajectory or not isinstance(trajectory, list):
        return 0.0, ["Trajectory rỗng hoặc không hợp lệ"], {}

    score = 100.0
    issues = []
    
    length = len(trajectory)
    has_grasp = any("grasp" in str(step).lower() for step in trajectory)
    has_place = any("place" in str(step).lower() for step in trajectory)
    
    success = False
    if trajectory and isinstance(trajectory[-1], dict):
        success = bool(trajectory[-1].get("success", False))

    # Penalty theo mode
    penalties = {
        "strict": {"short": 30, "grasp": 35, "place": 35, "fail": 40},
        "normal": {"short": 20, "grasp": 25, "place": 25, "fail": 30},
        "loose":  {"short": 15, "grasp": 20, "place": 20, "fail": 25}
    }[mode]

    if length < 5:
        score -= penalties["short"]
        issues.append(f"Trajectory quá ngắn (chỉ {length} bước)")

    if not has_grasp:
        score -= penalties["grasp"]
        issues.append("Thiếu hành động Grasp")

    if not has_place:
        score -= penalties["place"]
        issues.append("Thiếu hành động Place")

    if not success:
        score -= penalties["fail"]
        issues.append("Bước cuối không thành công (success = False)")

    score = max(0, min(100, round(score, 1)))

    # Weighted score
    weighted = (
        (30 if has_grasp else 0) * 0.3 +
        (30 if has_place else 0) * 0.3 +
        min(length * 2, 20) * 0.2 +
        (20 if success else 0) * 0.2
    )

    final_score = round(score * 0.6 + weighted * 0.4, 1)

    metrics = {
        "length": length,
        "has_grasp": has_grasp,
        "has_place": has_place,
        "success": success,
        "weighted_score": round(weighted, 1)
    }

    return final_score, issues, metrics