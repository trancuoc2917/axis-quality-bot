def calculate_quality_score(trajectory: any, mode: str = "full"):
    # Chuẩn hóa input
    if isinstance(trajectory, str):
        try:
            import json
            trajectory = json.loads(trajectory)
        except:
            pass

    if not trajectory:
        return 0.0, [{"message": "Trajectory rỗng hoặc không hợp lệ", "type": "empty"}], {}

    score = 100.0
    issues = []
    
    # Xử lý cả list và dict
    if isinstance(trajectory, dict):
        trajectory = [trajectory]  # chuyển dict thành list 1 phần tử

    length = len(trajectory)
    has_grasp = any("grasp" in str(step).lower() for step in trajectory)
    has_place = any("place" in str(step).lower() for step in trajectory)
    
    success = False
    if trajectory and isinstance(trajectory[-1], dict):
        success = bool(trajectory[-1].get("success", False))

    penalties = {
        "strict": {"short": 30, "grasp": 35, "place": 35, "fail": 40},
        "normal": {"short": 20, "grasp": 25, "place": 25, "fail": 30},
        "loose":  {"short": 15, "grasp": 20, "place": 20, "fail": 25},
        "full":   {"short": 20, "grasp": 25, "place": 25, "fail": 30}
    }.get(mode, {"short": 20, "grasp": 25, "place": 25, "fail": 30})

    if length < 5:
        score -= penalties["short"]
        issues.append({"message": f"Trajectory quá ngắn (chỉ {length} bước)", "type": "short"})

    if not has_grasp:
        score -= penalties["grasp"]
        issues.append({"message": "Thiếu hành động Grasp", "type": "grasp"})

    if not has_place:
        score -= penalties["place"]
        issues.append({"message": "Thiếu hành động Place", "type": "place"})

    if not success:
        score -= penalties["fail"]
        issues.append({"message": "Bước cuối không thành công (success = False)", "type": "fail"})

    score = max(0, min(100, round(score, 1)))

    metrics = {
        "length": length,
        "has_grasp": has_grasp,
        "has_place": has_place,
        "success": success,
        "mode": mode
    }

    return score, issues, metrics