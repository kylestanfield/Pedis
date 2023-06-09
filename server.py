import asyncio
from resp_types import *

HOST = 'localhost'
PORT = 6379

def parse(message):
    print('now parsing!')
    return Array(message, 0)

async def handle_request(reader, writer):
    request = (await reader.read(1024)).decode('utf8')
    print(request)
    command = parse(request)
    print('done parsing!')
    print(command)
    

async def run_server():
    server = await asyncio.start_server(handle_request, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())