from .API_Elements import *

class Events:
	def __init__(self):

		@self.def_event("READY","on_ready")
		class Event(Bot_Element):

			def __init__(self, bot, data):
				Bot_Element.__init__(self,data,bot)
				self.version = data["v"]

				for x,y in self.__dict__.items():
					setattr(bot,x,y)

		@self.def_event("GUILD_CREATE","guild_create")
		class Event(Guild):

			def __init__(self, bot, data):
				Guild.__init__(self, data, bot)

				guild = bot.get_element(bot.guilds,self.id)
				if guild:
					for x,y in self.__dict__.items():
						setattr(guild,x,y)
				else:
					bot.guilds.append(self)

		@self.def_event("GUILD_UPDATE","guild_update")
		class Event(Guild):

			def __init__(self, bot, data):
				Guild.__init__(self, data, bot)

				guild = bot.get_element(bot.guilds,self.id)
				for x,y in self.__dict__.items():
					if y:
						setattr(guild,x,y)

		@self.def_event("GUILD_DELETE","guild_delete")
		class Event:

			def __init__(self, bot, data):
				self.id = data["id"]
				self.unavailable = data.get("unavailable")

		@self.def_event("MESSAGE_CREATE","on_message")
		class Event(Message):

			def __init__(self, bot, data):
				Message.__init__(self, data, bot)

		@self.def_event("MESSAGE_UPDATE","message_update")
		class Event(Message):

			def __init__(self, bot, data):
				Message.__init__(self, data, bot)

		@self.def_event("MESSAGE_DELETE","message_delete")
		class Event(Message):

			def __init__(self, bot, data):
				Message.__init__(self, data, bot)

		@self.def_event("MESSAGE_DELETE_BULK", "message_bulk")
		class Event:

			def __init__(self, bot, data):
				self.ids = data["ids"]
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id")

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				if self.guild:
					self.channel = bot.get_element(self.guilds.channels, self.channel_id)
				else:
					self.channel = bot.get_element(self.private_channels, self.channel_id)

		@self.def_event("MESSAGE_REACTION_ADD","reaction_add")
		class Event(Member):

			def __init__(self,bot,data):
				if "member" in data:
					Member.__init__(self,{**data["member"],"guild_id":data["guild_id"]},bot)
				self.emoji = Emoji(data["emoji"])
				self.user_id = data["user_id"]
				self.channel_id = data["channel_id"]
				self.message_id = data["message_id"]
				self.__bot = bot

			@property
			@Cache
			def message(self):
				return Message(self.__bot.api(f"/channels/{self.channel_id}/messages/{self.message_id}"),self.__bot)

			def delete(self):
				if self.id == self.__bot.user.id:
					self.message.delete_self_reaction(self.emoji.name)
				else:
					self.message.delete_reaction(self.emoji.name,user_id=self.id)

		@self.def_event("MESSAGE_REACTION_REMOVE","reaction_remove")
		class Event:

			def __init__(self, bot, data):
				self.user_id = data["user_id"]
				self.channel_id = data["channel_id"]
				self.message_id = data["message_id"]
				self.guild_id = data.get("guild_id")
				self.emoji = Emoji(data["emoji"])
				self.__bot = bot

			@property
			@Cache
			def message(self):
				return Message(self.__bot.api(f"/channels/{self.channel_id}/messages/{self.message_id}"),self.__bot)

		@self.def_event("CHANNEL_PINS_UPDATE","pin_update")
		class Event:

			def __init__(self, bot, data):
				self.channel_id = data["channel_id"]
				self.last_pin_timestamp = data.get("last_pin_timestamp")
				self.guild_id = data.get("guild_id")

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				if self.guild:
					self.channel = bot.get_element(self.guilds.channels, self.channel_id)
				else:
					self.channel = bot.get_element(self.private_channels, self.channel_id)

		@self.def_event("CHANNEL_CREATE","channel_create")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				if self.type == 1:
					if bot.get_element(bot.private_channels, self.id):
						bot.set_element(bot.private_channels, self)
					else:
						bot.private_channels.append(self)
				else:
					self.guild.channels.append(self)

		@self.def_event("CHANNEL_UPDATE","channel_update")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				bot.set_element(self.guild.channels, self)

		@self.def_event("CHANNEL_DELETE","channel_delete")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				self.guild.channels.remove(bot.get_element(self.guild.channels, self.id))

		@self.def_event("GUILD_MEMBER_ADD","member_join")
		class Event(Member):

			def __init__(self, bot, data):
				Member.__init__(self,data,bot)

				self.guild.members.append(self)

		@self.def_event("GUILD_MEMBER_UPDATE","member_update")
		class Event(Member):

			def __init__(self, bot, data):
				Member.__init__(self,data,bot)

				bot.set_element(self.guild.members,self)

		@self.def_event("GUILD_MEMBER_REMOVE","member_quit")
		class Event(User):

			def __init__(self, bot, data):
				User.__init__(self,data["user"],bot)
				self.guild_id = data["guild_id"]

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				self.guild.members.remove(bot.get_element(self.guild.members, self.id))

		@self.def_event("GUILD_ROLE_CREATE","role_create")
		class Event(Role):

			def __init__(self, bot, data):
				Role.__init__(self, {**data["role"],"guild_id":data["guild_id"]}, bot)

				self.guild.roles.append(self)

		@self.def_event("GUILD_ROLE_UPDATE","role_update")
		class Event(Role):
			def __init__(self, bot, data):
				Role.__init__(self, {**data["role"],"guild_id":data["guild_id"]}, bot)

				bot.set_element(self.guild.roles,self)

		@self.def_event("GUILD_ROLE_DELETE","role_delete")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				self.id = data["role_id"]

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				role = bot.get_element(self.guild.roles, self.id)
				for x,y in role.__dict__.items():
					setattr(self,x,y)
				self.guild.roles.remove(role)

		@self.def_event("INVITE_CREATE","invite_create")
		class Event(Invite):

			def __init__(self, bot, data):
				Invite.__init__(self, data, bot)
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				self.channel = bot.get_element(self.guild.channels, self.channel_id)
				self.channel.invites.append(self)

		@self.def_event("INVITE_DELETE","invite_delete")
		class Event(Invite):

			def __init__(self, bot, data):
				Invite.__init__(self, data, bot)
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				self.channel = bot.get_element(self.guild.channels, self.channel_id)
				for invite in channel.invites:
					if invite.code == self.code:
						for x,y in invite.__dict__.items():
							setattr(self,x,y)
						self.channel.invites.remove(invite)
						break

		@self.def_event("GUILD_BAN_ADD", "add_ban")
		class Event(Ban):

			def __init__(self, bot, data):
				Ban.__init__(self, data, bot)
				self.guild_id = data["guild_id"]

				guild = bot.get_element(bot.guilds, self.guild_id)

		@self.def_event("GUILD_BAN_REMOVE", "remove_ban")
		class Event(Ban):

			def __init__(self, bot, data):
				Ban.__init__(self, data, bot)
				self.guild_id = data["guild_id"]

				guild = bot.get_element(bot.guilds, self.guild_id)

		@self.def_event("GUILD_EMOJIS_UPDATE", "emojis_update")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				self.emojis = [Emoji(emoji) for emoji in data["emojis"]]

				self.guild = bot.get_element(bot.guilds, self.guild_id)

		@self.def_event("GUILD_INTEGRATIONS_UPDATE", "integration_update")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]

				self.guild = bot.get_element(bot.guilds, self.guild_id)

		@self.def_event("WEBHOOKS_UPDATE", "webhook_update")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				self.channel_id = data["channel_id"]

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				self.channel = bot.get_element(self.guild.channels, self.channel_id)

		@self.def_event("TYPING_START", "typing")
		class Event:

			def __init__(self, bot, data):
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id")
				self.user_id = data["user_id"]
				self.timestamp = data["timestamp"]
				if "member" in data:
					self.member = Member(data["member"],bot)

				self.guild = bot.get_element(bot.guilds, self.guild_id)
				if self.guild:
					self.channel = bot.get_element(self.guild.channels, self.channel_id)
				else:
					self.channel = bot.get_element(self.private_channels, self.channel_id)

'''
		@self.def_event("VOICE_STATE_UPDATE","")
		class Event:

			def __init__(self, bot, data):
				self.voice = bot.voices.get(data["guild_id"])
				self.member = Member(data["member"],bot)
				self.session_id = data.get("session_id")
				self.__bot = bot

			async def run(self):
				if self.member.id == self.__bot.user.id:
					if self.voice:
						if not self.voice.session_id:
							self.voice.session_id = self.session_id
							self.voice.state += 1
							if self.voice.state == 2:
								await self.voice.run()

		@self.def_event("VOICE_SERVER_UPDATE","")
		class Event:

			def __init__(self, bot, data):
				self.voice = bot.voices[data["guild_id"]]
				self.token = data["token"]
				self.endpoint = data["endpoint"]

			async def run(self):
				if not self.voice.token:
					self.voice.token = self.token
					self.voice.endpoint = self.endpoint.replace(":80","")
					self.voice.state += 1
					if self.voice.state == 2:
						await self.voice.run()
'''

		