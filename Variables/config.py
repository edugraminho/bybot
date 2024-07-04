from pathlib import Path, PurePath
import os
from datetime import datetime, timedelta


# ==================== API BINANCE ====================
PURCHASE_PRICE = 1
PERCENTAGE_STOP = 2
LEVERAGE = 20

LIST_TARGETS_TAKE_PROFITS = [4, 7]
PERCENTAGE_TAKE_PROFIT = 7

MESSAGES_LIMIT = 10

# ====================== DIRETÓRIOS LOCAIS e DATAS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_DIRECTORY = os.path.join(ROOT, "Data")
SESSION_DIRECTORY = os.path.join(ROOT, "Session")
CURRENT_DAY = datetime.now().strftime("%d/%m")
FULL_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
DATE_NOW = datetime.now().strftime(FULL_DATE_FORMAT)
