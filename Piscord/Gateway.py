import websockets
import json
import asyncio

class Gateway:

	def __init__(self, url, token, auth_op = 10, events_code = 0):
		self.url = url
		self.token = token
		self.auth_op = auth_op
		self.last_sequence = 0
		self.events_code = events_code
		self.session_id = None

	async def connect(self, action = None):
		self.loop = asyncio.get_event_loop()
		ws = await websockets.connect(self.url)
		self.ws = ws
		while True:
			try:
				msg = await self.ws.recv()
			except websockets.exceptions.ConnectionClosedOK as e:
				if e.code == 1001:
					if self.session_id and self.last_sequence:
						payload = {
							"op": 6,
							"d": {
								"token": self.token,
								"session_id": self.session_id,
								"seq": self.last_sequence
						}}
						await self.ws.close()
						self.ws = await websockets.connect(self.url)
						await self.send(payload)
						msg = await self.ws.recv()
						data = json.loads(msg)
						self.interval = data["d"]["heartbeat_interval"]
						continue
				return
			data = json.loads(msg)
			x = data.get("s")
			if x:
				self.last_sequence = x
			if data["op"] == self.auth_op:
				self.interval = data["d"]["heartbeat_interval"]
				self.heartbeat = asyncio.create_task(self.__heartbeat(self.ws))
				payload = {
					"op": 2,
					"d": {
						"token": self.token,
						"properties": {
							"$browser": "Piscord",
							"$device": "Piscord"
				}}}
				await self.send(payload)
			if data["op"] == self.events_code:
				if data["t"] == "READY":
					self.session_id = data["d"]["session_id"]
			yield data

	async def __heartbeat(self, ws):
		while True:
			await asyncio.sleep(self.interval / 1000)
			await self.send({"op": 1,"d": self.last_sequence})

	async def send(self, payload):
		await self.ws.send(json.dumps(payload))

	async def _stop(self):
		await self.ws.close()

	def stop(self):
		asyncio.run_coroutine_threadsafe(self._stop(), self.loop)