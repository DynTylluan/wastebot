from collections import namedtuple
from datetime import datetime
from os import environ
import asyncio
import discord
import re

client = discord.Client()

trailhead = discord.Game("%help", start=datetime(1970, 1, 1, 0, 0, 0))

Command = namedtuple("Command", ["name", "desc", "usage", "regex", "action"])

commands = {}

# HELP

help_commands = ("help", "hello", "roles", "enrole", "derole", "color", "bleach")

async def help_action(msg, invoc):
	name = invoc[1]
	if name:
		if name in commands:
			await msg.channel.send("`%{0.name}`: {0.desc} Usage: `{0.usage}`.".format(commands[name]))
		else:
			await msg.channel.send("`uhh, %{}` isn’t even a command. for more information, type `%help`.".format(name))
	else:
		await msg.channel.send("Commands: {}".format(", ".join(map("`{}`".format, help_commands))))

commands["help"] = Command("help", "prompts the bot to list commands or describe the specified command.", "%help [%<command name>]", re.compile("\s*%help(?:\s+%([a-z-]+))?\s*$"), help_action)

# HELLO

async def hello_action(msg, invoc):
	await msg.channel.send("Hello, {0.display_name}.".format(msg.author))

commands["hello"] = Command("hello", "prompts the bot to greet the commander.", "%hello", re.compile("\s*%hello\s*$"), hello_action)

# TODO: ROLES
# TODO: COLOR

# MAIN SHIT

@client.event
async def on_ready():
  await client.change_presence(activity=trailhead)

@client.event
async def on_message(msg):
	if msg.author == client.user:
		return

	match = re.match("\s*%([a-z-]+)(?:\s+|$)", msg.content)
	if match:
		comm = commands.get(match[1])
		if comm:
			invoc = comm.regex.match(msg.content)
			if invoc:
				await comm.action(msg, invoc)
			else:
				await msg.channel.send("uhh, that’s not how you use `%{0.name}`. Usage: `{0.usage}`. for more information, type `%help %{0.name}`.".format(comm))
		else:
			await msg.channel.send("uhh, `%{}` isn’t even a command. for more information, type `%help`.".format(match[1]))

if ("TOKEN" in environ):
	client.run(environ["TOKEN"])