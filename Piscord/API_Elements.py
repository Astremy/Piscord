class Cache:
	def __init__(self, func):
		self.func = func
		self.result = None

	def __call__(self,ref):
		if self.result:
			return self.result
		result = self.func(ref)
		self.result = result
		return result

class API_Element:

	def to_json(self):
		output = {}
		for x,y in self.__dict__.items():
			if x.endswith("__bot"):continue
			if y != None:
				if type(y) == list:
					e=[]
					for p in y:
						if isinstance(p,API_Element):
							p = p.to_json()
						e += [p]
					y = e
				if isinstance(y,API_Element):
					y = y.to_json()
				output[x]=y
		return output


class Bot_Element:

	def __init__(self, bot_element, bot):
		self.user = User(bot_element.get("user",{}), bot)
		self.guilds = [Guild(guild, bot) for guild in bot_element.get("guilds",[])]
		self.relationships = bot_element.get("relationships",[])
		self.private_channels = bot_element.get("private_channels",[])
		self.presences = bot_element.get("presences",[])
		self.voices = {}

class Guild:

	def __init__(self, guild, bot):
		self.id = guild.get("id")
		self.name = guild.get("name")
		self.icon = guild.get("icon")
		self.splash = guild.get("splash")
		self.discovery_splash = guild.get("discovery_splash")
		self.owner = guild.get("owner")
		self.owner_id = guild.get("owner_id")
		self.permissions = guild.get("permissions")
		self.region = guild.get("region")
		self.afk_channel_id = guild.get("afk_channel_id")
		self.afk_timeout = guild.get("afk_timeout")
		self.embed_enabled = guild.get("embed_enabled")
		self.embed_channel_id = guild.get("embed_channel_id")
		self.verification_level = guild.get("verification_level")
		self.default_message_notifications = guild.get("default_message_notifications")
		self.explicit_content_filter = guild.get("explicit_content_filter")
		self.roles = [Role(role,bot) for role in guild.get("roles",[])]
		self.emojis = [Emoji(emoji) for emoji in guild.get("emojis",[])]
		self.features = guild.get("features",[]) #To Do
		self.mfa_level = guild.get("mfa_level")
		self.application_id = guild.get("application_id")
		self.widget_enabled = guild.get("widget_enabled")
		self.widget_channel_id = guild.get("widget_channel_id")
		self.system_channel_id = guild.get("system_channel_id")
		self.system_channel_flags = guild.get("system_channel_flags")
		self.rules_channel_id = guild.get("rules_channel_id")
		self.joined_at = guild.get("joined_at")
		self.large = guild.get("large")
		self.unavailable = guild.get("unavailable")
		self.member_count = guild.get("member_count")
		self.voice_states = guild.get("voice_states")
		self.members = [Member(member,bot) for member in guild.get("members",[])]
		self.channels = [Channel(channel,bot) for channel in guild.get("channels",[])]
		self.presences = guild.get("presences",[]) # To Do
		self.max_presences = guild.get("max_presences")
		self.max_members = guild.get("max_members")
		self.max_video_channel_users = guild.get("max_video_channel_users")
		self.vanity_url_code = guild.get("vanity_url_code")
		self.description = guild.get("description")
		self.banner = guild.get("banner")
		self.premium_tier = guild.get("premium_tier")
		self.premium_subscription_count = guild.get("premium_subscription_count")
		self.preferred_locale = guild.get("preferred_locale")
		self.public_updates_channel_id = guild.get("public_updates_channel_id")
		self.approximate_member_count = guild.get("approximate_member_count")
		self.approximate_presence_count = guild.get("approximate_presence_count")
		self.__bot = bot

	def __repr__(self):
		if self.name:
			return self.name
		elif self.id:
			return self.id
		else:
			return "Guild"

	def get_channels(self):
		channels = self.__bot.api(f"/guilds/{self.id}/channels")
		return [Channel(channel,self.__bot) for channel in channels]

	def get_roles(self):
		roles = self.__bot.api(f"/guilds/{self.id}/roles")
		return [Role(role,self.__bot) for role in roles]

	def get_invites(self):
		invites = self.__bot.api(f"/guilds/{self.id}/invites")
		return [Invite(invite,self.__bot) for invite in invites]

	def get_members(self, limit=100, after=0):
		members = self.__bot.api(f"/guilds/{self.id}/members","GET",params={"limit":limit,"after":after})
		return [Member({**member,"guild_id":self.id},self.__bot) for member in members]

	def get_member(self,user_id):
		return Member({**self.__bot.api(f"/guilds/{self.id}/members/{user_id}"),"guild_id":self.id},self.__bot)

	def get_bans(self):
		bans = self.__bot.api(f"/guilds/{self.id}/bans")
		return [Ban(ban,self.__bot) for ban in bans]

	def get_ban(self, user_id):
		return Ban(self.__bot.api(f"/guilds/{self.id}/bans/{user_id}"),self.__bot)

	def create_channel(self,**kwargs):
		''' kwargs : https://discord.com/developers/docs/resources/guild#create-guild-channel '''
		return Channel(self.__bot.api(f"/guilds/{self.id}/channels", "POST", json=kwargs),self.__bot)

	def create_role(self,**kwargs):
		''' kwargs : https://discord.com/developers/docs/resources/guild#create-guild-role '''
		return Role(self.__bot.api(f"/guilds/{self.id}/roles", "POST", json=kwargs),self.__bot)

