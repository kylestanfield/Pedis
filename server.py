import asyncio
from resp_types import *

HOST = 'localhost'
PORT = 6379

def deserialize(message):
    data_type = message[0]
    match data_type:
        case '+':
            return SimpleString(message)
        case '-':
            return Error(message)
        case ':':
            return Integer(message)
        case '$':
            return BulkString(message)
        case '*':
            return Array(message)
        case _:
            raise ValueError(f'Could not parse {message}')


async def handle_request(reader, writer):
    request = (await reader.read(1024)).decode('utf8')
    print(request.split('\r\n'))
    

async def run_server():
    server = await asyncio.start_server(handle_request, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())