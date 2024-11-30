from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

LOOP_FLAG = True

class OSCServer:

    def __init__(self, ip="127.0.0.1", port=8000):
        self.loop_flag = True
        self.ip = ip
        self.port = port
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/test", self.test_handler)

    def test_handler(self, address, *args):
        print(f"{address}: {args}")
        self.loop_flag = False

    async def loop(self):
        while self.loop_flag:
            await asyncio.sleep(1)

    async def init_main(self):
        server = AsyncIOOSCUDPServer((self.ip, self.port), self.dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
        await self.loop()  # Enter main loop of program
        transport.close()  # Clean up serve endpoint

    def run(self):
        asyncio.run(self.init_main())

if __name__=="__main__":
    server = OSCServer()
    server.run()