#Testing each coin to see if it is in spot trading
#https://www.bybit.com/en-US/trade/spot/BTC/USDT

import webbrowser
from selenium import webdriver
driver = webdriver.Chrome()


with open(f"Coins_part0.txt", "r") as cf:
    lines = cf.readlines()

Total_coin_list = [line.replace("\n", "") for line in lines]
print(Total_coin_list)

coin_list_amount = len(Total_coin_list)
print('There are:', coin_list_amount, 'Coins')

coinlist = []
coinbad = []

for coin in Total_coin_list:
	link = 'https://www.bybit.com/en-US/trade/spot/' + coin + '/USDT'
	driver.get(link)
	print(driver.current_url)
	if driver.current_url == link:
		coinlist.append(coin)
	else:
		print("This coin is bad: ", coin)
		coinbad.append(coin)

print("These coins work:", coinlist)

Good_coin_Amount = len(coinlist)
Bad_coin_amount = len(coinbad)

print("There are: ", Good_coin_Amount, "Coins")

print("These coins don't work:", coinbad)

print("There are: ", Bad_coin_amount, "Coins")

driver.quit()



