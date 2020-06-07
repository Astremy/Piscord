class Perm:

	def __init__(self,number):
		self.number = 2**number

	def __eq__(self,n):
		if n & self.number == self.number:
			return True
		else:
			return False

create_instant_invite = Perm(0)
kick_members = Perm(1)
ban_members = Perm(2)
administrator = Perm(3)
manage_channels = Perm(4)
manage_guild = Perm(5)
add_reactions = Perm(6)
view_audit_log = Perm(7)
priority_speaker = Perm(8)
stream = Perm(9)
view_channel = Perm(10)
send_messages = Perm(11)
send_tts_messages = Perm(12)
manage_messages = Perm(13)
embed_links = Perm(14)
attach_files = Perm(15)
read_message_history = Perm(16)
mention_everyone = Perm(17)
use_external_emojis = Perm(18)
view_guild_insights = Perm(19)
connect = Perm(20)
speak = Perm(21)
mute_members = Perm(22)
deafen_members = Perm(23)
move_members = Perm(24)
use_vad = Perm(25)
change_nickname = Perm(26)
manage_nicknames = Perm(27)
manage_roles = Perm(28)
manage_webhooks = Perm(29)
manage_emojis = Perm(30)
