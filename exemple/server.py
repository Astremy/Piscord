from Piscord import *
from SAPAS import *

bot = Bot("Token")

@bot.event("on_ready")
def on_ready(user):
	print(f"Bot {user.name} Connected !")

@bot.event("on_message")
def on_message(message):
	if message.content == "Ping !":
		bot.send_message(message.channel,"Pong !")

@bot.event("reaction_add")
def reaction_add(reaction):
	reaction.get_message().add_reaction(reaction.emoji.name)

bot.start()

site = Server("localhost",80)

@site.path("/")
def index(user):
	z=[]
	for guild in bot.get_self_guilds():
		z.append(f"<p>{guild.name} :</p>")
		for channel in guild.get_channels():
			z.append(f"<p>{channel.name} : {channel.id}<p>")
	return template("index.html",chann="".join(z))

@site.path("/send_message")
@methods("POST")
def add_reaction(user):
	if "message" in user.request.form:
		if "channel" in user.request.form:
			bot.send_message(user.request.form["channel"],user.request.form["message"])
	return redirect(user,"/")

site.start()
