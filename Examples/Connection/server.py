from Piscord import *
from SAPAS import *
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

bot = Bot("NzA1NTE1ODMzNjk0MzU1NTY2.XqtrrA.FBQr0JNbjHPic6IksPSIh88FJH4")

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

site = Server("127.0.0.1",80)

auth = OAuth(bot,"fT9dVgqu2DU72nr0bpdkZx2pZIQZ34AG","http://127.0.0.1/connect","identify guilds")

"""
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
"""

@site.path("/")
def index(user):
	return template("index.html")

@site.path("/connect")
def connect(user):
	if "code" in user.request.form:
		token = auth.get_token(user.request.form["code"])
		user.set_cookie("token",json.dumps(token))
		return redirect(user,"/panel")
	elif "error" in user.request.form:
		return redirect(user,"/")
	else:
		return redirect(user,auth.get_url())

@site.path("/panel")
@need_cookies("token")
def panel(user):
	guilds = auth.get_guilds(user.cookies["token"])
	return [guild.name for guild in guilds]

site.start()