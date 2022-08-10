import krakenex
from pykrakenapi import KrakenAPI
api = krakenex.API()
kraken = KrakenAPI(api)

api.load_key('KrakenPass.txt')


TRX = float((kraken.get_ticker_information('TRXUSD'))['a'][0][0])

response = kraken.add_standard_order(pair='TRXUSD', type='buy', ordertype='limit', 
                                     volume='20', price=TRX-0.005, validate=False, timeinforce=None, trigger=None)
print(response)


sleep(3)

check_order = kraken.query_orders_info(response['txid'][0])

if check_order['status'][0] == 'open' or 'closed':
    print('Order completed sucessfully')
    break
else:
    print('Order rejected')
    break