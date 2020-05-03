import asyncio
import json
import aiohttp
from threading import Thread

class Utility:

	def get_self_user(self):
		return User(asyncio.run(self.api_call("/users/@me", "GET")), self)

	def get_self_guilds(self):
		return [Guild(guild,self) for guild in asyncio.run(self.api_call("/users/@me/guilds", "GET"))]

	def send_message(self,channel,**kwargs):
		return Message(asyncio.run(self.api_call(f"/channels/{channel}/messages", "POST", json=kwargs)),self)

	def get_guild(self,guild_id):
		return Guild(asyncio.run(self.api_call(f"/guilds/{guild_id}","GET")),self)

	def get_channel(self,channel_id):
		return Channel(asyncio.run(self.api_call(f"/channels/{channel_id}","GET")),self)

	def get_user(self,user_id):
		return User(asyncio.run(self.api_call(f"/users/{user_id}")), self)

	def get_invite(self, invite_code):
		return Invite(asyncio.run(self.api_call(f"/invites/{invite_code}","GET", params={"with_counts":"true"})),self)

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

class Bot(Thread,Utility,Events):

	def __init__(self,token):
		self.events_list = {}
		Events.__init__(self)
		Thread.__init__(self)
		Utility.__init__(self)
		self.token=token
		self.api="https://discordapp.com/api"
		self.__last_sequence = ""
		self.events = {}

	def def_event(self,event,name):
		def add_event(function):
			self.events_list[event] = [name,function]
			def thing():...
			return thing
		return add_event

	def event(self,arg):
		def truc():...

		def add_event(function):
			self.events[arg]=function
			return truc

		if type(arg) == str:
			return add_event

		self.events[arg.__name__] = arg
		return truc

	async def api_call(self,path, method="GET", **kwargs):
		defaults = {
			"headers": {
				"Authorization": f"Bot {self.token}",
				"User-Agent": "Bot"
			}
		}
		kwargs = dict(defaults, **kwargs)
		async with aiohttp.ClientSession() as session:
			async with session.request(method, self.api+path,**kwargs) as response:
				try:
					assert 200 == response.status, response.reason
					return await response.json()
				except:...

	async def begin(self):
		response = await self.api_call("/gateway")
		await self.__main(response["url"])

	async def __main(self,url):
		events = self.events_list
		async with aiohttp.ClientSession() as session:
			async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
				async for msg in ws:
					data = json.loads(msg.data)

					if data["op"] == 10:
						asyncio.create_task(self.__heartbeat(ws,data["d"]["heartbeat_interval"]))
						await ws.send_json({
							"op": 2,
							"d": {
								"token": self.token,
								"properties": {},
								"compress": False,
								"large_threshold": 250
						}})
					elif data["op"] == 0:
						if data["t"] in events:
							event = events[data["t"]]
							if event[0] in self.events:
								x = Thread(target=self.events[event[0]],args=(event[1](self,data["d"]),))
								x.start()
						self.__last_sequence=data["s"]

	async def __heartbeat(self,ws, interval):
		while True:
			await asyncio.sleep(interval / 1000)
			await ws.send_json({"op": 1,"d": self.__last_sequence})

	def run(self):
		self.loop = asyncio.new_event_loop()
		try:
			self.loop.run_until_complete(self.begin())
		except RuntimeError:print("Bot éteint")

	def stop(self):
		try:
			self.loop.stop()
		except:...
		try:
			for x in asyncio.all_tasks():
				try:
					x.cancel()
				except:...
		except:...

