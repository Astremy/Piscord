from Piscord import *
from SAPAS import *

bot = Bot("Token")

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
			message = user.request.form["message"].replace("+"," ")
			clean_message = message.split("%")
			for i in range(1,len(clean_message)):
				clean_message[i] = chr(int(clean_message[i][:2],16))+clean_message[i][2:]
			bot.send_message(user.request.form["channel"],"".join(clean_message))
	return redirect(user,"/")

site.start()
