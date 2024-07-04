import time
import asyncio
import pdb
from Libraries.logger import get_logger
from Libraries.telegram_api import get_messages_group
from Libraries.handle_msg import handle_msgs
from Libraries.futures import (
    get_all_open_positions_bybit,
    get_current_price_crypto,
    get_usdt_balance,
    get_all_open_positions_bybit,
    get_all_orders,
    create_order_buy_long_or_short,
    find_value_to_aport,
    set_leverage,
)

from Database.db_connection import get_db
from Database.db_services import SignalsService

logger = get_logger(__name__)


def trade():
    initial_time = time.time()

    untreated_message = get_messages_group()
    signals_data = handle_msgs(untreated_message)

    db_session = next(get_db())
    db = SignalsService(db_session)

    for signal_data in signals_data:
        db.save_signal(signal_data)

    all_signals = db.get_all_signals()

    all_positions = get_all_open_positions_bybit()
    # logger.info(all_positions)

    all_orders = get_all_orders()

    balance = get_usdt_balance()
    for signal in all_signals:
        # TODO achar a quantidade para inserir na ordem de compra

        for position in all_positions:

            #################################################################
            #################### VERIFICA DUPLICIDADES ######################
            if (
                position["symbol"] == signal.crypto_name
                and signal.signal_type == "NEW"
                and signal.direction == position["side"]
            ):
                db.update_signal(
                    {"status": "DUPLICATE", "signal_type": "DUPLICATE"}, signal.id
                )

            ####### FECHA POSICAO SE APARECER NOVA NA DIRECAO OPOSTA ########
            if (
                position["symbol"] == signal.crypto_name
                and signal.signal_type == "NEW"
                and signal.direction != position["side"]
            ):
                # TODO cancelar a aberta e abrir uma nova
                symbol = position["symbol"]
                side = position["side"]

                logger.info(f"Signal {signal.crypto_name} not matched with position.")
                # db.update_signal({"status": "NOT_MATCHED"}, signal.id)


        #################################################################
        ############################ BUY ###############################

        if signal.signal_type == "NEW" and signal.status == None:
            set_leverage(crypto=signal.crypto_name)
            value_aport = find_value_to_aport(signal.crypto_name)

            res = create_order_buy_long_or_short(
                crypto=signal.crypto_name, direction=signal.direction, qty=value_aport
            )

            if res == "OK":
                db.update_signal(
                    {"status": "COMPLETED", "signal_type": "OK"}, signal.id
                )
                logger.info(f"Signal {signal.crypto_name} created successfully.")
            else:
                db.update_signal(
                    {"status": "FAIL", "signal_type": "ERROR"}, signal.id
                )


    actual_time = time.time()
    exec_time = actual_time - initial_time
    # logger.info(f"Tempo de execução: {exec_time:.2f} segundos")


trade()
