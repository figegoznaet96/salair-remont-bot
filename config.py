import logging
import os

# === DEBUG — покажет, что именно подгружается ===
print("=== DEBUG RAILWAY ===")
print("TOKEN:", "✅ SET" if os.getenv("TOKEN") else "❌ MISSING")
print("MECHANIC_ID:", os.getenv("MECHANIC_ID"))
print("LOGIST_IDS:", os.getenv("LOGIST_IDS"))
print("=====================")

TOKEN = os.getenv("TOKEN")
MECHANIC_ID = int(os.getenv("MECHANIC_ID") or 0)      # 0 — если вдруг None
LOGIST_IDS = [int(x) for x in os.getenv("LOGIST_IDS", "").split(",") if x]

MACHINES = [
    "КамАЗ А123 ВЕ 77",
    "Volvo FH-456",
    "MAN TGX 789",
    "Scania R500",
    "КамАЗ 6520",
    "Volvo FM-13",
    "Другая машина",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
