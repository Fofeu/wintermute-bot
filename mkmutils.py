import mkmenv
from mkmsdk.mkm import mkm

MTG_ID = 1
EN_ID = 1
FR_ID = 2
DE_ID = 3

def get_prices(card_name, lang):
	result = []
	for x in mkm.market_place.products(name=card_name, game=MTG_ID, language=lang, match=True).json()["product"]:
		result.append({'expansion': x['expansion'], 'number': x['number'], 'priceGuide': x['priceGuide']})
	#print(response[0].keys())
	return result
	

if __name__ == '__main__':
	#s1 = input("Card name: ")
	#s2 = int(input("Lang (EN=1, FR=2, DE=3): "))
	
	for x in get_prices('Kitchen Finks', 1):
		print(x)
