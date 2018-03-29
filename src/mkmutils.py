from mkmsdk.mkm import mkm

MTG_ID = 1
EN_ID = 1
FR_ID = 2
DE_ID = 3

def get_prices(card_name, lang):
	result = []
	for x in mkm.market_place.products(name=card_name, game=MTG_ID, language=lang, match="false").json()["product"]:
		if (x['category']['idCategory'] == 1):
			result.append({'expansion': x['expansion'], 'number': x['number'], 'priceGuide': x['priceGuide']})
	return result
	

if __name__ == '__main__':
	for x in get_prices('Hazoret', 1):
		print(x)
	print()
	for x in get_prices('Kitchen Fin', 1):
		print(x)
