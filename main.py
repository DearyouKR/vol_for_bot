import requests
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, timedelta, timezone
import pandas as pd
import schedule

# WebHook地址
# 天量
webhook_5m_top = 'https://oapi.dingtalk.com/robot/send?access_token=f3fbe0e3bb95a40d0a9bf5f4498d555410237695a47b6236cdecc0c30651011e'
secret_5m_top = 'SECfa2bcc5048a060d89a7305a2cf5c34712750751dbac4595c4fb1262d259309ef'
xiaoding_5m_top = DingtalkChatbot(webhook_5m_top, secret=secret_5m_top)

# 超级
webhook_5m_super = 'https://oapi.dingtalk.com/robot/send?access_token=92fc3ffe8f4285d6aa1ce9dad2f8c648a10a5e8f9c831774bcc00ab12f02a951'
secret_5m_super = 'SEC4278cf9284017d4017c615092625e4aed9348862b566baae5addd6b2e51f882c'
xiaoding_5m_super = DingtalkChatbot(webhook_5m_super, secret=secret_5m_super)

# 普通
webhook_5m_ordinary = 'https://oapi.dingtalk.com/robot/send?access_token=a1d975fcaa3b7392f9f1ccb463bcafaf3d86b1932424c23e8917650c17798d1c'
secret_5m_ordinary = 'SECeaf7b79fd1e67e95fbeb289329037f6951ee7cdf6caa89b1e85ee9b0752fedd6'
xiaoding_5m_ordinary = DingtalkChatbot(webhook_5m_ordinary, secret=secret_5m_ordinary)

symbol_list = [
    "BTC",
    "ETH",
    "BNB",
    "XRP",
    "ADA",
    "DOGE",
    "MATIC",
    "SOL",
    "DOT",
    "LTC",
    "AVAX",
    "SHIB",
    "TRX",
    "UNI",
    "ATOM",
    "LINK",
    "ETC",
    "APT",
    "APE",
    "FIL",
    "NEAR",
    "ALGO",
    "ICP",
    "FTM",
    "MANA",
    "AAVE",
    "FLOW",
    "SAND",
    "AXS",
    "EGLD",
    "THETA",
    "CHZ",
    "KLAY",
    "OP",
    "DYDX",
    "GALA",
    "SUSHI",
    "WAVES",
    "SXP",
    "BAND"
]
circulating_supply_list = [
    19279156,
    122373866,
    157901321,
    50803611248,
    34593679000,
    132670764300,
    8734317475,
    372167563,
    1152837032,
    72187491,
    314976329,
    549063278876301,
    91799812419,
    762209327,
    286370297,
    507999970,
    139231738,
    160289078,
    368593750,
    377599710,
    852251512,
    7201410778,
    284694564,
    2773337050,
    1855084192,
    14093193,
    1036200000,
    1499470108,
    100469735,
    24938279,
    1000000000,
    6661685577,
    3090359037,
    234748364,
    156256174,
    6977205436,
    222257372,
    110517154,
    553431268,
    52800606
]


# 买入成交量
def vol_sx():
    for symbol, circulating_supply in zip(symbol_list, circulating_supply_list):
        url_15m = 'https://api3.binance.com/api/v3/klines?symbol=' + symbol + 'USDT&interval=1d&limit=192'
        data_15m = requests.get(url_15m)
        data_json_15m = data_15m.json()
        df_15m = pd.DataFrame(data_json_15m)[5]
        df_15m["vol"] = df_15m.astype(float) / 72
        vol_ma = round(df_15m["vol"].mean())

        url = 'https://api3.binance.com/api/v3/klines?symbol=' + symbol + 'USDT&interval=5m&limit=2'

        data = requests.get(url)
        data_json = data.json()[0]
        buy = float(data_json[9])
        vol = float(data_json[5])
        circulating_supply_bfb = (vol / circulating_supply) * 100

        if vol < 1:
            vol = 2
        if buy < 1:
            buy = vol / 2

        bfb = (buy / vol) * 100

        open_time = int(float(data_json[0]) / 1000)
        td = timedelta(hours=8)
        tz = timezone(td)
        dt = datetime.fromtimestamp(open_time, tz)
        dt = dt.strftime('%m-%d %H:%M')
        top_1 = 75
        top_2 = 65
        bottom_1 = 25
        bottom_2 = 35

        if bfb > top_1 and vol > vol_ma * 3:
            txt = dt + "--" + symbol + "--现货5分钟-天量B-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_top.send_text(msg=txt, is_at_all=False)
        elif bfb > top_2 and vol > vol_ma * 3:
            txt = dt + "--" + symbol + "--现货5分钟-天量A-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_top.send_text(msg=txt, is_at_all=False)
        elif bfb > top_1 and vol > vol_ma * 2:
            txt = dt + "--" + symbol + "--现货5分钟-超级B-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_super.send_text(msg=txt, is_at_all=False)
        elif bfb > top_2 and vol > vol_ma * 2:
            txt = dt + "--" + symbol + "--现货5分钟-超级A-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_super.send_text(msg=txt, is_at_all=False)
        elif bfb > top_1 and vol > vol_ma * 1:
            txt = dt + "--" + symbol + "--现货5分钟-普通B-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_ordinary.send_text(msg=txt, is_at_all=False)
        elif bfb > top_2 and vol > vol_ma * 1:
            txt = dt + "--" + symbol + "--现货5分钟-普通A-买入--" + str(round(bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_ordinary.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_1 and vol > vol_ma * 3:
            txt = dt + "--" + symbol + "--现货5分钟-天量B-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_top.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_2 and vol > vol_ma * 3:
            txt = dt + "--" + symbol + "--现货5分钟-天量A-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_top.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_1 and vol > vol_ma * 2:
            txt = dt + "--" + symbol + "--现货5分钟-超级B-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_super.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_2 and vol > vol_ma * 2:
            txt = dt + "--" + symbol + "--现货5分钟-超级A-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_super.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_1 and vol > vol_ma * 1:
            txt = dt + "--" + symbol + "--现货5分钟-普通B-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_ordinary.send_text(msg=txt, is_at_all=False)
        elif bfb < bottom_2 and vol > vol_ma * 1:
            txt = dt + "--" + symbol + "--现货5分钟-普通A-卖出--" + str(round(100-bfb)) + "，流通比：" + str(
                round(circulating_supply_bfb, 3))
            xiaoding_5m_ordinary.send_text(msg=txt, is_at_all=False)
        else:
            print(symbol + "--Not established")


def main():
    print("开始运行")
    schedule.every().hour.at(":05").do(vol_sx)
    schedule.every().hour.at(":10").do(vol_sx)
    schedule.every().hour.at(":15").do(vol_sx)
    schedule.every().hour.at(":20").do(vol_sx)
    schedule.every().hour.at(":25").do(vol_sx)
    schedule.every().hour.at(":30").do(vol_sx)
    schedule.every().hour.at(":35").do(vol_sx)
    schedule.every().hour.at(":40").do(vol_sx)
    schedule.every().hour.at(":45").do(vol_sx)
    schedule.every().hour.at(":50").do(vol_sx)
    schedule.every().hour.at(":55").do(vol_sx)
    schedule.every().hour.at(":00").do(vol_sx)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