class OAuth:

	def __init__(self, bot, secret, redirect_uri, scope):
		self.bot = bot
		self.secret = secret
		self.id = bot.get_self_user().id
		self.redirect_uri = redirect_uri
		self.scope = scope

	def get_url(self):
		return f"https://discordapp.com/api/oauth2/authorize?client_id={self.id}&redirect_uri={self.redirect_uri}&response_type=code&scope={'%20'.join(self.scope.split())}"

	def get_token(self, code):
		data = {
			"client_id": self.id,
			"client_secret": self.secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		return asyncio.run(self.bot.api_call("/oauth2/token","POST",data=data))

	def __request_token(self,token,url):
		headers = {
			"Authorization": f"Bearer {json.loads(token)['access_token']}"
		}

		return asyncio.run(self.bot.api_call(url,"GET",headers=headers))

	def get_user(self,token):
		if "identify" in self.scope:
			return User(self.__request_token(token,"/users/@me"),self.bot)
		return "Invalid Scope"

	def get_guilds(self,token):
		if "guilds" in self.scope:
			return [Guild(guild,self.bot) for guild in self.__request_token(token,"/users/@me/guilds")]
		return "Invalid Scope"

	def add_guild_member(self, token, guild_id, user_id):
		if "guilds.join" in self.scope:
			return Member({**self.bot.api_call(f"/guilds/{guild_id}/members/{user_id}","PUT",json=json.loads(token)["access_token"]),"guild_id":guild_id})
		return "Invalid Scope"

class API_Element:

	def to_json(self):
		output = {}
		for x,y in self.__dict__.items():
			if y:
				if type(y) == list:
					e=[]
					for p in y:
						if isinstance(p,API_Element):
							p = p.to_json()
						e += p
					y = e
				if isinstance(y,API_Element):
					y = y.to_json()
				output[x]=y
		return output

class Guild(API_Element):

	def __init__(self, guild, bot):
		self.id = guild["id"]
		self.name = guild["name"]
		self.__bot = bot

	def __repr__(self):
		return self.name

	def get_channels(self):
		channels = asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/channels"))
		return [Channel(channel,self.__bot) for channel in channels]

	def get_roles(self):
		roles = asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/roles"))
		return [Role(role,self.__bot) for role in roles]

	def get_invites(self):
		invites = asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/invites"))
		return [Invite(invite,self.__bot) for invite in invites]

	def get_members(self):
		members = asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/members")),self.__bot
		return [Member({**member,"guild_id":self.id},self.__bot) for member in members]

	def get_member(self,user_id):
		return Member({**asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/members/{user_id}")),"guild_id":self.id},self.__bot)

	def get_bans(self):
		bans = asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/bans")),self.__bot
		return [Ban(ban,self.__bot) for ban in bans]

	def get_ban(self, user_id):
		return Ban(asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/bans/{user_id}")),self.__bot)

	def create_channel(self,**kwargs):
		''' kwargs : https://discordapp.com/developers/docs/resources/guild#create-guild-channel '''
		return Channel(asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/channels", "POST", json=kwargs)),self.__bot)

	def create_role(self,**kwargs):
		''' kwargs : https://discordapp.com/developers/docs/resources/guild#create-guild-role '''
		return Role(asyncio.run(self.__bot.api_call(f"/guilds/{self.id}/roles", "POST", json=kwargs)),self.__bot)

class Channel(API_Element):

	def __init__(self,channel,bot):
		self.id = channel["id"]
		self.type = channel["type"]
		self.guild_id = channel.get("guild_id",None)
		self.position = channel.get("position",None)
		self.permission_overwrites = [Overwrite(overwrite,bot,self) for overwrite in channel.get("permission_overwrites",[])]
		self.name = channel.get("name",None)
		self.topic = channel.get("topic",None)
		self.nsfw = channel.get("nsfw",None)
		self.last_message_id = channel.get("last_message_id",None)
		self.bitrate = channel.get("bitrate",None)
		self.user_limit = channel.get("user_limit",None)
		self.rate_limit_per_user = channel.get("rate_limit_per_user",None)
		self.recipients = channel.get("recipients",None)
		if "recipients" in channel:
			self.recipients = [User(user,bot) for user in channel["recipients"]]
		self.icon = channel.get("icon",None)
		self.owner_id = channel.get("owner_id",None)
		self.application_id = channel.get("application_id",None)
		self.parent_id = channel.get("parent_id",None)
		self.last_pin_timestamp = channel.get("last_pin_timestamp",None)
		self.__bot = bot

	def __repr__(self):
		return self.name

	def edit(self,**modifs):
		asyncio.run(self.__bot.api_call(f"/channels/{self.id}","PATCH",json=modifs))

	def send(self,**kwargs):
		return Message(asyncio.run(self.__bot.api_call(f"/channels/{self.id}/messages", "POST", json=kwargs)),self.__bot)

	def get_messages(self):
		messages = asyncio.run(self.__bot.api_call(f"/channels/{self.id}/messages"))
		return [Message(message,self.__bot) for message in messages]

	def get_invites(self):
		invites = asyncio.run(self.__bot.api_call(f"/channels/{self.id}/invites"))
		return [Invite(invite,self.__bot) for invite in invites]

	def create_invite(self,**kwargs):
		return Invite(asyncio.run(self.__bot.api_call(f"/channels/{self.id}/invites","POST",json=kwargs)),self.__bot)

class Message(API_Element):

	def __init__(self, message, bot):
		self.id = message["id"]
		self.channel_id = message["channel_id"]
		self.guild_id = message.get("guild_id",None)
		self.author = User(message["author"],bot)
		if "member" in message:
			self.author = Member({**message["member"],"user":{**message["author"]},"guild_id":self.guild_id}, bot)
		self.content = message["content"]
		self.timestamp = message["timestamp"]
		self.edited_timestamp = message.get("edited_timestamp",None)
		self.tts = message["tts"]
		self.mention_everyone = message["mention_everyone"]
		self.mentions = [User(mention,bot) for mention in message["mentions"]]
		self.mentions_roles = message["mention_roles"]
		self.mention_channels = []
		if "mention_channels" in message:
			self.mention_channels = [Channel(channel,bot) for channel in message["mention_channels"]]
		self.attachments = [Attachment(attachment) for attachment in message["attachments"]]
		self.embeds = [Embed(embed) for embed in message["embeds"]]
		self.reactions = []
		if "reactions" in message:
			self.reactions = [Reaction(reaction,self) for reaction in message["reactions"]]
		self.nonce = message.get("nonce",None)
		self.pinned = message["pinned"]
		self.webhook_id = message.get("webhook_id",None)
		self.type = message["type"]
		self.activity = message.get("activity",None) # Object
		self.application = message.get("application",None) #Object
		self.message_reference = message.get("message_reference",None) #Object
		self.flags = message.get("flags",None)
		self.__bot = bot

	def __repr__(self):
		return self.content

	def delete(self):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}","DELETE"))

	def edit(self,**modifs):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}","PATCH",json=modifs))

	def add_reaction(self, reaction):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","PUT"))

	def delete_reactions(self):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}/reactions","DELETE"))

	def delete_self_reaction(self, reaction):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","DELETE"))

	def delete_reaction(self,reaction,user_id=None):
		if user_id:
			asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/{user_id}","DELETE"))
		else:
			asyncio.run(self.__bot.api_call(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}","DELETE"))


class User(API_Element):

	def __init__(self, user, bot):
		self.system = user.get("system",None)
		self.mfa_enabled = user.get("mfa_enabled",None)
		self.locale = user.get("locale",None)
		self.verified = user.get("verified",None)
		self.email = user.get("email",None)
		self.flags = user.get("flags",None)
		self.premium_type = user.get("premium_type",None)
		self.public_flags = user.get("public_flags",None)
		self.id = user["id"]
		self.name = user["username"]
		self.discriminator = user["discriminator"]
		self.avatar = None
		if user["avatar"]:
			self.avatar = f"https://cdn.discordapp.com/avatars/{self.id}/{user['avatar']}.png"
		self.mention = f"<@{self.id}>"
		self.__bot = bot

	def __repr__(self):
		return self.name

	def create_dm(self):
		return Channel(asyncio.run(self.__bot.api_call(f"/users/@me/channels","POST",json={"recipient_id":self.id})),self.__bot)

class Member(User):

	def __init__(self, member, bot):
		if "user" in member:
			User.__init__(self,member["user"],bot)
		self.guild_id = member.get("guild_id",None)
		self.premium_since = member.get("premium_since",None)
		self.roles = [role for role in member["roles"]]
		self.mute = member["mute"]
		self.deaf = member["deaf"]
		self.nick = member.get("nick",None)
		self.joined_at = member["joined_at"]
		self.__bot = bot

	def edit(self, **modifs):
		if hasattr(self,"id"):
			user_id=self.id
			asyncio.run(self.__bot.api_call(f"/channels/{self.guild_id}/messages/{user_id}","PATCH",json=modifs))

	def kick(self):
		if hasattr(self,"id"):
			user_id=self.id
			asyncio.run(self.__bot.api_call(f"/guilds/{self.guild_id}/members/{user_id}","DELETE"))

	def ban(self, reason=None):
		if hasattr(self,"id"):
			user_id=self.id
			asyncio.run(self.__bot.api_call(f"/guilds/{self.guild_id}/bans/{user_id}","PUT", json={"reason":reason}))

	def add_role(self, role):
		if hasattr(self,"id"):
			user_id=self.id
			asyncio.run(self.__bot.api_call(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","PUT"))

	def remove_role(self, role):
		if hasattr(self,"id"):
			user_id=self.id
			asyncio.run(self.__bot.api_call(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","DELETE"))

class Reaction(API_Element):

	def __init__(self,reaction,message):
		self.count = reaction["count"]
		self.me = reaction["me"]
		self.emoji = Emoji(reaction["emoji"])
		self.message = message

class Emoji(API_Element):

	def __init__(self,emoji):
		self.name = emoji["name"]
		self.id = emoji["id"]

class Role(API_Element):

	def __init__(self, role, bot):
		self.id = role.get("id",None)
		self.name = role.get("name",None)
		self.color = role.get("color",None)
		self.hoist = role.get("hoist",None)
		self.position = role.get("position",None)
		self.permissions = role.get("permissions",None)
		self.managed = role.get("managed",None)
		self.mentionable = role.get("mentionable",None)
		self.guild_id = role.get("guild_id",None)
		self.__bot = bot

	def __repr__(self):
		return self.name

	def delete(self):
		asyncio.run(self.__bot.api_call(f"/channels/{self.guild_id}/roles/{self.id}","DELETE"))

	def edit(self,**modifs):
		asyncio.run(self.__bot.api_call(f"/channels/{self.guild_id}/messages/{self.id}","PATCH",json=modifs))


class Attachment(API_Element):

	def __init__(self,attachment):
		self.id = attachment["id"]
		self.filename = attachment["filename"]
		self.size = attachment["size"]
		self.url = attachment["url"]
		self.proxy_url = attachment["proxy_url"]
		self.height = attachment.get("height",None)
		self.width = attachment.get("width",None)

class Allowed_Mentions(API_Element):

	def __init__(self,mentions):
		self.parse = mentions.get("parse",None)
		self.roles = mentions.get("roles",None)
		self.users = mentions.get("users",None)

class Embed(API_Element):

	def __init__(self,embed):
		self.title = embed.get("title",None)
		self.type = embed.get("type",None)
		self.description = embed.get("description",None)
		self.url = embed.get("url",None)
		self.timestamp = embed.get("timestamp",None)
		self.color = embed.get("color",None)
		self.footer = Embed_Footer(embed.get("footer",{}))
		self.image = Embed_Image(embed.get("image",{}))
		self.thumbnail = Embed_Image(embed.get("thumbnail",{}))
		self.video = Embed_Image(embed.get("video",{}))
		self.provider = Embed_Provider(embed.get("provider",{}))
		self.author = Embed_Author(embed.get("author",{}))
		self.fields = [Embed_Field(field) for field in embed.get("fields",[])]

	def add_field(self,**kwargs):
		self.fields.append(Embed_Field(kwargs))
		return self.fields[-1]

class Embed_Image(API_Element):

	def __init__(self,image):
		self.url = image.get("url",None)
		self.proxy_url = image.get("proxy_url",None)
		self.height = image.get("height",None)
		self.width = image.get("width",None)

class Embed_Field(API_Element):

	def __init__(self,field):
		self.name = field.get("name",None)
		self.value = field.get("value",None)
		self.inline = field.get("inline",None)

class Embed_Footer(API_Element):

	def __init__(self,footer):
		self.text = footer.get("text",None)
		self.icon_url = footer.get("icon_url",None)
		self.proxy_icon_url = footer.get("proxy_icon_url",None)

class Embed_Provider(API_Element):

	def __init__(self,provider):
		self.name = provider.get("name",None)
		self.url = provider.get("url",None)

class Embed_Author(API_Element):

	def __init__(self,author):
		self.name = author.get("name",None)
		self.url = author.get("url",None)
		self.icon_url = author.get("icon_url",None)
		self.proxy_icon_url = author.get("proxy_icon_url",None)

class Invite(API_Element):

	def __init__(self, invite, bot):
		self.code = invite["code"]
		self.url = f"https://discord.gg/{self.code}"
		self.guild = None
		if "guild" in invite:
			self.guild = Guild(invite["guild"], bot)
		self.channel = None
		if "channel" in invite:
			self.channel = Channel(invite["channel"], bot)
		self.inviter = None
		if "inviter" in invite:
			self.inviter = User(invite["inviter"], bot)
		self.target_user = None
		if "target_user" in invite:
			self.channel = User(invite["target_user"], bot)
		self.target_user_type = invite.get("target_user_type",None)
		self.approximate_presence_count = invite.get("approximate_presence_count",None)
		self.approximate_member_count = invite.get("approximate_member_count",None)
		self.max_age = invite.get("max_age",None)
		self.max_uses = invite.get("max_uses",None)
		self.temporary = invite.get("temporary",None)
		self.uses = invite.get("uses",None)
		self.created_at = invite.get("created_at",None)
		self.__bot = bot

	def __repr__(self):
		return self.url

	def delete(self):
		asyncio.run(self.__bot.api_call(f"/invites/{self.code}","DELETE"))

class Ban(API_Element):

	def __init__(self,ban,bot):
		self.reason = ban.get("reason",None)
		self.user = User(ban["user"])
		self.__bot = bot

	def pardon(self, guild_id):
		asyncio.run(self.__bot.api_call(f"/guilds/{guild_id}/bans/{self.user.id}","DELETE"))

class Overwrite(API_Element):

	def __init__(self,overwrite,bot,channel):
		self.id = overwrite["id"]
		self.type = overwrite["type"]
		self.allow = overwrite["allow"]
		self.deny = overwrite["deny"]
		self.channel = channel
		self.__bot = bot

	def edit(self,**modifs):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel.id}/permissions/{self.id}","PUT",json=modifs))

	def delete(self):
		asyncio.run(self.__bot.api_call(f"/channels/{self.channel.id}/permissions/{self.id}","DELETE"))
