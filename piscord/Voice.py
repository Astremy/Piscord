import socket
import subprocess
from random import randint

from .Gateway import *


class Voice:

    def __init__(self, voice, bot):
        self.guild_id = voice["guild_id"]
        self.channel_id = voice["channel_id"]
        self.mute = voice.get("mute", None)
        self.deaf = voice.get("deaf", None)
        self.state = 0
        self.gateway = None
        self.client = VoiceClient(self.guild_id, bot.user.id)
        self.__bot = bot


async def run(self):
    self.loop = asyncio.get_event_loop()
    response = await self.__bot.api_call("/gateway")
    gateway = Gateway(f"{response['url']}?v=7&encoding=json", self.__bot.token)
    self.gateway = gateway
    async for data in gateway.connect():
        if data["op"] == 0:
            if data["t"] == "READY":
                await gateway.send({
                    "op": 4,
                    "d": {
                        "guild_id": self.guild_id,
                        "channel_id": self.channel_id,
                        "mute": self.mute,
                        "deaf": self.deaf
                    }})

            if data["t"] == "VOICE_SERVER_UPDATE":
                if data["d"]["guild_id"] == self.guild_id:
                    self.client.token = data["d"]["token"]
                    self.client.endpoint = data["d"]["endpoint"][:-3]
            elif data["t"] == "VOICE_STATE_UPDATE":
                if data["d"]["user_id"] == self.__bot.user.id and data["d"]["guild_id"] == self.guild_id:
                    self.client.session_id = data["d"]["session_id"]
            if self.client.session_id and self.client.token and not self.state:
                self.state = 1
                asyncio.create_task(self.client.run())


def stop(self):
    if self.client.gateway:
        self.client.stop()
    if self.gateway:
        self.gateway.stop()


def play(self, name):
    print("bip1")
    payload = {
        "op": 5,
        "d": {
            "speaking": 1,
            "delay": 0,
            "ssrc": 1
        }}
    asyncio.run(self.client.gateway.send(payload))
    ip = socket.gethostbyname(self.client.endpoint)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sending = AudioStream()
    print("bip2")
    self.socket.sendto(sending.encode_packet(name), (ip, self.client.port))
    print("bip3")


class VoiceClient:

    def __init__(self, guild_id, user_id):
        self.guild_id = guild_id
        self.user_id = user_id
        self.session_id = None
        self.token = None
        self.endpoint = None
        self.gateway = None
        self.secret_key = None
        self.mode = None
        self.ip = None
        self.port = None

    async def run(self):
        gateway = Gateway(f"wss://{self.endpoint}/?v=4", "", auth_op=8, events_code=-1, heartbeat_code=3)
        self.gateway = gateway
        payload = {
            "op": 0,
            "d": {
                "server_id": self.guild_id,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "token": self.token
            }}
        async for data in gateway.connect(payload):

            if data["op"] == 2:
                self.ip = data["d"]["ip"]
                self.port = data["d"]["port"]
                payload = {
                    "op": 1,
                    "d": {
                        "protocol": "udp",
                        "data": {
                            "address": self.ip,
                            "port": self.port,
                            "mode": "xsalsa20_poly1305_lite"
                        }}}
                await gateway.send(payload)

            if data["op"] == 4:
                self.mode = data["d"]["mode"]
                self.secret_key = data["d"]["secret_key"]

    def stop(self):
        self.gateway.stop()


class AudioStream:
    """
    To understand how this class works and why, please refer to the following documents:
    - https://discord.com/developers/docs/topics/voice-connections
    - https://www.rfcreader.com/#rfc3550_line548
    and more specifically to this section of discord's documentation:
    - https://discord.com/developers/docs/topics/voice-connections#encrypting-and-sending-voice-voice-packet-structure
    """

    def __init__(self):
        self.sequence = randint(0, 65_535)
        self.ssrc = randint(0, 65_535)
        self.timestamp = 0

    def encode_packet(self, audio):
        packet = bytearray()
        packet.append(0x80)
        packet.append(0x78)
        self.packet_add(packet, self.sequence, 2)
        self.packet_add(packet, self.timestamp, 4)
        self.packet_add(packet, self.ssrc, 4)

        return bytes(packet) + b"r" * 1000  # self.encode_voice_data(audio)[:5000]

    def packet_add(self, packet, value, bytes):
        for i in range(bytes, 0, -1):
            x = 256 ** (i - 1)
            v = value // x
            if v > 255:
                raise ValueError("Too large number")
            value = value % x
            packet.append(v)

    def encode_voice_data(self, audio: str):
        """
        Todo: implement Opus audio encryption and increment timestamp accordingly 
        """
        try:
            output = subprocess.Popen(f"ffmpeg -i {audio} -f s16le -ar 48000 -ac 2 -loglevel warning pipe:1",
                                      stdout=subprocess.PIPE).stdout
        except FileNotFoundError as e:
            raise ProcessLookupError("You should install ffmpeg to use voices")
        return output.read()
