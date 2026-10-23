import random
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

# CORS設定（すべてのオリジンからの通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# システムの動作状態（初期状態は休止中）
SYSTEM_STATE = {
    "is_active": False,
    "current_mode": "STANDBY"
}

# 設定されたパスキー
UNLOCK_PASSKEY = "KAMAKURA-SOLITARY-ACTIVATE-2026"  # 起動キー
LOCK_PASSKEY = "KAMAKURA-SOLITARY-STANDBY-2026"    # 休止キー

# 量子・高度脅威概念プール
WILD_CONCEPTS = [
    {
        "category": "量子技術・暗号", 
        "concept": "ショアのアルゴリズムを用いた公開鍵暗号体系（RSA/ECC）の瞬時破綻とリプレイス遅延の悪用",
        "mitre_id": "T1588.002",
        "kill_chain_phase": "Resource Development / Cryptographic Compromise"
    },
    {
        "category": "量子技術・通信", 
        "concept": "量子もつれ・量子鍵配送（QKD）ネットワークへの巧妙な中間者（MITM）観測干渉バイパス",
        "mitre_id": "T1557",
        "kill_chain_phase": "Credential Access / Interception"
    },
    {
        "category": "攻撃手法(TTPs)", 
        "concept": "Living-off-the-Land手法を用いた正規管理ツールへの偽装潜伏",
        "mitre_id": "T1078",
        "kill_chain_phase": "Defense Evasion / Persistence"
    },
    {
        "category": "攻撃手法(TTPs)", 
        "concept": "DNSトンネリングおよびステガノグラフィによる暗号化データ隠蔽抽出",
        "mitre_id": "T1048",
        "kill_chain_phase": "Exfiltration"
    },
    {
        "category": "空間・生体", 
        "concept": "脳波・神経インターフェース（BCI）プロトコルの直接乗っ取り",
        "mitre_id": "T1531",
        "kill_chain_phase": "Impact / Control Takeover"
    },
    {
        "category": "生態・システム", 
        "concept": "菌糸型分散自律ネットワーク（DAO）のコンセンサス偽装",
        "mitre_id": "T1565",
        "kill_chain_phase": "Data Manipulation"
    }
]

class AuthRequest(BaseModel):
    passkey: str

class SecuritySimRequest(BaseModel):
    target_system: str
    cross_count: Optional[int] = 2

