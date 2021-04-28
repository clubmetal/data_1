import time
import pyupbit
import datetime

access = "SKM1cEKLPpe7wlkcXbTdAjuwovuLP7dFrnSFDO4v"
secret = "i0VtJsB741RWUOjM7UCWGMG79gmrxvdcryuxhD7T"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes30", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes30", count=1)
    start_time = df.index[0]
    return start_time

def get_ma50(ticker):
    """50일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes30", count=50)
    ma50 = df['close'].rolling(15).mean().iloc[-1]
    return ma50

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes30", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma7(ticker):
    """7일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minutes30", count=7)
    ma7 = df['close'].rolling(7).mean().iloc[-1]
    return ma7

def get_avg_buy_price(ticker):
    """매수평균가 조회"""
    avg_buy_price = upbit.get_avg_buy_price()
    for b in avg_buy_price:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_avg_buy_price(ticker):
    """매수평균가 조회"""
    avg_buy_price = upbit.get_avg_buy_price()
    for b in avg_buy_price:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP")
        end_time = start_time + datetime.timedelta(days=30)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", 0.5)
            ma15 = get_ma15("KRW-XRP")
            ma7 = get_ma7("KRW-XRP")
            ma50 = get_ma50("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma15 < current_price and ma7 < current_price and ma7 > ma15 and ma7 > ma50:
                krw = get_balance("KRW")
                if krw > 5000 and krw > 500000:
                    upbit.buy_market_order("KRW-XRP", krw*0.2)
        else:
            avg_buy_price = get_avg_buy_price("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if avg_buy_price > 1:
                normal_price = current_price / avg_buy_price
                if 0.97 > normal_price:
                    xrp = get_balance("XRP")
                    if xrp > 5:
                        upbit.sell_market_order("KRW-XRP", xrp*0.9995)
                elif normal_price > 1.02:
                     ma15 = get_ma15("KRW-XRP")
                     ma7 = get_ma7("KRW-XRP")
                     if ma15 > ma7:
                        xrp = get_balance("XRP")
                        if xrp > 5:
                            upbit.sell_market_order("KRW-XRP", xrp*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)