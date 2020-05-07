import asyncio
from .API_Elements import *

class Events:
	def __init__(self):
		
		@self.def_event("MESSAGE_CREATE","on_message")
		class Event(Message):

			def __init__(self, bot, data):
				Message.__init__(self, data, bot)

		@self.def_event("READY","on_ready")
		class Event(User):

			def __init__(self, bot, data):
				self.version = data["v"]
				User.__init__(self, data["user"],bot)

		@self.def_event("MESSAGE_REACTION_ADD","reaction_add")
		class Event(Member):

			def __init__(self,bot,data):
				Member.__init__(self,{**data["member"],"guild_id":data["guild_id"]},bot)
				self.emoji = Emoji(data["emoji"])
				self.channel_id = data["channel_id"]
				self.message_id = data["message_id"]
				self.__bot = bot

			def get_message(self):
				return Message(asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.message_id}")),self.__bot)

			def delete(self):
				if self.id == self.__bot.get_self_user().id:
					self.get_message().delete_self_reaction(self.emoji.name)
				else:
					self.get_message().delete_reaction(self.emoji.name,user_id=self.id)

		@self.def_event("MESSAGE_REACTION_REMOVE","reaction_remove")
		class Event:

			def __init__(self, bot, data):
				self.user_id = data["user_id"]
				self.channel_id = data["channel_id"]
				self.message_id = data["message_id"]
				self.guild_id = data["guild_id"]
				self.emoji = Emoji(data["emoji"])
				self.__bot = bot

			def get_message(self):
				return Message(asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.message_id}")),self.__bot)

		@self.def_event("CHANNEL_CREATE","channel_create")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

		@self.def_event("CHANNEL_DELETE","channel_delete")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

		@self.def_event("CHANNEL_UPDATE","channel_update")
		class Event(Channel):

			def __init__(self, bot, data):
				Channel.__init__(self, data, bot)

		@self.def_event("GUILD_MEMBER_ADD","member_join")
		class Event(Member):

			def __init__(self, bot, data):
				Member.__init__(self,data,bot)

		@self.def_event("GUILD_MEMBER_REMOVE","member_quit")
		class Event(User):

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				User.__init__(self,data["user"],bot)

		@self.def_event("GUILD_ROLE_CREATE","role_create")
		class Event(Role):

			def __init__(self, bot, data):
				Role.__init__(self, data, bot)

		@self.def_event("GUILD_ROLE_DELETE","role_delete")
		class Event:

			def __init__(self, bot, data):
				self.guild_id = data["guild_id"]
				self.role_id = data["role_id"]

		@self.def_event("INVITE_CREATE","invite_create")
		class Event(Invite):

			def __init__(self, bot, data):
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)
				Invite.__init__(self, data, bot)

		@self.def_event("INVITE_DELETE","invite_delete")
		class Event:

			def __init__(self, bot, data):
				self.code = data["code"]
				self.channel_id = data["channel_id"]
				self.guild_id = data.get("guild_id",None)