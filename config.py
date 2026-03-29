import logging
import os

print("=== FULL ENV FROM RAILWAY ===")
for key, value in os.environ.items():
    if key in ["TOKEN", "MECHANIC_ID", "LOGIST_IDS"]:
        print(f"{key} = {value}")
print("=============================")

TOKEN = os.getenv("TOKEN")
MECHANIC_ID = int(os.getenv("MECHANIC_ID") or 0)
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
