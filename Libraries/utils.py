import pdb
import re
import pytz
from Variables.config import *
from Libraries.logger import get_logger

logger = get_logger(__name__)


def processing_signal_messages(untreated_data):
    try:
        #logger.info(f"Processando as mensagem...")

        all_msgs_data = []

        for data in untreated_data:
            if data.message != None:

                _date = data.date.astimezone(
                    pytz.timezone("America/Sao_Paulo")).strftime("%d/%m %H:%M:%S")

                reply_to = data.reply_to.reply_to_msg_id \
                    if data.reply_to is not None else ""

                new_crypto = re.search("#(\w+)/", data.message)
                # closed_crypto = re.search('(?<=#)(.[^#]*USDT)', data.message)

                direction = re.search("\((\w+)\S*,", data.message)

                # closed_signal = re.search(
                #     'Closed|All entry|Cancelled', data.message)

                # all_take_profit = re.search('All take-profit', data.message)

                crypto_name = None
                direction_type = None
                signal_type = None
                insert = False

                if new_crypto != None:
                    crypto_name = new_crypto[1].strip().upper()
                    signal_type = "NEW"

                # if closed_crypto != None:
                #     crypto_name = closed_crypto[0].strip().replace(
                #         "/", "").upper()

                # if closed_signal != None:
                #     signal_type = "CLOSE"
                #     insert = True
                #     direction_type = "OPEN_ORDER"

                # if all_take_profit != None:
                #     signal_type = "ALL_TAKE_PROFIT"
                #     insert = True
                #     direction_type = "OPEN_ORDER"

                if direction != None and reply_to == "":
                    direction_type = direction[1].strip().upper()
                    insert = True

                if insert:
                    signal_message = {
                        "_id": data.id,
                        "reply_to": reply_to,
                        "date": str(_date),
                        "crypto_name": f"{crypto_name}USDT",
                        "direction": direction_type,
                        "signal_type": signal_type,
                        "status": "",
                        "price_buy": "",
                        "stop_price": "",
                        "qty": "",
                    }

                    all_msgs_data.append(signal_message)
        return all_msgs_data
    except Exception as e:
        logger.error(e)
        pass


