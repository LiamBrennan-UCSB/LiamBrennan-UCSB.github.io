import pandas as pd
import urllib.request
import numpy as np

base_url = "https://swingtradebot.com/equities?min_vol=250000&min_price={min}&max_price={max}&adx_trend=&grade=&include_etfs=0&html_button=as_html&page={page}"

## test url generator ##
minimum = 0
maximum = 5
page = 3
print(base_url.format(min=minimum, max=maximum, page=page))

minimum = 5
maximum = 10
page = 10
print(base_url.format(min=minimum, max=maximum, page=page))


## extract symbols ##
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

symbols = []

MIN = 0
MAX = 5
for page in range(1, 30):

    url = base_url.format(min=MIN, max=MAX, page=page)
    print(url)
    req = urllib.request.Request(url=url, headers=header)
    page = urllib.request.urlopen(req).read()
    table = pd.read_html(page)

    print(table[0].Symbol)

    symbols.append([sym for sym in table[0].Symbol])

print(symbols)

symbols_flat = flat_list = list(np.concatenate(symbols).flat)

with open("all_symbols_under5.txt", "w") as o_f:
    for symbol in symbols_flat:
        o_f.write(symbol + "\n")