class Channel:

	def __init__(self, channel, bot, guild = None):
		self.id = channel.get("id")
		self.type = channel.get("type")
		self.guild_id = channel.get("guild_id")
		self.position = channel.get("position")
		self.permission_overwrites = [Overwrite(overwrite,bot,self.id) for overwrite in channel.get("permission_overwrites",[])]
		self.name = channel.get("name")
		self.topic = channel.get("topic")
		self.nsfw = channel.get("nsfw")
		self.last_message_id = channel.get("last_message_id")
		self.bitrate = channel.get("bitrate")
		self.user_limit = channel.get("user_limit")
		self.rate_limit_per_user = channel.get("rate_limit_per_user")
		self.recipients = [User(user,bot) for user in channel.get("recipients",[])]
		self.icon = channel.get("icon")
		self.owner_id = channel.get("owner_id")
		self.application_id = channel.get("application_id")
		self.parent_id = channel.get("parent_id")
		self.last_pin_timestamp = channel.get("last_pin_timestamp")
		self.invites = channel.get("invites",[])
		self.__bot = bot

		if guild:
			self.guild = guild
		else:
			self.guild = bot.get_element(bot.guilds,self.guild_id)

	def __repr__(self):
		if self.name: return self.name
		else: return self.id

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.id}","PATCH",json=modifs)

	def send(self,content=None,**kwargs):
		return Message(self.__bot.api(f"/channels/{self.id}/messages", "POST", json={"content":content,**kwargs}),self.__bot)

	def get_messages(self):
		messages = self.__bot.api(f"/channels/{self.id}/messages")
		return [Message(message,self.__bot) for message in messages]

	def get_invites(self):
		invites = self.__bot.api(f"/channels/{self.id}/invites")
		return [Invite(invite,self.__bot) for invite in invites]

	def create_invite(self,**kwargs):
		return Invite(self.__bot.api(f"/channels/{self.id}/invites","POST",json=kwargs),self.__bot)

	def typing(self):
		self.__bot.api(f"/channels/{self.id}/typing","POST")

