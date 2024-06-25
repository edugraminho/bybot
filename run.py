import time
import asyncio
import pdb
from Libraries.logger import get_logger
from Variables.config import *
from Libraries.telegram_api import get_messages_group
from Libraries.utils import (
    processing_signal_messages
)

logger = get_logger(__name__)



def trade():
    initial_time = time.time()

    untreated_message = get_messages_group()
    signal_data = processing_signal_messages(untreated_message)
    logger.info(signal_data)

trade()