# WEBダッシュボード（HTML/JS/CSS）の配信
@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyber Threat Simulation Dashboard</title>
        <style>
            :root {
                --bg-color: #0d1117;
                --card-bg: #161b22;
                --border-color: #30363d;
                --text-color: #c9d1d9;
                --accent-green: #2ea043;
                --accent-red: #da3633;
                --accent-blue: #58a6ff;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                margin: 0;
                padding: 16px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .card {
                background-color: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 16px;
            }
            h1, h2 {
                margin-top: 0;
                font-size: 1.2rem;
            }
            .status-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.9rem;
            }
            .status-standby { background-color: var(--accent-red); color: #fff; }
            .status-active { background-color: var(--accent-green); color: #fff; }
            input, button {
                width: 100%;
                padding: 12px;
                margin-top: 8px;
                border-radius: 6px;
                border: 1px solid var(--border-color);
                box-sizing: border-box;
                font-size: 1rem;
            }
            input {
                background-color: #0d1117;
                color: var(--text-color);
            }
            button {
                background-color: var(--accent-blue);
                color: #fff;
                font-weight: bold;
                cursor: pointer;
                border: none;
            }
            button:active { opacity: 0.8; }
            .btn-lock { background-color: var(--accent-red); }
            .result-box {
                background-color: #0d1117;
                border: 1px solid var(--border-color);
                padding: 12px;
                border-radius: 6px;
                font-family: monospace;
                white-space: pre-wrap;
                font-size: 0.85rem;
                max-height: 250px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>システムステータス</h1>
                <div>
                    状態: <span id="statusBadge" class="status-badge status-standby">確認中...</span>
                </div>
            </div>

            <div class="card">
                <h2>パスキー認証（State Control）</h2>
                <input type="password" id="passkeyInput" placeholder="パスキーを入力...">
                <button onclick="sendAuth('/auth/unlock')">起動（ACTIVE）</button>
                <button onclick="sendAuth('/auth/lock')" class="btn-lock">休止（STANDBY）</button>
            </div>

            <div class="card">
                <h2>脅威シミュレーション実行</h2>
                <input type="text" id="targetInput" placeholder="標的システム名（例: 次世代金融基盤）" value="次世代金融・暗号通信インフラ">
                <button onclick="runSimulation()">シミュレーション実行</button>
                <h3>実行結果:</h3>
                <div id="resultOutput" class="result-box">待機中...</div>
            </div>
        </div>

        <script>
            async function updateStatus() {
                try {
                    const res = await fetch('/status');
                    const data = await res.json();
                    const badge = document.getElementById('statusBadge');
                    if (data.is_active) {
                        badge.textContent = 'ACTIVE (稼働中)';
                        badge.className = 'status-badge status-active';
                    } else {
                        badge.textContent = 'STANDBY (休止中)';
                        badge.className = 'status-badge status-standby';
                    }
                } catch (e) {
                    console.error(e);
                }
            }

            async function sendAuth(endpoint) {
                const passkey = document.getElementById('passkeyInput').value;
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({passkey: passkey})
                });
                const data = await res.json();
                alert(data.message || data.detail);
                document.getElementById('passkeyInput').value = '';
                updateStatus();
            }

            async function runSimulation() {
                const target = document.getElementById('targetInput').value;
                const res = await fetch('/simulate-threat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target_system: target, cross_count: 2})
                });
                const data = await res.json();
                document.getElementById('resultOutput').textContent = JSON.stringify(data, null, 2);
            }

            updateStatus();
        </script>
    </body>
    </html>
    """
    return html_content

# ステータス確認用エンドポイント
@app.get("/status")
def get_status():
    return {
        "status": SYSTEM_STATE["current_mode"],
        "is_active": SYSTEM_STATE["is_active"]
    }

# パスキーによる起動（Active化）
@app.post("/auth/unlock")
def unlock_system(req: AuthRequest):
    if req.passkey == UNLOCK_PASSKEY:
        SYSTEM_STATE["is_active"] = True
        SYSTEM_STATE["current_mode"] = "ACTIVE"
        return {"status": "SUCCESS", "mode": "ACTIVE", "message": "システムが正常に起動しました。"}
    raise HTTPException(status_code=401, detail="無効な起動パスキーです。")

# パスキーによる休止（Standby化）
@app.post("/auth/lock")
def lock_system(req: AuthRequest):
    if req.passkey == LOCK_PASSKEY:
        SYSTEM_STATE["is_active"] = False
        SYSTEM_STATE["current_mode"] = "STANDBY"
        return {"status": "SUCCESS", "mode": "STANDBY", "message": "システムは休止状態に移行しました。"}
    raise HTTPException(status_code=401, detail="無効な休止パスキーです。")

# 脅威シミュレーション実行（Active時のみ稼働）
@app.post("/simulate-threat")
def simulate_threat(req: SecuritySimRequest):
    if not SYSTEM_STATE["is_active"]:
        raise HTTPException(status_code=403, detail="システムは休止状態（STANDBY）です。起動用パスキーを入力してください。")

    target = req.target_system
    count = max(1, min(req.cross_count, 3))
    chosen_threats = random.sample(WILD_CONCEPTS, count)
    
    threat_indices = [round(random.uniform(0.90, 0.99), 2) for _ in range(count)]
    avg_threat_index = round(sum(threat_indices) / count, 2)
    
    kill_chain_steps = [
        {
            "step": i + 1,
            "phase": t["kill_chain_phase"],
            "mitre_attack_id": t["mitre_id"],
            "vector": f"【{t['category']}】{t['concept']}"
        }
        for i, t in enumerate(chosen_threats)
    ]

    return {
        "mode": "quantum_enhanced_threat_simulation",
        "system_status": SYSTEM_STATE["current_mode"],
        "target_system": target,
        "cross_count": count,
        "wildcard_threat_index": avg_threat_index,
        "kill_chain_steps": kill_chain_steps,
        "simulation_report": f"【高度脅威シミュレーション作動中 / 標的: {target}】"
    }