class Message:

	def __init__(self, message, bot):
		self.id = message.get("id")
		self.channel_id = message.get("channel_id")
		self.guild_id = message.get("guild_id")
		if "author" in message:
			self.author = User(message["author"],bot)
		if "member" in message:
			self.author = Member({**message["member"],"user":{**message["author"]},"guild_id":self.guild_id}, bot)
		self.content = message.get("content")
		self.timestamp = message.get("timestamp")
		self.edited_timestamp = message.get("edited_timestamp")
		self.tts = message.get("tts")
		self.mention_everyone = message.get("mention_everyone")
		self.mentions = [User(mention,bot) for mention in message.get("mentions",[])]
		self.mentions_roles = message.get("mention_roles")
		self.mention_channels = [Channel(channel,bot) for channel in message.get("mention_channels",[])]
		self.attachments = [Attachment(attachment) for attachment in message.get("attachments",[])]
		self.embeds = [Embed(embed) for embed in message.get("embeds",[])]
		self.reactions = [Reaction(reaction,self.id) for reaction in message.get("reactions",[])]
		self.nonce = message.get("nonce")
		self.pinned = message.get("pinned")
		self.webhook_id = message.get("webhook_id")
		self.type = message.get("type")
		self.activity = message.get("activity") # Object
		self.application = message.get("application") #Object
		self.message_reference = message.get("message_reference") #Object
		self.flags = message.get("flags")
		self.__bot = bot

		self.guild = bot.get_element(bot.guilds, self.guild_id)
		if self.guild:
			self.channel = bot.get_element(self.guild.channels, self.channel_id)
		else:
			self.channel = bot.get_element(bot.private_channels, self.channel_id)

	def __repr__(self):
		return self.content

	def delete(self):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","DELETE")

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","PATCH",json=modifs)

	def add_reaction(self, emoji):
		reaction = emoji.get_reaction()
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","PUT")

	def delete_reactions(self):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions","DELETE")

	def delete_self_reaction(self, emoji):
		reaction = emoji.get_reaction()
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","DELETE")

	def delete_reaction(self,emoji,user_id=None):
		reaction = emoji.get_reaction()
		if user_id:
			self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/{user_id}","DELETE")
		else:
			self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}","DELETE")


class User:

	def __init__(self, user, bot):
		self.bot = user.get("bot")
		self.system = user.get("system")
		self.mfa_enabled = user.get("mfa_enabled")
		self.locale = user.get("locale")
		self.verified = user.get("verified")
		self.email = user.get("email")
		self.flags = user.get("flags")
		self.premium_type = user.get("premium_type")
		self.public_flags = user.get("public_flags")
		self.id = user.get("id")
		self.name = user.get("username")
		self.discriminator = user.get("discriminator")
		self.avatar = user.get("avatar")
		if self.avatar:
			if self.avatar.startswith("a_"):
				avatar_type = ".gif"
			else:
				avatar_type = ".png"
			self.avatar = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}{avatar_type}"
		self.mention = f"<@{self.id}>"
		self.__bot = bot

	def __repr__(self):
		return self.name

	@property
	@Cache
	def dm(self):
		return Channel(self.__bot.api(f"/users/@me/channels","POST",json={"recipient_id":self.id}),self.__bot)

class Member(User):

	def __init__(self, member, bot):
		if "user" in member:
			User.__init__(self,member["user"],bot)
		self.guild_id = member.get("guild_id")
		self.premium_since = member.get("premium_since")
		self.roles = [role for role in member.get("roles",[])]
		self.hoisted_role = member.get("hoisted_role")
		self.mute = member.get("mute")
		self.deaf = member.get("deaf")
		self.nick = member.get("nick")
		self.joined_at = member.get("joined_at")
		self.__bot = bot

		self.guild = bot.get_element(bot.guilds,self.guild_id)

	def edit(self, **modifs):
		if hasattr(self,"id"):
			user_id=self.id
			self.__bot.api(f"/channels/{self.guild_id}/messages/{user_id}","PATCH",json=modifs)

	def kick(self):
		if hasattr(self,"id"):
			user_id=self.id
			delete_member = self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}","DELETE")

	def ban(self, reason=None):
		if hasattr(self,"id"):
			user_id=self.id
			self.__bot.api(f"/guilds/{self.guild_id}/bans/{user_id}","PUT", json={"reason":reason})

	def add_role(self, role):
		if hasattr(self,"id"):
			user_id=self.id
			self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","PUT")

	def remove_role(self, role):
		if hasattr(self,"id"):
			user_id=self.id
			self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}/roles/{role.id}","DELETE")

class Reaction:

	def __init__(self,reaction,message_id):
		self.count = reaction.get("count")
		self.me = reaction.get("me")
		self.emoji = Emoji(reaction["emoji"])
		self.message_id = message_id

