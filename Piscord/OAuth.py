from .API_Elements import *

class OAuth:

	def __init__(self, bot, secret, redirect_uri, scope):
		self.bot = bot
		self.secret = secret
		self.id = bot.get_self_user().id
		self.redirect_uri = redirect_uri
		self.scope = scope

	def get_url(self):
		return f"https://discord.com/api/oauth2/authorize?client_id={self.id}&redirect_uri={self.redirect_uri}&response_type=code&scope={'%20'.join(self.scope.split())}"

	def get_token(self, code):
		data = {
			"client_id": self.id,
			"client_secret": self.secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope
		}

		return self.__bot.api("/oauth2/token","POST",data=data)

	def __request_token(self,token,url):
		headers = {
			"Authorization": f"Bearer {json.loads(token)['access_token']}"
		}

		return self.__bot.api(url,"GET",headers=headers)

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