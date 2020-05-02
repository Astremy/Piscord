from Piscord import *
from SAPAS import *

bot = Bot("Token")

@bot.event("on_ready")
def on_ready(ready):
	print(f"Bot {ready.name} Connected !")

@bot.event("on_message")
def on_message(message):
	content = message.content.split()
	if len(content):
		if content[0]=="!avatar":
			if len(message.mentions)<1:
				user=message.author
			else:
				user=message.mentions[0]

			if user.avatar:
				embed = Embed({})
				embed.color = 3375070
				embed.title = f"{user.name}'s avatar"
				embed.image = Embed_Image({})
				embed.image.url = str(user.avatar)
				bot.send_message(message.channel_id,embed=embed.to_json())
			else:
				bot.send_message(message.channel_id,content="Aucun avatar")
	if message.content == "Ping !":
		bot.send_message(message.channel_id,content=f"Pong ! {message.author.mention}")

@bot.event("reaction_add")
def reaction_add(reaction):
	reaction.get_message().add_reaction(reaction.emoji.name)

bot.start()

site = Server("localhost",8080)

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
			bot.send_message(user.request.form["channel"],content="".join(clean_message))
	return redirect(user,"/")

site.start()
