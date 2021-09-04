from .API_Elements import *
import json


class OAuth:

    def __init__(self, bot, secret, redirect_uri, scope):
        self.bot = bot
        self.secret = secret
        self.id = bot.get_self_user().id
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_url(self):

        """
        Get the url for authentification with discord
        """

        return f"https://discord.com/api/oauth2/authorize?client_id={self.id}" \
               f"&redirect_uri={self.redirect_uri}&response_type=code&scope={'%20'.join(self.scope.split())}"

    def get_token(self, code):

        """
        Get the token of the user

        code:
            The code returned by the authentification
        """

        data = {
            "client_id": self.id,
            "client_secret": self.secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }

        return self.bot.api("/oauth2/token", "POST", data=data)

    def __request_token(self, token, url):
        headers = {
            "Authorization": f"Bearer {json.loads(token)['access_token']}"
        }

        return self.bot.api(url, "GET", headers=headers)

    def get_user(self, token):

        """
        Get a :class:`User` object, represent the authenticated user

        token:
            The token of the user
        """

        if "identify" in self.scope:
            return User(self.__request_token(token, "/users/@me"), self.bot)
        return "Invalid Scope"

    def get_guilds(self, token):

        """
        Get a list of :class:`Guild` objects, the guilds where the user is

        token:
            The token of the user
        """

        if "guilds" in self.scope:
            return [Guild(guild, self.bot) for guild in self.__request_token(token, "/users/@me/guilds")]
        return "Invalid Scope"

    def add_guild_member(self, token, guild_id, user_id):

        """
        Add the authenticated user to a guild where the bot is

        token:
            The token of the user
        guild_id:
            The if of the guild to add
        user_id:
            The id of the user
        """

        if "guilds.join" in self.scope:
            return Member({**self.bot.api_call(f"/guilds/{guild_id}/members/{user_id}", "PUT",
                                               json=json.loads(token)["access_token"]), "guild_id": guild_id}
                          )
        return "Invalid Scope"
