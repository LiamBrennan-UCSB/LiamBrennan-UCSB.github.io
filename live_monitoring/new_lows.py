import os
import time
import pandas as pd
import urllib.request

import yagmail
import datetime

import numpy as np

#------------- communication protocol info -------------#
FROM_EMAIL = "stonkoclonk@gmail.com"
FROM_PASS = "9d2bk8PNseQtQsAs"
yag = yagmail.SMTP(FROM_EMAIL, FROM_PASS)

RECIPIENTS_EMAILS = [
    "3239079063@vtext.com",
    # "liamb7144@gmail.com"
]

coins = [
"BATUSD",
"LINKUSD",
"DOGEUSD" ,
# "GRTUSD",
"MATICUSD",
"SUSHIUSD" ,
"TRXUSD",
"UNIUSD"
]

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}



def get_price(coin):
    link = "https://www.marketwatch.com/investing/cryptocurrency/{0}/charts"
    req = urllib.request.Request(url=link.format(coin), headers=header)
    html = str(urllib.request.urlopen(req).read())
    with open("t.txt", "w") as f:
        f.write(html)

    splitstr_phrase ='''"price"'''
    price = float(html.split(splitstr_phrase)[1].split('''"p''')[0][2:-2].replace(',', ''))

    return price


def get_day_range(coin):

    link = f"https://finance.yahoo.com/quote/{coin.split('USD')[0]}-USD"
    req = urllib.request.Request(url=link, headers=header)
    html = str(urllib.request.urlopen(req).read())

    splitstr_phrase ='''data-test="DAYS_RANGE-value"'''

    target = html.split(splitstr_phrase)[1].split('<')[0].split(' - ')
    low = float(target[0][1:].replace(",", ""))
    high = float(target[1].replace(",", ""))

    return low, high

def get_current_time():
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")

    return current_time

def send_message(contents, subject='SENTRY', attachments=[]):

    contents.append("Current time: {0}".format(get_current_time()))

    for recipient in RECIPIENTS_EMAILS:
        yag.send(recipient, subject, contents)

while 1:
    for coin in coins:
        while 1:
            try:
                print(coin)
                low, high = get_day_range(coin)
                print(low, high)
                price = get_price(coin)

                if price < low:
                    print("Found new low. Sending alert.")
                    contents = []
                    contents.append(f"New low for {coin}. Previous low: {low}. New low: {price}.")
                    send_message(contents, subject='NEW LOW')
                break
            except urllib.error.HTTPError:
                print("Sleeping to fool Yahoo.")
                time.sleep(10)

    time.sleep(30)