class Emoji:

	def __init__(self,emoji):
		self.name = emoji.get("name")
		self.id = emoji.get("id")
		self.roles = emoji.get("roles")
		self.user = emoji.get("user")
		self.require_colons = emoji.get("require_colons")
		self.managed = emoji.get("managed")
		self.animated = emoji.get("animated")
		self.available = emoji.get("available")

	def get_reaction(self):
		if self.id:
			return f"{self.name}:{self.id}"
		return self.name

class Role:

	def __init__(self, role, bot):
		self.id = role.get("id")
		self.name = role.get("name")
		self.color = role.get("color")
		self.hoist = role.get("hoist")
		self.position = role.get("position")
		self.permissions = role.get("permissions")
		self.managed = role.get("managed")
		self.mentionable = role.get("mentionable")
		self.guild_id = role.get("guild_id")
		self.__bot = bot

		self.guild = bot.get_element(bot.guilds,self.guild_id)

	def __repr__(self):
		return self.name

	def delete(self):
		self.__bot.api(f"/channels/{self.guild_id}/roles/{self.id}","DELETE")

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.guild_id}/messages/{self.id}","PATCH",json=modifs)


class Attachment:

	def __init__(self,attachment):
		self.id = attachment.get("id")
		self.filename = attachment.get("filename")
		self.size = attachment.get("size")
		self.url = attachment.get("url")
		self.proxy_url = attachment.get("proxy_url")
		self.height = attachment.get("height")
		self.width = attachment.get("width")

class Allowed_Mentions:

	def __init__(self,mentions):
		self.parse = mentions.get("parse")
		self.roles = mentions.get("roles")
		self.users = mentions.get("users")

class Embed(API_Element):

	def __init__(self,embed={}):
		self.title = embed.get("title")
		self.type = embed.get("type")
		self.description = embed.get("description")
		self.url = embed.get("url")
		self.timestamp = embed.get("timestamp")
		self.color = embed.get("color")
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
		self.url = image.get("url")
		self.proxy_url = image.get("proxy_url")
		self.height = image.get("height")
		self.width = image.get("width")

class Embed_Field(API_Element):

	def __init__(self,field):
		self.name = field.get("name")
		self.value = field.get("value")
		self.inline = field.get("inline")

class Embed_Footer(API_Element):

	def __init__(self,footer):
		self.text = footer.get("text")
		self.icon_url = footer.get("icon_url")
		self.proxy_icon_url = footer.get("proxy_icon_url")

class Embed_Provider(API_Element):

	def __init__(self,provider):
		self.name = provider.get("name")
		self.url = provider.get("url")

class Embed_Author(API_Element):

	def __init__(self,author):
		self.name = author.get("name")
		self.url = author.get("url")
		self.icon_url = author.get("icon_url")
		self.proxy_icon_url = author.get("proxy_icon_url")

class Invite:

	def __init__(self, invite, bot):
		self.code = invite.get("code")
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
		self.target_user_type = invite.get("target_user_type")
		self.approximate_presence_count = invite.get("approximate_presence_count")
		self.approximate_member_count = invite.get("approximate_member_count")
		self.max_age = invite.get("max_age")
		self.max_uses = invite.get("max_uses")
		self.temporary = invite.get("temporary")
		self.uses = invite.get("uses")
		self.created_at = invite.get("created_at")
		self.__bot = bot

	def __repr__(self):
		return self.url

	def delete(self):
		self.__bot.api(f"/invites/{self.code}","DELETE")

class Ban:

	def __init__(self,ban,bot):
		self.reason = ban.get("reason")
		self.user = User(ban["user"])
		self.__bot = bot

	def pardon(self, guild_id):
		self.__bot.api(f"/guilds/{guild_id}/bans/{self.user.id}","DELETE")

class Overwrite:

	def __init__(self,overwrite,bot,channel_id):
		self.id = overwrite.get("id")
		self.type = overwrite.get("type")
		self.allow = overwrite.get("allow")
		self.deny = overwrite.get("deny")
		self.channel_id = channel_id
		self.__bot = bot

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.channel_id}/permissions/{self.id}","PUT",json=modifs)

	def delete(self):
		self.__bot.api(f"/channels/{self.channel_id}/permissions/{self.id}","DELETE")
