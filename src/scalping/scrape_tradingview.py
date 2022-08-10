import requests
import urllib
import time
from tqdm import tqdm
import asyncio

from tradingview_ta import TA_Handler, Interval, Exchange

import bybit_buy_sell as bbs

intervals = [Interval.INTERVAL_15_MINUTES, 
    Interval.INTERVAL_30_MINUTES, 
    Interval.INTERVAL_1_HOUR,
    Interval.INTERVAL_2_HOURS,
    Interval.INTERVAL_4_HOURS,
    Interval.INTERVAL_1_DAY,]

async def get_info(coin):

    buys, sells, neutrals = 0, 0, 0

    for interval in intervals:

        coin_handler = TA_Handler(
            symbol=coin.upper(),
            screener="crypto",
            exchange="bybit",
            interval=interval
        )


        summary = coin_handler.get_analysis().summary

        buys += summary['BUY']
        sells += summary['SELL']
        neutrals += summary['NEUTRAL']


    rec_15min_handler = coin_handler = TA_Handler(
        symbol=coin.upper(),
        screener="crypto",
        exchange="bybit",
        interval=Interval.INTERVAL_15_MINUTES
    )
    rec_30min_handler = coin_handler = TA_Handler(
        symbol=coin.upper(),
        screener="crypto",
        exchange="bybit",
        interval=Interval.INTERVAL_30_MINUTES
    )

    summary_15min = rec_15min_handler.get_analysis().summary
    summary_30min = rec_30min_handler.get_analysis().summary

    buy_now = False
    if summary_15min['BUY'] > summary_15min['SELL'] + summary_15min['NEUTRAL'] or summary_30min['BUY'] > summary_30min['SELL'] + summary_30min['NEUTRAL']:
        buy_now = True


    not_exploded = await bbs.check_coin_lower_part_day(coin.split('USDT')[0])

    if buys > (sells + neutrals) and buy_now:

        return True, buys

    else:
        return False, 0


async def scan_market():

    good_coin_list = ['IMX', 'ZEN', 'SC', 'STX', 'BICO', '1INCH', 'KLAY', 'SPELL', 'AR', 'ICX', 'CELO', 'WAVES', 'RVN', 'LOOKS', 'JASMY', 'HNT', 'ZIL', 'SUN', 'JST', 'PAXG', 'KDA', 'APE', 'GMT', 'HOT', 'DGB', 'ZRX', 'GLMR', 'SCRT', 'MINA', 'BOBA', 'ACH', 'GAL', 'OP', 'BEL', 'EOS', 'XRP', 'DOT', 'BIT', 'ADA', 'SOL', 'MANA', 'LTC', 'BTC', 'ETH', 'EOS', 'XRP', 'BCH', 'XTZ', 'LINK', 'ADA', 'UNI', 'XEM', 'SUSHI', 'AAVE', 'DOGE', 'MATIC', 'ETC', 'BNB', 'FIL', 'XLM', 'TRX', 'THETA', 'AXS', 'SAND', 'KSM', 'ATOM', 'CHZ', 'CRV', 'ENJ', 'YFI', 'ICP', 'FTM', 'ALGO', 'DYDX', 'NEAR', 'SRM', 'OMG', 'FTT', 'BIT', 'GALA', 'HBAR', 'ONE', 'C98', 'AGLD', 'MKR', 'EGLD', 'REN', 'TLM', 'RUNE', 'WOO', 'LRC', 'ENS', 'BAT', 'SNX', 'SLP', 'ANKR', 'QTUM']


    best_coins_list = []
    best_coin, best_buys = None, -99999
    coins_with_issues = 0
    for coin in tqdm(good_coin_list):

        try:
            rec, buys = await get_info(coin+"USDT")
        except:
            print(f"Problem with {coin}")
            coins_with_issues += 1
            continue

        if rec:
            if buys > best_buys:
                best_coins_list.append((coin, buys))
                best_coin = coin
                best_buys = buys

    print(best_coins_list)
    print(f"Coins with issues: {coins_with_issues}")
    return best_coin, best_buys



async def main():

    print(await scan_market())


if __name__ == '__main__':
    asyncio.run(main())
