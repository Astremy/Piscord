import asyncio
import json
import aiohttp
from threading import Thread
from .Events import Events
from .API_Elements import *

class Utility:

	def get_self_user(self):
		return User(asyncio.run(self.api_call("/users/@me", "GET")), self)

	def get_self_guilds(self):
		return [Guild(guild,self) for guild in asyncio.run(self.api_call("/users/@me/guilds", "GET"))]

	def send_message(self,channel,**kwargs):
		return Message(asyncio.run(self.api_call(f"/channels/{channel}/messages", "POST", json=kwargs)),self)

	def get_guild(self,guild_id):
		return Guild(asyncio.run(self.api_call(f"/guilds/{guild_id}","GET")),self)

	def get_channel(self,channel_id):
		return Channel(asyncio.run(self.api_call(f"/channels/{channel_id}","GET")),self)

	def get_user(self,user_id):
		return User(asyncio.run(self.api_call(f"/users/{user_id}")), self)

	def get_invite(self, invite_code):
		return Invite(asyncio.run(self.api_call(f"/invites/{invite_code}","GET", params={"with_counts":"true"})),self)

class Bot(Thread,Utility,Events):

	def __init__(self,token):
		self.events_list = {}
		Events.__init__(self)
		Thread.__init__(self)
		Utility.__init__(self)
		self.token=token
		self.api="https://discord.com/api"
		self.__last_sequence = ""
		self.events = {}

	def def_event(self,event,name):
		def add_event(function):
			self.events_list[event] = [name,function]
			def thing():...
			return thing
		return add_event

	def event(self,arg):
		def truc():...

		def add_event(function):
			self.events[arg]=function
			return truc

		if type(arg) == str:
			return add_event

		self.events[arg.__name__] = arg
		return truc

	async def api_call(self,path, method="GET", **kwargs):
		defaults = {
			"headers": {
				"Authorization": f"Bot {self.token}",
				"User-Agent": "Bot"
			}
		}
		kwargs = dict(defaults, **kwargs)
		async with aiohttp.ClientSession() as session:
			async with session.request(method, self.api+path,**kwargs) as response:
				try:
					assert 200 == response.status, response.reason
					return await response.json()
				except:...

	async def begin(self):
		response = await self.api_call("/gateway")
		await self.__main(response["url"])

	async def __main(self,url):
		events = self.events_list
		async with aiohttp.ClientSession() as session:
			async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
				async for msg in ws:
					data = json.loads(msg.data)

					if data["op"] == 10:
						asyncio.create_task(self.__heartbeat(ws,data["d"]["heartbeat_interval"]))
						await ws.send_json({
							"op": 2,
							"d": {
								"token": self.token,
								"properties": {},
								"compress": False,
								"large_threshold": 250
						}})
					elif data["op"] == 0:
						if data["t"] in events:
							event = events[data["t"]]
							if event[0] in self.events:
								x = Thread(target=self.events[event[0]],args=(event[1](self,data["d"]),))
								x.start()
						self.__last_sequence=data["s"]

	async def __heartbeat(self,ws, interval):
		while True:
			await asyncio.sleep(interval / 1000)
			await ws.send_json({"op": 1,"d": self.__last_sequence})

	def run(self):
		self.loop = asyncio.new_event_loop()
		try:
			self.loop.run_until_complete(self.begin())
		except RuntimeError:print("Bot éteint")

	def stop(self):
		try:
			self.loop.stop()
		except:...
		try:
			for x in asyncio.all_tasks():
				try:
					x.cancel()
				except:...
		except:...