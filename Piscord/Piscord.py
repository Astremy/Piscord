import asyncio
import json
import aiohttp
from threading import Thread
from .Events import Events
from .Errors import *
from .API_Elements import *

class Utility:

	def get_self_user(self):
		return User(self.api("/users/@me", "GET"), self)

	def get_self_guilds(self):
		return [Guild(guild,self) for guild in self.api("/users/@me/guilds", "GET")]

	def send_message(self,channel,**kwargs):
		return Message(self.api(f"/channels/{channel}/messages", "POST", json=kwargs),self)

	def get_guild(self,guild_id):
		return Guild(self.api(f"/guilds/{guild_id}","GET"),self)

	def get_channel(self,channel_id):
		return Channel(self.api(f"/channels/{channel_id}","GET"),self)

	def get_user(self,user_id):
		return User(self.api(f"/users/{user_id}"), self)

	def get_invite(self, invite_code):
		return Invite(self.api(f"/invites/{invite_code}","GET", params={"with_counts":"true"}),self)

class Bot(Thread,Utility,Events):

	def __init__(self,token,api_sleep=0.05):
		self.events_list = {}
		Events.__init__(self)
		Thread.__init__(self)
		Utility.__init__(self)
		Bot_Element.__init__(self,{},self)
		self.token=token
		self.api_sleep = api_sleep
		self.api_url="https://discord.com/api"
		self.__last_sequence = ""
		self.events = {}
		self.is_stopped = False

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
			async with session.request(method, self.api_url+path,**kwargs) as response:
				try:
					assert response.status in [200,204]
					if response.status == 200:
						return await response.json()
				except:
					if response.status == 400:
						return BadRequestError()
					elif response.status == 403:
						return PermissionsError()
					else:
						return Error()

	def api(self, path, method="GET", **kwargs):
		loop = asyncio.new_event_loop()
		output = loop.run_until_complete(self.api_call(path,method,**kwargs))
		loop.run_until_complete(asyncio.sleep(self.api_sleep))
		loop.close()
		if output and isinstance(output,Error):
			raise output
		else:
			return output

	async def begin(self):
		response = await self.api_call("/gateway")
		await self.__main(response["url"])

	async def __main(self,url):
		events = self.events_list
		async with aiohttp.ClientSession() as session:
			async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
				async for msg in ws:
					if self.is_stopped:
						await ws.close()
						self.heartbeat.cancel()
						return
					data = json.loads(msg.data)

					if data["op"] == 10:
						self.heartbeat = asyncio.create_task(self.__heartbeat(ws,data["d"]["heartbeat_interval"]))
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
							output = event[1](self,data["d"])
							if event[0] in self.events:
								x = Thread(target=self.events[event[0]],args=(output,))
								x.start()
						self.__last_sequence=data["s"]

	async def __heartbeat(self,ws, interval):
		while True:
			await asyncio.sleep(interval / 1000)
			await ws.send_json({"op": 1,"d": self.__last_sequence})

	def run(self):
		self.loop = asyncio.new_event_loop()
		print("Starting Bot")
		try:
			self.loop.run_until_complete(self.begin())
		except RuntimeError:
			print("Stopping Bot")

	def stop(self):
		self.is_stopped = True