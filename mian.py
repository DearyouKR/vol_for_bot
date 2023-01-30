import requests
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, timedelta, timezone
import pandas as pd

#
symbol_m = [
    "BTC",
    "ETH",
    "BNB",
    "AAVE",
    "ADA",
    "ALGO",
    "APE",
    "APT",
    "ATOM",
    "AVAX",
    "AXS",
    "BAND",
    "CHZ",
    "DOGE",
    "DOT",
    "DYDX",
    "EGLD",
    "ETC",
    "FIL",
    "FLOW",
    "FTM",
    "GALA",
    "ICP",
    "KLAY",
    "LINK",
    "LTC",
    "MANA",
    "MATIC",
    "NEAR",
    "OP",
    "SAND",
    "SHIB",
    "SOL",
    "SUSHI",
    "SXP",
    "THETA",
    "TRX",
    "UNI",
    "WAVES",
    "XRP"
]

# 买入成交量
while True:
    for i in symbol_m:
        url_1h = 'https://api3.binance.com/api/v3/klines?symbol=' + i + 'USDT&interval=1h&limit=360'
        data_1h = requests.get(url_1h)
        data_json_1h = data_1h.json()
        df_1h = pd.DataFrame(data_json_1h)[5]
        df_1h["vol"] = df_1h.astype(float)
        vol_ma = round(df_1h["vol"].mean())
        # print(vol_ma)

        url = 'https://api3.binance.com/api/v3/klines?symbol=' + i + 'USDT&interval=15m&limit=2'

        data = requests.get(url)
        data_json = data.json()[0]
        # print(data_json)
        buy = float(data_json[9])
        vol = float(data_json[5])
        # print(vol)
        bfb = (buy / vol) * 100
        open_time = int(float(data_json[0]) / 1000)
        td = timedelta(hours=8)
        tz = timezone(td)
        dt = datetime.fromtimestamp(open_time, tz)
        dt = dt.strftime('%m-%d %H:%M')

        if bfb > 70 and vol > vol_ma / 2:
            txt = dt + "---" + i + "---15分钟筛选后-超级-积极买入---" + str(round(bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        elif bfb < 30 and vol > vol_ma / 2:
            txt = dt + "---" + i + "---15分钟筛选后-超级-积极卖入---" + str(round(100 - bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        elif bfb > 60 and vol > vol_ma / 2:
            txt = dt + "---" + i + "---15分钟筛选后-普通-积极买入---" + str(round(bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        elif bfb < 40 and vol > vol_ma / 2:
            txt = dt + "---" + i + "---15分钟筛选后-普通-积极卖入---" + str(round(100 - bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        elif bfb > 75 and vol > vol_ma / 4:
            txt = dt + "---" + i + "---15分钟出现-积极买入---" + str(round(bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        elif bfb < 25 and vol > vol_ma / 4:
            txt = dt + "---" + i + "---15分钟出现-积极卖入---" + str(round(100 - bfb))
            xiaoding.send_text(msg=txt, is_at_all=False)
        else:
            print(i + "--还未满足条件")

    time.sleep(300)
