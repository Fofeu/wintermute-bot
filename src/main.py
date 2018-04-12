from secrets import key
from wintermute import Wintermute

if __name__ =='__main__':

	channels = {"Comput Yourself": "botchannel"}

	client = Wintermute(
		channels = channels,
		bot_prelude = '[bot] ',
		timeout = 30,
		multiprocessing = 4
	)

	client.launch(key)
