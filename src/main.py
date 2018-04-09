import discord
from secrets import key
from utils import *
import logging
from botgram import BotGram
from parseresult import *
from concurrent.futures import TimeoutError
from pebble import ProcessPool
from wintermute import Wintermute

if __name__ =='__main__':

	channels = {"Comput Yourself": "botchannel"}

	client = Wintermute(
		channels = channels,
		bot_prelude = '[bot] ',
		timeout = 30
	)

	client.launch(key)
