from pybit.unified_trading import HTTP
import os
from Libraries.logger import get_logger
import requests
from Variables.config import (
    PURCHASE_PRICE,
    LEVERAGE,
    PERCENTAGE_STOP,
    PERCENTAGE_TAKE_PROFIT,
)

logger = get_logger(__name__)


# Credenciais da API da Bybit
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")


session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=False,
)


def set_leverage(crypto):
    try:
        session.set_leverage(
            category="linear",
            symbol=crypto,
            buyLeverage=str(LEVERAGE),
            sellLeverage=str(LEVERAGE),
        )
    except:
        pass


def get_usdt_balance():
    response = session.get_wallet_balance(accountType="UNIFIED")
    if response["retCode"] == 0 and "result" in response:
        for account in response["result"]["list"]:
            for coin in account["coin"]:
                if coin["coin"] == "USDT":
                    return coin["walletBalance"]
    return None


def get_current_price_crypto(crypto):
    # https://bybit-exchange.github.io/docs/v5/market/tickers
    data = session.get_tickers(
        category="inverse",
        symbol=crypto,
    )

    return float(data["result"]["list"][0]["markPrice"])


def find_value_to_aport(crypto):
    price_crypto = get_current_price_crypto(crypto)

    value_aport = (PURCHASE_PRICE / price_crypto) * LEVERAGE

    if value_aport < 0.01:
        return round(value_aport, 4)
    if value_aport < 0.1:
        return round(value_aport, 3)
    if value_aport < 1:
        return round(value_aport, 1)
    if value_aport < 10:
        return round(value_aport, 1)

    return int(value_aport)


def get_all_open_positions_bybit():
    positions = session.get_positions(category="linear", symbol=None, settleCoin="USDT")
    return positions["result"]["list"]


{
    "retCode": 0,
    "retMsg": "OK",
    "result": {
        "nextPageCursor": "BTCUSDT%2C1719444330678%2C0",
        "category": "linear",
        "list": [
            {
                "symbol": "BTCUSDT",
                "leverage": "10",
                "autoAddMargin": 0,
                "avgPrice": "60766.7",
                "liqPrice": "5480.2026151",
                "riskLimitValue": "2000000",
                "takeProfit": "",
                "positionValue": "60.7667",
                "isReduceOnly": False,
                "tpslMode": "Full",
                "riskId": 1,
                "trailingStop": "0",
                "unrealisedPnl": "0.05588",
                "markPrice": "60822.58",
                "adlRankIndicator": 2,
                "cumRealisedPnl": "-0.03342169",
                "positionMM": "0.33391302",
                "createdTime": "1719186463996",
                "positionIdx": 0,
                "positionIM": "6.10674952",
                "seq": 197812367200,
                "updatedTime": "1719444330678",
                "side": "Buy",
                "bustPrice": "",
                "positionBalance": "0",
                "leverageSysUpdatedTime": "",
                "curRealisedPnl": "-0.03342169",
                "size": "0.001",
                "positionStatus": "Normal",
                "mmrSysUpdatedTime": "",
                "stopLoss": "",
                "tradeMode": 0,
                "sessionAvgPrice": "",
            }
        ],
    },
    "retExtInfo": {},
    "time": 1719446282332,
}


def get_all_orders():
    orders = session.get_open_orders(category="linear", symbol=None, settleCoin="USDT")
    return orders["result"]["list"]


{
    "retCode": 0,
    "retMsg": "OK",
    "result": {
        "nextPageCursor": "",
        "category": "linear",
        "list": [
            {
                "symbol": "BTCUSDT",
                "orderType": "Limit",
                "orderLinkId": "",
                "slLimitPrice": "0",
                "orderId": "85c50482-267b-4a42-b03b-e97e4d8fdf12",
                "cancelType": "UNKNOWN",
                "avgPrice": "",
                "stopOrderType": "",
                "lastPriceOnCreated": "60895.3",
                "orderStatus": "New",
                "createType": "CreateByUser",
                "takeProfit": "",
                "cumExecValue": "0",
                "tpslMode": "",
                "smpType": "None",
                "triggerDirection": 0,
                "blockTradeId": "",
                "isLeverage": "",
                "rejectReason": "EC_NoError",
                "price": "58895.2",
                "orderIv": "",
                "createdTime": "1719443133613",
                "tpTriggerBy": "",
                "positionIdx": 0,
                "timeInForce": "GTC",
                "leavesValue": "58.8952",
                "updatedTime": "1719443133614",
                "side": "Buy",
                "smpGroup": 0,
                "triggerPrice": "",
                "tpLimitPrice": "0",
                "cumExecFee": "0",
                "leavesQty": "0.001",
                "slTriggerBy": "",
                "closeOnTrigger": False,
                "placeType": "",
                "cumExecQty": "0",
                "reduceOnly": False,
                "qty": "0.001",
                "stopLoss": "",
                "marketUnit": "",
                "smpOrderId": "",
                "triggerBy": "",
            }
        ],
    },
    "retExtInfo": {},
    "time": 1719446356613,
}


def create_order_buy_long_or_short(crypto, direction, qty):
    try:
        stop_loss = calculate_price_stop_loss(crypto, direction)
        logger.info(f"Stop loss: {stop_loss}")

        take_profit = calculate_price_take_profit(crypto, direction)
        logger.info(f"Take profit: {take_profit}")

        res = session.place_order(
            category="linear",
            symbol=crypto,
            side=direction,
            orderType="Market",
            qty=qty,
            isLeverage=1,
            takeProfit=take_profit,
            stopLoss=stop_loss,
            timeInForce="GTC",
        )
        logger.info(res)

        if res["retMsg"] == "OK":
            return "OK"
    except Exception as e:
        logger.error(f"Error creating order, cryto {crypto}: {e}")
        return "FAIL"


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


def add_take_profit(crypto, direction, tpsl_mode):
    tp_price = calculate_price_take_profit(crypto, direction)

    return session.set_trading_stop(
        category="linear",
        symbol=crypto,
        takeProfit=str(tp_price),
        tpslMode=tpsl_mode,  # Full or Partial
        positionIdx=1 if direction == "Buy" else 2,
    )


def adjuste_round_price(value):

    if value < 0.01:
        return round(float(value), 5)
    if value < 0.1:
        return round(float(value), 4)
    if value < 1:
        return round(float(value), 3)
    if value < 999:
        return round(float(value), 2)
    else:
        return int(value)


def calculate_price_stop_loss(crypto, direction):
    cur_price = get_current_price_crypto(crypto)

    perc = PERCENTAGE_STOP / 100

    price = float(cur_price - (cur_price * perc))

    if direction == "Sell":
        price = float(cur_price + (cur_price * perc))

    price = adjuste_round_price(price)
    return price


def calculate_price_take_profit(crypto, direction):
    cur_price = get_current_price_crypto(crypto)

    perc = PERCENTAGE_TAKE_PROFIT / 100

    price = float(cur_price + (cur_price * perc))

    if direction == "Sell":
        price = float(cur_price - (cur_price * perc))

    price = adjuste_round_price(price)
    return price
