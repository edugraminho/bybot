import pdb
import re
import pytz
from Variables.config import DATE_NOW
from .utils import convert_date_to_timestamp
from Libraries.logger import get_logger

logger = get_logger(__name__)


def handle_msgs(untreated_data):
    try:
        all_msgs_data = []

        for data in untreated_data:
            if data.message != None:

                timestamp_now = convert_date_to_timestamp(DATE_NOW)

                reply_to = (
                    data.reply_to.reply_to_msg_id if data.reply_to is not None else ""
                )

                new_crypto = re.search("#(\w+)/", data.message)

                direction = re.search("\((\w+)\S*,", data.message)

                crypto_name = None
                direction_type = None
                signal_type = None
                insert = False

                if new_crypto != None:
                    crypto_name = new_crypto[1].strip().upper()
                    signal_type = "NEW"

                if direction != None and reply_to == "":
                    direction_type = direction[1].strip().upper()
                    insert = True

                if insert:
                    signal_message = {
                        "id": data.id,
                        "reply_to": reply_to,
                        "date": DATE_NOW,
                        "timestamp": timestamp_now,
                        "crypto_name": f"{crypto_name}USDT",
                        "direction": "Buy" if direction_type == "LONG" else "Sell",
                        "signal_type": signal_type,
                    }

                    all_msgs_data.append(signal_message)
        return all_msgs_data
    except Exception as e:
        logger.error(e)
        pass
