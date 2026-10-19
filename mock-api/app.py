import random
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# MITRE ATT&CK風のIDとキルチェーンフェーズを統合した高度脅威概念プール
WILD_CONCEPTS = [
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
        "category": "攻撃手法(TTPs)", 
        "concept": "サプライチェーン依存関係を悪用した依存ライブラリへのバックドア汚染",
        "mitre_id": "T1195",
        "kill_chain_phase": "Initial Access"
    },
    {
        "category": "物理・量子", 
        "concept": "量子もつれ・量子鍵配送（QKD）ネットワークの観測干渉バイパス",
        "mitre_id": "T1557",
        "kill_chain_phase": "Credential Access / Interception"
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

class PredictionRequest(BaseModel):
    topic: str

class SecuritySimRequest(BaseModel):
    target_system: str
    cross_count: Optional[int] = 2

@app.get("/")
def read_root():
    return {"message": "Advanced Cyber Threat Simulation API is running successfully!"}

@app.post("/predict")
def predict_future(request: PredictionRequest):
    topic = request.topic
    return {
        "topic": topic,
        "prediction_horizon": "2035年",
        "thought_process": [
            "1. 高度持続的脅威（APT）データベースおよびATT&CKベクトルのマッピング",
            "2. 攻撃者の戦術・技術と異種インフラの構造的相関シミュレーション",
            "3. 複合的ゼロデイ攻撃キルチェーンの確率的重み付け"
        ],
        "scenarios": [
            f"{topic}を標的とした自律型エージェントによる多次元スキャンが検知されています。",
            f"境界防御を迂回する内部潜伏に対し、ゼロトラストアーキテクチャの動的再構築が求められます。"
        ],
        "confidence_score": 0.88
    }

@app.post("/simulate-threat")
def simulate_threat(req: SecuritySimRequest):
    target = req.target_system
    count = max(1, min(req.cross_count, 3))
    chosen_threats = random.sample(WILD_CONCEPTS, count)
    
    threat_indices = [round(random.uniform(0.88, 0.99), 2) for _ in range(count)]
    avg_threat_index = round(sum(threat_indices) / count, 2)
    
    # キルチェーンのステップ構造を構築
    kill_chain_steps = [
        {
            "step": i + 1,
            "phase": t["kill_chain_phase"],
            "mitre_attack_id": t["mitre_id"],
            "vector": f"【{t['category']}】{t['concept']}"
        }
        for i, t in enumerate(chosen_threats)
    ]
    
    response_text = (
        f"【高度脅威シミュレーション作動 / 標的システム: {target}】\n\n"
        f"ATT&CKフレームワークおよび異分野システムを融合した複合キルチェーンを生成しました。\n"
        f"算出された異端攻撃度（Wildcard Threat Index）: {avg_threat_index}"
    )

    return {
        "mode": "mitre_linked_threat_simulation",
        "target_system": target,
        "cross_count": count,
        "wildcard_threat_index": avg_threat_index,
        "kill_chain_steps": kill_chain_steps,
        "simulation_report": response_text
    }
