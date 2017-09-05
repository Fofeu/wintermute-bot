import discord
from conn import key
from utils import *
import logging
from botgram import BotGram
from parseresult import *

channels = {"comput" : ("Comput Yourself", "botchannel")}

bot_prelude = '[bot] '

#dice_parser = DiceGram()

register_regex("roll", "^!roll (.*)$")
register_regex("rolldetail", "^!roll detail (.*)$")
register_regex("cdlamerde", "^!cdlamerde$")

logging.basicConfig(level=logging.INFO)

client = discord.Client()

bot_parser = BotGram(client)

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
	return

@client.event
async def on_member_update(before, after):
	tasks = []

	for t in tasks:
		await t

@client.event
async def on_message(mess):
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
			tasks.append(client.send_message(mess.channel, bot_prelude + mess.author.mention + ' ' + str(resp)))

	for t in tasks:
		await t

client.run(key)
