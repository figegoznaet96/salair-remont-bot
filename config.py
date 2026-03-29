import logging
import os

TOKEN = os.getenv("TOKEN")
MECHANIC_ID = int(os.getenv("MECHANIC_ID"))
LOGIST_IDS = list(map(int, os.getenv("LOGIST_IDS", "").split(",")))

MACHINES = [
    "КамАЗ А123 ВЕ 77",
    "Volvo FH-456",
    "MAN TGX 789",
    "Scania R500",
    "КамАЗ 6520",
    "Volvo FM-13",
    "Другая машина",
    # Добавляй сюда свои машины
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)