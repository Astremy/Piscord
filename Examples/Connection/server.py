from Piscord import *
from SAPAS import *
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

bot = Bot("Bot Token")

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

auth = OAuth(bot,"Bot Secret","http://127.0.0.1/connect","identify guilds")

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
