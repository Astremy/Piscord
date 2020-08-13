"""
CREATE_INSTANT_INVITE:
	Permission to create instant invites for guild
KICK_MEMBERS:
	Permission to kick members from the guild
BAN_MEMBERS:
	Permission to ban members from the guild
ADMINISTRATOR:
	Admin permission of the guild
MANAGE_CHANNELS:
	Permission to modify channels of the guild
MANAGE_GUILD:
	Permission to modify guild
ADD_REACTIONS:
	Permission to add reaction on a message (if the reaction isn't already here)
VIEW_AUDIT_LOG:
	Permission to see the guild log
PRIORITY_SPEAKER:
	Permission to speak on a priority basis in guild
STREAM:
	Permission to stream in guild voice channel
VIEW_CHANNEL:
	Permission to view channels in guild
SEND_MESSAGES:
	Permission to send messages in channel
SEND_TTS_MESSAGES:
	Permission to send tts messages in channel
MANAGE_MESSAGES:
	Permission to delete messages of other members
EMBED_LINKS:
	Permission to auto-embed links
ATTACH_FILES:
	Permission to send files (images, files..)
READ_MESSAGE_HISTORY:
	Permission to read previous messages
MENTION_EVERYONE:
	Permission to mention @everyone or @here
USE_EXTERNAL_EMOJIS:
	Permission to send emoji from other guilds
VIEW_GUILD_INSIGHTS:
	Permission to view guild insights
CONNECT:
	Permission to connect to voice channels
SPEAK:
	Permission to speak in voice channels
MUTE_MEMBERS:
	Permission to mute members (can't speak)
DEAFEN_MEMBERS:
	Permission to deaf members (can't hear)
MOVE_MEMBERS:
	Permission to move members between voice channels
USE_VAD:
	Permission to use voice-activity-detection
CHANGE_NICKNAME:
	Permission to change self nickname
MANAGE_NICKNAMES:
	Permission to change nickname of other members
MANAGE_ROLES:
	Permission to create/edit roles
MANAGE_WEBHOOKS:
	Permission to create/edit webhooks
MANAGE_EMOJIS:
	Permission to create/edit emojis
"""

class Perm(int):

	def __new__(cls, value):
		return int.__new__(cls, value)

	def __eq__(self,n):
		if isinstance(n,Perm):
			return (n.real & self.real) == n.real
		else:
			return (int(n) & self.real) == int(n)

	def __ne__(self,n):
		return not self == n

	def __add__(self,n):
		return self | n

	def __sub__(self,n):
		if isinstance(n,Perm):
			n = n.real
		n = int(n)

		out = Perm(self.real - (n & self.real))
		return out

	def __or__(self,n):
		if isinstance(n,Perm):
			out = Perm(self.real | n.real)
		else:
			out = Perm(self.real | int(n))
		return out

CREATE_INSTANT_INVITE = Perm(2**0)
KICK_MEMBERS = Perm(2**1)
BAN_MEMBERS = Perm(2**2)
ADMINISTRATOR = Perm(2**3)
MANAGE_CHANNELS = Perm(2**4)
MANAGE_GUILD = Perm(2**5)
ADD_REACTIONS = Perm(2**6)
VIEW_AUDIT_LOG = Perm(2**7)
PRIORITY_SPEAKER = Perm(2**8)
STREAM = Perm(2**9)
VIEW_CHANNEL = Perm(2**10)
SEND_MESSAGES = Perm(2**11)
SEND_TTS_MESSAGES = Perm(2**12)
MANAGE_MESSAGES = Perm(2**13)
EMBED_LINKS = Perm(2**14)
ATTACH_FILES = Perm(2**15)
READ_MESSAGE_HISTORY = Perm(2**16)
MENTION_EVERYONE = Perm(2**17)
USE_EXTERNAL_EMOJIS = Perm(2**18)
VIEW_GUILD_INSIGHTS = Perm(2**19)
CONNECT = Perm(2**20)
SPEAK = Perm(2**21)
MUTE_MEMBERS = Perm(2**22)
DEAFEN_MEMBERS = Perm(2**23)
MOVE_MEMBERS = Perm(2**24)
USE_VAD = Perm(2**25)
CHANGE_NICKNAME = Perm(2**26)
MANAGE_NICKNAMES = Perm(2**27)
MANAGE_ROLES = Perm(2**28)
MANAGE_WEBHOOKS = Perm(2**29)
MANAGE_EMOJIS = Perm(2**30)