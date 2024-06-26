import time
import asyncio
import pdb
from Libraries.logger import get_logger
from Libraries.telegram_api import get_messages_group
from Libraries.utils import processing_signal_messages
from Libraries.futures import (
    get_all_open_positions_bybit,
    get_current_price_crypto,
    get_usdt_balance,
)

from Database.db_connection import get_db
from Database.db_services import SignalsService

logger = get_logger(__name__)


def trade():
    initial_time = time.time()

    untreated_message = get_messages_group()
    signal_data = processing_signal_messages(untreated_message)

    logger.info(get_usdt_balance())

    SignalsService(get_db()).save_signal(signal_data)


trade()
