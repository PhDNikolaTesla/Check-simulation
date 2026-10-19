import random
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# システムの動作状態（初期状態は休止中）
SYSTEM_STATE = {
    "is_active": False,
    "current_mode": "STANDBY"
}

# 設定されたパスキー（開発用初期値）
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

@app.get("/")
def read_root():
    return {
        "status": SYSTEM_STATE["current_mode"],
        "is_active": SYSTEM_STATE["is_active"],
        "message": "Security Simulation Application Backend Operating."
    }

# パスキーによる起動（Active化）
@app.post("/auth/unlock")
def unlock_system(req: AuthRequest):
    if req.passkey == UNLOCK_PASSKEY:
        SYSTEM_STATE["is_active"] = True
        SYSTEM_STATE["current_mode"] = "ACTIVE"
        return {"status": "SUCCESS", "mode": "ACTIVE", "message": "システムが正常に起動しました。脅威シミュレーション機能が有効です。"}
    raise HTTPException(status_code=401, detail="無効な起動パスキーです。")

# パスキーによる休止（Standby化）
@app.post("/auth/lock")
def lock_system(req: AuthRequest):
    if req.passkey == LOCK_PASSKEY:
        SYSTEM_STATE["is_active"] = False
        SYSTEM_STATE["current_mode"] = "STANDBY"
        return {"status": "SUCCESS", "mode": "STANDBY", "message": "システムは休止状態に移行しました。コア機能はロックされました。"}
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
