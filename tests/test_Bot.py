from .imports import Bot

from unittest.mock import Mock,patch
import pytest
import json
import pathlib


root = pathlib.Path(__file__).resolve().parent
with root.joinpath("calls.json").open() as f1, \
     root.joinpath("responses.json").open() as f2:
	calls = json.load(f1)
	responses = json.load(f2)

async def api_call(path, method="GET", **kwargs):
	return responses[f"{path} {method}"]

Bot.api_call = Mock()
Bot.api_call.side_effect = api_call

@pytest.fixture()
def bot_ready():
	bot = Bot("")
	bot.events_list["READY"][1](bot,calls["READY"])
	return bot

@pytest.fixture()
def bot_guilds(bot_ready):
	bot = bot_ready
	bot.events_list["GUILD_CREATE"][1](bot,calls["GUILD_CREATE"])
	return bot

@pytest.fixture()
def bot_message(bot_guilds):
	bot = bot_guilds
	message = bot.events_list["MESSAGE_CREATE"][1](bot,calls["MESSAGE_CREATE"])
	return bot, message

def test_ready_bot(bot_ready):
	assert bot_ready.user.name == "Piscord Unittest"
	assert bot_ready.user.id == "715274051374940202"

def test_ready_guild(bot_ready):
	assert len(bot_ready.guilds) == 1
	guild = bot_ready.guilds[0]
	assert guild.id == "715273516555174009"
	assert guild.unavailable
	assert guild.channels == []
	assert guild.members == []
	assert not guild.name

def test_guilds_attribs(bot_guilds):
	bot = bot_guilds
	assert len(bot.guilds) == 1
	guild = bot.guilds[0]

	assert guild.id == "715273516555174009"
	assert not guild.unavailable
	assert len(guild.channels) == 4
	assert len(guild.members) == guild.member_count
	assert guild.name == "Piscord_Unittest"

def test_guilds_funcs(bot_guilds):
	bot = bot_guilds
	guild = bot.guilds[0]

	channel = guild.create_channel(name="test")
	role = guild.create_role(name="neko")

	assert channel.name == "test"
	assert channel.id == "715364724769816656"

	assert role.name == "neko"
	assert role.permissions == 104320577
	assert role.id == "715370573575749724"

	assert channel.guild == guild
	assert role.guild == guild

def test_message_send(bot_message):
	bot, message = bot_message

	assert message.id == "715958368191381604"
	assert message.author.id == "263331548542009348"
	assert message.channel == bot.get_element(bot.guilds[0].channels,id="715273516555174012")
	assert message.guild == bot.guilds[0]
	assert message.mentions
	assert message.mentions[0].id == bot.user.id
	assert bot.get_element(message.guild.members,id=bot.user.id)

def test_channel_attribs(bot_guilds):
	bot = bot_guilds
	guild = bot.guilds[0]
	channel = guild.channels[0]

	assert channel.name == "Salons textuels"
	assert channel.type == 4
	assert channel.id == "715273516555174010"
	assert channel.guild == guild
	assert channel.nsfw == None
