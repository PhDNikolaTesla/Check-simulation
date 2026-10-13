from fastapi import FastAPI, Request
import json
import os
from datetime import datetime

app = FastAPI()

LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "attacker_behavior.log")

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(request: Request, path_name: str):
    client_ip = request.client.host
    method = request.method
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    
    # リクエストボディの取得
    body = ""
    try:
        body = await request.json()
    except Exception:
        try:
            raw_body = await request.body()
            body = raw_body.decode("utf-8", errors="ignore")
        except Exception:
            body = "Could not decode body"

    # 収集するログデータ
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_ip": client_ip,
        "method": method,
        "path": f"/{path_name}",
        "query_params": query_params,
        "headers": headers,
        "body": body
    }

    # ファイルに追記
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

    return {
        "status": "success",
        "message": "Endpoint active",
        "requested_path": f"/{path_name}"
    }
