from .API_Elements import *
from time import time

class Events:
	def __init__(self):

		@self.def_event("GUILD_CREATE","guild_create")
		class Event(Guild):

			def __init__(self, bot, data):
				Guild.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.id:
						for x,y in self.__dict__.items():
							setattr(guild,x,y)

		@self.def_event("MESSAGE_CREATE","on_message")
		class Event(Message):

			def __init__(self, bot, data):
				Message.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								self.channel = channel
								break
						break

		@self.def_event("MESSAGE_UPDATE","message_update")
		class Event(Message):

			def __init__(self, data, bot):
				Message.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								self.channel = channel
								break
						break

		@self.def_event("MESSAGE_DELETE","message_delete")
		class Event(Message):

			def __init__(self, data, bot):
				Message.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								self.channel = channel
								break
						break

		@self.def_event("READY","on_ready")
		class Event(Bot_Element):

			def __init__(self, bot, data):
				Bot_Element.__init__(self,data,bot)
				self.version = data["v"]

				for x,y in self.__dict__.items():
					setattr(bot,x,y)

		@self.def_event("MESSAGE_REACTION_ADD","reaction_add")
		class Event(Member):

			def __init__(self,bot,data):
				Member.__init__(self,{**data["member"],"guild_id":data["guild_id"]},bot)
				self.emoji = Emoji(data["emoji"])
				self.channel_id = data["channel_id"]
				self.message_id = data["message_id"]
				self.__bot = bot

			@property
			@Cache
			def message(self):
				message = Message(self.__bot.api(f"/channels/{self.channel_id}/messages/{self.message_id}"),self.__bot)
				for guild in self.__bot.guilds:
					if guild.id == self.guild_id:
						message.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								message.channel = channel
								break
						break
				return message

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
				self.guild_id = data["guild_id"]
				self.emoji = Emoji(data["emoji"])
				self.__bot = bot

			@property
			@Cache
			def message(self):
				message = Message(self.__bot.api(f"/channels/{self.channel_id}/messages/{self.message_id}"),self.__bot)
				for guild in self.__bot.guilds:
					if guild.id == self.guild_id:
						message.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								message.channel = channel
								break
						break
				return message

		@self.def_event("CHANNEL_CREATE","channel_create")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						guild.channels.append(self)
						break

		@self.def_event("CHANNEL_UPDATE","channel_update")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for i in range(len(guild.channels)):
							if guild.channels[i].id == self.id:
								guild.channels[i] = self
								break
						break

		@self.def_event("CHANNEL_DELETE","channel_delete")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.id:
								guild.channels.remove(channel)
								break
						break

		@self.def_event("GUILD_MEMBER_ADD","member_join")
		class Event(Member):

			def __init__(self, bot, data):
				Member.__init__(self,data,bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						guild.members.append(self)
						break

		@self.def_event("GUILD_MEMBER_UPDATE","member_update")
		class Event(Member):
			def __init__(self, bot, data):
				Member.__init__(self,data,bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for i in range(len(guild.members)):
							if guild.members[i].id == self.id:
								guild.members[i] = self
								break
						break

		@self.def_event("GUILD_MEMBER_REMOVE","member_quit")
		class Event(User):

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				User.__init__(self,data["user"],bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for member in guild.members:
							if member.id == self.id:
								guild.members.remove(member)
								break
						break

		@self.def_event("GUILD_ROLE_CREATE","role_create")
		class Event(Role):

			def __init__(self, bot, data):
				Role.__init__(self, data["role"], bot)
				self.guild_id = data["guild_id"]

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						guild.roles.append(self)
						break

		@self.def_event("GUILD_ROLE_UPDATE","role_update")
		class Event(Role):
			def __init__(self, bot, data):
				Role.__init__(self, data["role"], bot)
				self.guild_id = data["guild_id"]

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for i in range(len(guild.roles)):
							if guild.roles[i].id == self.id:
								guild.roles[i] = self
								break
						break

		@self.def_event("GUILD_ROLE_DELETE","role_delete")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				self.id = data["role_id"]

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for role in guild.roles:
							if role.id == self.id:
								for x,y in role.__dict__.items():
									setattr(self,x,y)
								guild.roles.remove(role)
								break
						break

		@self.def_event("INVITE_CREATE","invite_create")
		class Event(Invite):

			def __init__(self, bot, data):
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)
				Invite.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								self.channel = channel
								channel.invites.append(self)
								break
						break

		@self.def_event("INVITE_DELETE","invite_delete")
		class Event(Invite):

			def __init__(self, bot, data):
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)
				Invite.__init__(self, data, bot)

				for guild in bot.guilds:
					if guild.id == self.guild_id:
						self.guild = guild
						for channel in guild.channels:
							if channel.id == self.channel_id:
								self.channel = channel
								for invite in channel.invites:
									if invite.code == self.code:
										for x,y in invite.__dict__.items():
											setattr(self,x,y)
										channel.invites.remove(invite)
										break
								break
						break