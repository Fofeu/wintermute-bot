import discord
import logging
from botgram import BotGram
from pebble import ProcessPool
import asyncio
from concurrent.futures import TimeoutError
from discord.errors import HTTPException

class Wintermute(discord.Client):
	__channels = None
	__bot_prelude = None
	__timeout = None
	__loop = None
	__parser = None
	__pool = None

	def __init__(self,
		channels = {},
		bot_prelude = '[bot] ',
		timeout = 10,
		multiprocessing = 1,
		loglevel = logging.INFO,
		async_loop = None):
		super().__init__()

		self.__channels = channels
		self.__bot_prelude = bot_prelude
		self.__timeout = timeout
		logging.basicConfig(level=loglevel)
		if async_loop is not None:
			self.__loop = async_loop
		else:
			self.__loop = asyncio.get_event_loop()

		self.__parser = BotGram()
		self.__pool = ProcessPool(max_workers=multiprocessing)

	def __del__(self):
		self.__pool.close()
		self.__pool.join()
		if self.__loop.is_running():
			self.__loop.stop()
		self.__loop.run_until_complete(self.__loop.shutdown_asyncgens())
		self.__loop.close()

	def launch(self, key):
		try:
			self.__loop.run_until_complete(self.start(key))
		except:
			self.__loop.run_until_complete(self.logout())
		finally:
			self.__loop.close()

	async def on_ready(self):
		logging.info("Online as " + str(self.user.name))
		tmpchannels = {}
		for s in self.servers:
			if s.name in self.__channels:
				channel = self.__channels[s.name]
				for c in s.channels:
					if c.name == channel:
						logging.info("found #" + channel + " on " + s.name)
						tmpchannels["s.name"] = c.name
		logging.info('Setup done')

	async def on_message(self, mess):
		if mess.channel.is_private:
			logging.info("new private message from " + str(mess.author))
		else:
			logging.info("new message on server " + str(mess.server) + " and channel " + str(mess.channel) + " from " + str(mess.author))
		logging.info("len: " + str(len(mess.content)))
		logging.info("content: " + str(mess.content))
		if mess.channel.is_private:
			return

		if (mess.channel.permissions_for(mess.channel.server.me).send_messages
			and mess.channel.name == self.__channels[mess.server.name]):
			resp = self.__parser.parse(mess)
			if resp is not None:
				task = self.__pool.schedule(
					str,
					args=(resp,),
					timeout=self.__timeout)
				asyncio.ensure_future(self.collect_response(mess.channel, mess.author.mention, task))

	async def collect_response(self, channel, mention, task):
		try:
			while not task.done():
				await asyncio.sleep(0.1)
			result = task.result()
			await self.send_message(channel,
				self.__bot_prelude + mention + ' ' + result)
		except TimeoutError:
			await self.send_message(channel,
				self.__bot_prelude + mention + ' Your request timed out')
			task.cancel()
		except HTTPException as e:
			if e.response.status == 400:
				await self.send_message(channel,
				self.__bot_prelude + mention + ' Error: Request reply was probably too long')

