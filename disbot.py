import discord
from conn import key
from utils import *
from dicegram import DiceGram

channels = {"comput" : ("Comput Yourself", "botchannel")}

bot_prelude = '[bot] '

dice_parser = DiceGram()

register_regex("roll", "^!roll (.*)$")
register_regex("cdlamerde", "^!cdlamerde$")

client = discord.Client()

@client.event
async def on_ready():
	global channels
	print("is online as", client.user.name)
	for s in client.servers:
		if s.name == channels["comput"][0]:
			#s.me.game = discord.Game(name="Manipulating humanity")
			for c in s.channels:
				if c.name == channels["comput"][1]:
					print("found #botchannel")
					channels["comput"] = s,c
	return

@client.event
async def on_member_update(before, after):
	global channel
	tasks = []

	#tasks.append(client.send_message(channel, bot_prelude + "Wait what ?"))
	#if before.status != discord.Status.offline and after.status == discord.Status.offline:
		#print(after.nick, "went offline from server", after.server)
		#if after.server == channels["comput"][0]:
			#tasks.append(client.send_message(channels["comput"][1], bot_prelude + "Au revoir " + after.nick + " !"))

	for t in tasks:
		await t

@client.event
async def on_message(mess):
	tasks = []

	if mess.channel.is_private:
		print("new private message from", mess.author)
	else:
		print("new message on server", mess.server, "and channel", mess.channel, "from", mess.author)
	print("len:", len(mess.content))
	print("content:", mess.content)
	print()
	
	if limit_to(mess, channels["comput"]):
		if for_me(mess, "cdlamerde"):
			tasks.append(client.send_message(mess.channel, bot_prelude + "Oui, maîîître !"))
		elif for_me(mess, "roll"):
			text = match(mess, "roll")[0]
			roll = dice_parser.parse(text)
			if roll is not None:
				tasks.append(client.send_message(mess.channel, bot_prelude + mess.author.mention + " " + str(roll) + " = " + str(int(roll))))
			else:
				tasks.append(client.send_message(mess.channel, bot_prelude + mess.author.mention + "Could not parse: " + text))

	for t in tasks:
		await t

client.run(key)
