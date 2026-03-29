import logging

# ==================== НАСТРОЙКИ БОТА ====================
TOKEN = "8636454027:AAHAoooVrvA-_oQLb2jXzWE_drXQz-CLp8o"
MECHANIC_ID = 1093924638
LOGIST_IDS = [8504590692]          # можно добавить ещё через запятую

MACHINES = [
    "КамАЗ А123 ВЕ 77",
    "Volvo FH-456",
    "MAN TGX 789",
    "Scania R500",
    "КамАЗ 6520",
    "Volvo FM-13",
    "Другая машина",
]
# =======================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
