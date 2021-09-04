import websockets
import json
import asyncio

from .Errors import TokenError, ConnexionError


class Gateway:

    def __init__(self, url, token, auth_op=10, events_code=0, heartbeat_code=1, presence=None):
        self.url = url
        self.token = token
        self.auth_op = auth_op
        self.last_sequence = 0
        self.events_code = events_code
        self.heartbeat_code = heartbeat_code
        self.session_id = None
        self.presence = presence
        self.error = None
        self.loop = None
        self.interval = None
        self.heartbeat = None
        self.ws = None

    async def connect(self, action=None, shards=None):
        if shards is None:
            shards = [0, 1]
        self.loop = asyncio.get_event_loop()
        ws = await websockets.connect(self.url, ping_interval=None, max_size=1_000_000_000)
        self.ws = ws
        while True:
            if self.error:
                raise self.error
            try:
                msg = await self.ws.recv()
            except Exception as e:
                if e.code in [1000, 1001, 1006]:
                    await self.ws.close()
                    if self.session_id and self.last_sequence:
                        await self.ws.close()
                        for i in range(5):
                            ws, msg = await self._reconnect()
                            if msg:
                                data = json.loads(msg)
                                self.ws = ws
                                self.interval = data["d"]["heartbeat_interval"]
                                break
                            else:
                                await asyncio.sleep(1)
                        else:
                            self.error = ConnexionError("You've lost the connection to the server")
                            self.heartbeat.cancel()
                        continue
                    else:
                        self.heartbeat.cancel()
                        return
                elif e.code == 4004:
                    self.error = TokenError()
                else:
                    self.error = ConnexionError(f"Unknown Error - {e.code}")
                self.heartbeat.cancel()
                continue

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
                            "$browser": "piscord",
                            "$device": "piscord"
                        },
                        "large_threshold": 250,
                        "presence": self.presence,
                    }}
                if shards[1] > 1:
                    payload["shard"] = shards

                if action:
                    await self.send(action)
                else:
                    await self.send(payload)
            if data["op"] == self.events_code:
                if data["t"] == "READY":
                    self.session_id = data["d"]["session_id"]
            yield data

    async def _reconnect(self):
        payload = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.last_sequence
            }}
        ws = await websockets.connect(self.url, ping_interval=None)
        msg = None
        try:
            await ws.recv()
            await self.send(payload)
            msg = await ws.recv()
        except Exception as e:
            # TODO: must do something with the "e" or put a more precise Exception
            await ws.close()
        return ws, msg

    async def __heartbeat(self, ws):
        while True:
            await asyncio.sleep(self.interval / 1000)
            if not self.ws.closed:
                await self.send({"op": self.heartbeat_code, "d": self.last_sequence})

    async def send(self, payload):
        await self.ws.send(json.dumps(payload))

    async def _stop(self):
        self.session_id = None
        await self.ws.close()
        self.heartbeat.cancel()

    def stop(self):
        asyncio.run_coroutine_threadsafe(self._stop(), self.loop)
