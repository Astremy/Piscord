from Piscord import *
from SAPAS import *
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

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

site = Server("127.0.0.1",80)

auth = OAuth(bot,"Secret","http://127.0.0.1/connect","identify guilds")

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
	return " ".join(f"<p><a href='/panel/{guild.id}'>{guild.name}</a></p>" for guild in guilds)

@site.path("/panel/{var}")
@need_cookies("token")
def discord_server(user,var):
	if var.isdecimal():
		b=0
		guilds = auth.get_guilds(user.cookies["token"])
		for guild in guilds:
			if var == guild.id:
				b=guild
		if b:
			try:
				guild = bot.get_guild(var)
				if user.request.method == "POST" and "channel" in user.request.form and "message" in user.request.form:
					message = user.request.form["message"].replace("+"," ")
					clean_message = message.split("%")
					for i in range(1,len(clean_message)):
						clean_message[i] = chr(int(clean_message[i][:2],16))+clean_message[i][2:]
					bot.send_message(user.request.form["channel"],"".join(clean_message))
					return f"<script>window.location.href='{user.request.url}';</script>"
				else:
					return template("send_message.html",channs=" ".join(f"<a onclick='chann(\"{chann.id}\");'>{chann.name}</a>" for chann in guild.get_channels()))
			except:
				return "Not Bot"
		return "Not in your discords"
	return "Error"

site.start()
