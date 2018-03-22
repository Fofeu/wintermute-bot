import discord
from secrets import key
from utils import *
import logging
from botgram import BotGram
from parseresult import *
from concurrent.futures import TimeoutError
from pebble import ProcessPool

if __name__ =='__main__':

	channels = {"comput" : ("Comput Yourself", "botchannel")}
	bot_prelude = '[bot] '
	timeoutt = 10

	logging.basicConfig(level=logging.INFO)

	client = discord.Client()

	bot_parser = BotGram(client)

	pool = ProcessPool()

	@client.event
	async def on_ready():
		global channels
		logging.info("Online as " + str(client.user.name))
		for s in client.servers:
			if s.name == channels["comput"][0]:
				#s.me.game = discord.Game(name="Manipulating humanity")
				for c in s.channels:
					if c.name == channels["comput"][1]:
						logging.info("found #botchannel on comput")
						channels["comput"] = s,c
		logging.info('Setup done')

	@client.event
	async def on_member_update(before, after):
		tasks = []

		for t in tasks:
			await t

	@client.event
	async def on_message(mess):
		global pool
		tasks = []

		if mess.channel.is_private:
			logging.info("new private message from " + str(mess.author))
		else:
			logging.info("new message on server " + str(mess.server) + " and channel " + str(mess.channel) + " from " + str(mess.author))
		logging.info("len: " + str(len(mess.content)))
		logging.info("content: " + str(mess.content))

		if mess.channel.permissions_for(mess.channel.server.me).send_messages:
			resp = bot_parser.parse(mess)
			if resp is not None:
				tasks.append(pool.schedule(composemess, args=((mess.channel, bot_prelude + mess.author.mention + ' ', resp),), timeout=timeoutt))

		for t in tasks:
			try:
				x = t.result()
				channel = x[0]
				response = x[1]
				await client.send_message(channel, response)
			except TimeoutError:
				t.cancel()
				pass



	client.run(key)
