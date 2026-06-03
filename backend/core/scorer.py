import json
import requests
from typing import Any, List, Dict

def is_transaction_hash(text: str) -> bool:
    """Kiểm tra có phải Transaction Hash không"""
    text = text.strip()
    return text.startswith("0x") and len(text) in (66, 64)

def fetch_transaction(tx_hash: str, chain: str = "ethereum"):
    """Fetch transaction từ public API"""
    try:
        if chain == "bsc":
            url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey=freekey"
        else:  # default ethereum
            url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey=freekey"
        
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if data.get("result"):
            tx = data["result"]
            return {
                "hash": tx_hash,
                "from": tx.get("from"),
                "to": tx.get("to"),
                "value": int(tx.get("value", 0)) / 10**18,
                "input": tx.get("input", "")[:100] + "..." if len(tx.get("input", "")) > 100 else tx.get("input", ""),
                "blockNumber": tx.get("blockNumber")
            }
        return None
    except:
        return None

def calculate_quality_score(trajectory: Any, mode: str = "full"):
    original_input = trajectory

    # === XỬ LÝ TRANSACTION HASH ===
    if isinstance(trajectory, str) and is_transaction_hash(trajectory):
        tx_data = fetch_transaction(trajectory)
        if tx_data:
            trajectory = tx_data  # chuyển thành dict để phân tích
            is_tx = True
        else:
            return 0.0, [{"message": "Không fetch được Transaction. Kiểm tra lại hash hoặc mạng", "type": "fetch_error"}], {}
    else:
        is_tx = False

    # === XỬ LÝ JSON STRING ===
    if isinstance(trajectory, str):
        try:
            trajectory = json.loads(trajectory)
        except:
            pass

    if not trajectory:
        return 0.0, [{"message": "Trajectory rỗng hoặc không hợp lệ", "type": "empty"}], {}

    # Chuẩn bị dữ liệu
    if isinstance(trajectory, dict):
        trajectory = [trajectory]

    length = len(trajectory)
    score = 100.0
    issues = []

    # Logic chấm điểm cơ bản
    if length < 5:
        score -= 25
        issues.append({"message": f"Trajectory quá ngắn (chỉ {length} bước)", "type": "short"})

    # Nếu là transaction
    if is_tx:
        issues.append({"message": "Phân tích Transaction Hash thành công", "type": "tx_success"})
        score = 85.0  # điểm mặc định cho TX

    score = max(0, min(100, round(score, 1)))

    metrics = {
        "length": length,
        "is_transaction": is_tx,
        "mode": mode
    }

    return score, issues, metrics