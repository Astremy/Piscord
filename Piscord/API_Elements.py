import asyncio

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
						e += [p]
					y = e
				if isinstance(y,API_Element):
					y = y.to_json()
				output[x]=y
		return output

class Guild(API_Element):

	def __init__(self, guild, bot):
		self.id = guild["id"]
		self.name = guild["name"]
		self.icon = guild.get("icon",None)
		self.splash = guild.get("splash",None)
		self.discovery_splash = guild.get("discovery_splash",None)
		self.owner = guild.get("owner",None)
		self.owner_id = guild.get("owner_id",None)
		self.permissions = guild.get("permissions",None)
		self.region = guild.get("region",None)
		self.afk_channel_id = guild.get("afk_channel_id",None)
		self.afk_timeout = guild.get("afk_timeout",None)
		self.embed_enabled = guild.get("embed_enabled",None)
		self.embed_channel_id = guild.get("embed_channel_id",None)
		self.verification_level = guild.get("verification_level",None)
		self.default_message_notifications = guild.get("default_message_notifications",None)
		self.explicit_content_filter = guild.get("explicit_content_filter",None)
		self.roles = [Role(role,bot) for role in guild.get("roles",[])]
		self.emojis = [Emoji(emoji) for emoji in guild.get("emojis",[])]
		self.features = guild.get("features",[]) #To Do
		self.mfa_level = guild.get("mfa_level",None)
		self.application_id = guild.get("application_id",None)
		self.widget_enabled = guild.get("widget_enabled",None)
		self.widget_channel_id = guild.get("widget_channel_id",None)
		self.system_channel_id = guild.get("system_channel_id",None)
		self.system_channel_flags = guild.get("system_channel_flags",None)
		self.rules_channel_id = guild.get("rules_channel_id",None)
		self.joined_at = guild.get("joined_at",None)
		self.large = guild.get("large",None)
		self.unavailable = guild.get("unavailable",None)
		self.member_count = guild.get("member_count",None)
		self.voice_states = guild.get("voice_states",None)
		self.members = [Member(member,bot) for member in guild.get("members",[])]
		self.channels = [Channel(channel,bot) for channel in guild.get("channels",[])]
		self.presences = guild.get("presences",[]) # To Do
		self.max_presences = guild.get("max_presences",None)
		self.max_members = guild.get("max_members",None)
		self.vanity_url_code = guild.get("vanity_url_code",None)
		self.description = guild.get("description",None)
		self.banner = guild.get("banner",None)
		self.premium_tier = guild.get("premium_tier",None)
		self.premium_subscription_count = guild.get("premium_subscription_count",None)
		self.preferred_locale = guild.get("preferred_locale",None)
		self.public_updates_channel_id = guild.get("public_updates_channel_id",None)
		self.approximate_member_count = guild.get("approximate_member_count",None)
		self.approximate_presence_count = guild.get("approximate_presence_count",None)
		self.__bot = bot

	def __repr__(self):
		return self.name

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
		self.__bot.api(f"/channels/{self.id}","PATCH",json=modifs)

	def send(self,**kwargs):
		return Message(self.__bot.api(f"/channels/{self.id}/messages", "POST", json=kwargs),self.__bot)

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
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","DELETE")

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}","PATCH",json=modifs)

	def add_reaction(self, reaction):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","PUT")

	def delete_reactions(self):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions","DELETE")

	def delete_self_reaction(self, reaction):
		self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me","DELETE")

	def delete_reaction(self,reaction,user_id=None):
		if user_id:
			self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/{user_id}","DELETE")
		else:
			self.__bot.api(f"/channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}","DELETE")


class User(API_Element):

	def __init__(self, user, bot):
		self.bot = user.get("bot",None)
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
			if user["avatar"].startswith("a_"):
				avatar_type = ".gif"
			else:
				avatar_type = ".png"
			self.avatar = f"https://cdn.discordapp.com/avatars/{self.id}/{user['avatar']}{avatar_type}"
		self.mention = f"<@{self.id}>"
		self.__bot = bot

	def __repr__(self):
		return self.name

	def create_dm(self):
		return Channel(self.__bot.api(f"/users/@me/channels","POST",json={"recipient_id":self.id}),self.__bot)

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
			self.__bot.api(f"/channels/{self.guild_id}/messages/{user_id}","PATCH",json=modifs)

	def kick(self):
		if hasattr(self,"id"):
			user_id=self.id
			delete_member = self.__bot.api(f"/guilds/{self.guild_id}/members/{user_id}","DELETE")
			return x

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
		self.__bot.api(f"/channels/{self.guild_id}/roles/{self.id}","DELETE")

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.guild_id}/messages/{self.id}","PATCH",json=modifs)


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
		self.__bot.api(f"/invites/{self.code}","DELETE")

class Ban(API_Element):

	def __init__(self,ban,bot):
		self.reason = ban.get("reason",None)
		self.user = User(ban["user"])
		self.__bot = bot

	def pardon(self, guild_id):
		self.__bot.api(f"/guilds/{guild_id}/bans/{self.user.id}","DELETE")

class Overwrite(API_Element):

	def __init__(self,overwrite,bot,channel):
		self.id = overwrite["id"]
		self.type = overwrite["type"]
		self.allow = overwrite["allow"]
		self.deny = overwrite["deny"]
		self.channel = channel
		self.__bot = bot

	def edit(self,**modifs):
		self.__bot.api(f"/channels/{self.channel.id}/permissions/{self.id}","PUT",json=modifs)

	def delete(self):
		self.__bot.api(f"/channels/{self.channel.id}/permissions/{self.id}","DELETE")
