OAuth with Piscord
------------------

Piscord include some functions to use authentification with discord

OAuth is a class to use that

How to create
^^^^^^^^^^^^^

.. code-block:: python

	from piscord import Bot, OAuth
	
	bot = Bot("Token")

	auth = OAuth(bot, "Secret", "url of redirect to get token", "scope")

You **should** have a bot object but you doesn't need to start it.
If you doesn't start the bot, you can create channel, rename, a lot of thing,
but can't receive commands or send message (require connexion).

The url is where the user is redirect after authentification with a code get request arg to obtain the token.

The scope is what the bot can do to the user account (see more : https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes)

Get the token
^^^^^^^^^^^^^

.. code-block:: python

	# To get the url where redirect the user for authentification with discord
	url = auth.get_url()

	# Code is the code get in the url after authentification
	token = auth.get_token(code)

After this, you have the token of the client.
You can store it (in user session cookie in web, or anything), and exploit it.

Usages
^^^^^^

.. code-block:: python

	# Get piscord user objet of the authentified user
	# You must have the identify scope
	user = auth.get_user(token)

	# Get list of the guilds where the user is
	# You must have the guilds scope
	guilds = auth.get_guilds(token)

	# Add the user to a guild where the bot is
	# You must have the guilds.join scope
	auth.add_guild_member(token, guild_id, user_id)

Functions
^^^^^^^^^

.. automodule:: piscord
	:noindex:

.. autoclass:: OAuth
	:members: