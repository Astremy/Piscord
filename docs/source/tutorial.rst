
Tutorial Piscord
================

Introduction
------------

Que permet piscord ?
^^^^^^^^^^^^^^^^^^^^

Piscord permet, au même titre que Discord.py, de faire des bots discord.
Seulement, l'avantage est que Piscord simplifie la création de bots sur plusieurs points.

Tout d'abord, la programmation avec Piscord est synchrone, ce qui en simplifie l'utilisation,
surtout par des personnes pas forcément expertes en python

Ensuite, la librairie n'est pas forcément bloquante.
Cela permet de faire plusieurs bots en un script, de lancer un serveur web en même temps..
A peu près ce que l'on veut.

Enfin, nous essayons de faire que ce soit le plus simple possible de faire un dialogue avec le web.
Il y a notamment une classe (OAuth) qui est la pour permettre d'utiliser la connexion avec discord facilement en faisant un site,
et d'exploiter ces données comme un bot le ferais.


Quels sont les prérequis pour l'utiliser ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les prérequis demandés pour utiliser piscord sont simples
- Savoir lire une doc (ce que vous êtes en train de faire)
- Connaitres les bases (variables, boucles, comparaison, fonctions)
- Savoir utiliser des classes
- Savoir débugguer

De plus, connaitre les décorateurs est utile mais pas indispensable vu qu'ils sont utilisés partout mais l'on ne s'attarde pas sur leur fonctionnement.


Comment installer piscord ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour installer la librairie, cela est très simple, il suffit de l'installer avec pip, (pip install -U piscord).
Cela va installer les dépendances de cette dernière, pour vous permettre de l'utiliser directement après.

Ensuite, dans votre code python, utilisez `import piscord`, `from piscord import *` ou `from piscord import things`
selon comment vous voulez l'utiliser.

First Bot
---------

Mettre en ligne le bot
^^^^^^^^^^^^^^^^^^^^^^

Pour mettre en ligne votre premier bot, récupérez le **token** de ce dernier et faites comme ceci :

.. code-block:: python

	from Piscord import Bot
	# Import de la classe Bot a partir de la librairie

	bot = Bot("Token")
	# Création d'un Bot avec votre token

	@bot.event
	def on_ready(ready):
		print(f"Bot {ready.user.name} Connected")
	# Créer un event correpondant à celui de "on_ready" (quand le bot est connecté a discord), et dire que le bot est lancé.

	bot.run()
	# Lancer le bot en mode bloquant

Information :
^^^^^^^^^^^^^

Vous avez deux façons de créer un event :
- En utilisant @bot.event et en renommant la fonction du nom de l'event
- En utilisant @bot.event("nom_de_l_event") et en renommant la fonction comme vous le souhaitez

Ce qui donne ça :

.. code-block:: python

	@bot.event
	def on_ready(ready):...

	ou

	@bot.event("on_ready")
	def ready(ready):...


Aussi, vous pouvez lancer le bot en mode bloquant (le code après ne sera pas exécuté) ou non bloquant.

.. code-block:: python

	bot.run()
	# Manière bloquante, a utiliser si l'on ne compte rien faire en même temps que lancer le bot.

	bot.start()
	# Manière non bloquante, si on lance d'autres bots après, ou un serveur web en parallèle.


Ping Pong
^^^^^^^^^

Une manière souvent utilisé pour illustrer la création d'un pemier bot est une commande ("ping") qui fera répondre une autre ("pong") au bot.
Voyons comment le faire avec Piscord :

.. code-block:: python

	from Piscord import Bot

	bot = Bot("Token")

	@bot.event
	def on_ready(ready):
		print(f"Bot {ready.user.name} Connected")

	@bot.event
	def on_message(message):
		if message.content == "!ping":
			message.channel.send("Pong !")
	# Quand un message est envoyé, on vérifie si son contenu est "!ping".
	# Si c'est le cas, on envoi dans le salon le message "Pong !"

	bot.run()

Objet Message
^^^^^^^^^^^^^

Quand on déclare un event, on récupère en argument un objet Event nous permettant de récupérer des informations de ce dernier.

Pour les voir je vous invite a aller consulter [La Documentation au sujet des Messages](https://piscord.astremy.com/#Message).
Sinon, voyons ensemble les plus utiles :

.. code-block:: python

	Message.content
	# Le contenu du message, ce qu'à saisi l'utilisateur. Cela permet d'identifier des éventuels commandes, gros mots...
	# C'est le message en lui-même (une chaine de caractères).

	Message.author
	# L'auteur du message. Un objet User se rapportant à l'utilsateur qui a éxécuté la commande,
	# permettant d'avoir diverses informations sur lui (pseudo, id..)

	Message.channel
	# Le salon dans lequel a été envoyé le message. Permet d'y renvoyer un message,
	# Ou de récupérer des informations sur le salon.

	Message.guild
	# Le serveur dans lequel a été envoyé le message.
	# Permet d'en récupérer des informations.


Un bot basique
^^^^^^^^^^^^^^

Voici un exemple un peu plus développé de l'utilisation de l'argument (je ne montre pas tout le code, seulement la partie event) :

.. code-block:: python

	@bot.event
	def on_message(message):
		if message.content == "!infos":
			if message.guild:
				server = message.guild.name
			else:
				server = "Aucun, nous sommes en messages privés"
			message.channel.send(f"Informations :\nUtilisateur : {message.author}\nServeur : {server}")

Envoyer des messages
--------------------

Pour envoyer un message, il y a deux façons de s'y prendre

.. code-block:: python

	channel.send(message)
	# Façon largement préférée, facile d'utilisation et simple à comprendre.

	bot.send_message(channel_id, message)
	# Ancienne forme, dépréciée, a utiliser le moins possible, sauf dans des cas très précis.

Dans ce tutoriel, on s'attardera sur la première forme.

Le premier argument de channel.send() est le contenu (content) du message.
Il n'est pas obligé d'être spécifié en tant que kwarg (sous forme `Channel.send(content = "contenu")`) 
mais peut simplement être mis directement `Channel.send("contenu")`.

Cependant, pour le reste des arguments, il faut spécifier le nom.

Arguments
^^^^^^^^^

Il y a différents arguments que l'on peut mettre dans le send :
- tts : Une valeur True ou False, si le message envoyé est un text-to-speech.
- files : Une liste des nom de fichiers que l'on souhaite envoyer (si l'on en envoie).
- embed : Un embed, nous verrons plus loin comment en faire.
- allowed_mentions : Un objet Allowed_Mentions, nous verrons également comment le faire plus loin.

### Allowed_Mentions

Les mentions autorisés permettent d'empêcher que le bot mentionne par mégarde quelque-chose qu'il ne devrait pas
(ex : mentionner everyone parce qu'il a les perms et qu'un malin lui fait répéter une mention qu'il ne peut pas utiliser).

Il a plusieurs paramètres : 
Parse : Parse est essentiel quand on joue avec la classe. Elle indique les types de mentions a autoriser, même si on doit les détailler après.
C'est une liste qui peut prendre les arguments que l'on veut selon ce que l'on souhaite faire.
- "everyone" : Autorise les mentions d'`@everyone` et `@here`
- "users" : Permet de mentionner les utilisateurs.
- "roles" : Permet de mentionner les rôles.

Ainsi, par exemple, vous pouvez faire :

.. code-block:: python

	Allowed_Mentions.parse = []
	# Supprime toutes les mentions

	Allowed_Mentions.parse = ["everyone"]
	# Ne permet au bot de mentionner seulement everyone/here (s'il en as les permissions)


Users : Users est un paramètre de la classe qui, si on ne permet pas de mentionner tous les utilisateurs (en mettant "users"),
permet de quand même en mentionner, mais en précisant les id des utilisateurs a laisser (avec un maximum de 100).

Roles : Roles est comme Users, mais pour les rôles. Si on ne permet pas au bot de mentionner tous les rôles,
permet de spécifier l'id des rôles a pouvoir mentionner quand même.

Exemple
"""""""

Voici un exemple de commande que l'on peut faire, ou cela se trouve utile :

.. code-block:: python
	
	@bot.event
	def on_message(message):
		content = message.content.split()
		if content[0] == "!me":
			if len(content) > 1:
				allow = Allowed_Mentions() # ou Allowed_Mentions({}) selon la version.
				allow.parse = []
				allow.users = [message.author.id]
				message.channel.send(" ".join(content[1:]),allowed_mentions=allow.to_json())

	# Envoie le message que l'utilisateur a mis après la commande !me, tout en ne pouvant mentionner que l'auteur de la commande.


Les embeds
^^^^^^^^^^

Les embeds sont quelque chose de très importants par rapport au messages, et mérite que l'on s'y attarde.

Ces derniers ont de nombreuses propriétés, et l'on s'attardera pas sur toutes. Pour plus d'informations,
visitez [La Documentation relative aux Embed](https://piscord.astremy.com/#Embed) ou [Les informations de Discord sur les Embed](https://discord.com/developers/docs/resources/channel#embed-object).

Voici les plus utiles :
- title : Une chaine de caractère correspondante au titre de l'Embed.
- description : Le texte dans l'Embed.
- color : La couleur de l'Embed (sous format hexadécimal passé en décimal).
- Image : Un objet image correspondant à une image principale de l'Embed. (Voir la documentation)

De plus, les Embed ont ce que l'on appelle les fields.
Ce sont des zones qui contiennent chacun leur titre et texte que l'on met dans un Embed.
Pour ajouter un field a un embed, on utilise Embed.add_field(name = name, value = value, inline = inline)

Exemple
"""""""

.. code-block:: python

	embed = Embed() # Crée l'embed

	embed.title = "Description des commandes" # Défini le titre de l'embed
	embed.color = 3375070 # Défini la couleur

	embed.add_field(name="!me",value="Commande qui répète du texte, en ne pouvant mentionner que soit-même")
	# Le name correspond au titre du field, la value à son contenu. Mettre inline = True permet de faire revenir le bloc a la ligne.
	embed.add_field(name="!ping",value="Commande de base qui répond 'Pong !'")

	Channel.send(embed=embed.to_json())

Quand l'on envoie un embed dans un channel, il ne faut pas oublier de mettre un .to_json, comme pour le Allowed_Mentions.