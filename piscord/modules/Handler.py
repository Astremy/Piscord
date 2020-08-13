from ..Piscord import Bot

class Handler(Bot):

	def __init__(self, token, prefix, api_sleep=0.05, shards=[0,1], verif_command=None):

		Bot.__init__(self, token, api_sleep=api_sleep, shards=shards)

		self.prefix = prefix
		self.commands = {}
		self.ext = {}
		self.on_message = None
		self.verif_command = self.verif
		if verif_command:
			self.verif_command = verif_command

		def handle(message):
			command = self.verif_command(message)
			if command:
				if command in self.commands:
					self.commands[command](message)
			if self.on_message:
				self.on_message(message)

		self.events["on_message"] = handle

	def verif(self, message):
		if message.content.startswith(self.prefix):
			return message.content.split()[0][len(self.prefix):]

	def command(self, arg):

		def add_command(function):
			self.commands[arg]=function
			return

		if type(arg) == str:
			return add_event

		self.commands[arg.__name__] = arg
		return

	def event(self,arg):

		def add_event(function):
			if arg == "on_message":
				self.on_message = function
				return
			self.events[arg]=function
			return

		if type(arg) == str:
			return add_event

		if arg.__name__ == "on_message":
			self.on_message = arg
			return
		self.events[arg.__name__] = arg
		return

	def load_module(self, name):
		self.ext[name] = Ext_Handler(self, name)
		with open(f"commands/{name}.py","r", encoding="utf-8") as file:
			exec(file.read(), {**globals(),"bot":self.ext[name]})

	def unload_module(self, name):
		if name in self.ext:
			for x in self.ext[name].commands:
				del self.commands[x]

class Ext_Handler:

	def __init__(self, handler, name):

		self.__handler = handler
		self.prefix = handler.prefix
		self.name = name
		self.commands = []

	def command(self, arg):

		def add_command(function):
			self.__handler.commands[arg]=function
			self.commands.append(arg)
			return

		if type(arg) == str:
			return add_event

		self.__handler.commands[arg.__name__] = arg
		self.commands.append(arg.__name__)
		return