from pybit.unified_trading import HTTP
import os
from Libraries.logger import get_logger

logger = get_logger(__name__)


# Credenciais da API da Bybit
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")


session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=False,
)



def futures_change_leverage(crypto, leverage):
    return session.set_leverage(symbol=crypto, leverage=leverage)


def get_current_price_crypto(crypto):
    return session.latest_information_for_symbol(symbol=crypto)["result"][0][
        "last_price"
    ]


def create_order_buy_long_or_short(crypto, buy_or_sell, direction, quantity):
    side = "Buy" if buy_or_sell == "buy" else "Sell"
    order_type = "Market" if direction == "long" else "Limit"
    return session.place_active_order(
        symbol=crypto,
        side=side,
        order_type=order_type,
        qty=quantity,
        time_in_force="GoodTillCancel",
    )


def closed_market(crypto, direction, quantity):
    side = "Sell" if direction == "long" else "Buy"
    return session.place_active_order(
        symbol=crypto,
        side=side,
        order_type="Market",
        qty=quantity,
        time_in_force="GoodTillCancel",
    )


def get_balance():
    return session.get_wallet_balance(accountType="UNIFIED")


def get_usdt_balance():
    response = session.get_wallet_balance(accountType="UNIFIED")
    if response["retCode"] == 0 and "result" in response:
        for account in response["result"]["list"]:
            for coin in account["coin"]:
                if coin["coin"] == "USDT":
                    return coin["walletBalance"]
    return None


def find_value_to_aport(crypto):
    balance = get_balance()
    # Supondo que você deseja alocar uma porcentagem do saldo USDT
    usdt_balance = balance["USDT"]["available_balance"]
    allocation_percentage = 0.1  # 10%
    return usdt_balance * allocation_percentage


def calculate_price_stop_limit(crypto, direction):
    current_price = float(get_current_price_crypto(crypto))
    if direction == "long":
        stop_price = current_price * 0.95  # 5% abaixo do preço atual
    else:
        stop_price = current_price * 1.05  # 5% acima do preço atual
    return stop_price


def get_all_open_positions_bybit():
    return session.my_position()["result"]


def add_stop_limit(crypto, direction, stop_price, quantity):
    side = "Sell" if direction == "long" else "Buy"
    return session.place_active_order(
        symbol=crypto,
        side=side,
        order_type="Stop",
        stop_px=stop_price,
        qty=quantity,
        base_price=stop_price,  # Este é o preço de ativação do stop
        time_in_force="GoodTillCancel",
    )


def cancel_open_order(order_id):
    return session.cancel_active_order(order_id=order_id)


def add_take_profit(crypto, direction, take_profit_price, quantity):
    side = "Sell" if direction == "long" else "Buy"
    return session.place_active_order(
        symbol=crypto,
        side=side,
        order_type="TakeProfit",
        take_profit=take_profit_price,
        qty=quantity,
        time_in_force="GoodTillCancel",
    )
