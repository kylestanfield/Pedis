import asyncio
from resp_types import *

HOST = 'localhost'
PORT = 6379

database = {}

def parse(message):
    return Array(message, 0)

async def handle_request(reader, writer):
    request = (await reader.read(1024)).decode('utf8')
    command = parse(request)
    procedure = command[0]
    args = command[1:]
    match procedure.getString():
        case 'PING':
            s = SimpleString('PONG')
            writer.write(s.serialize().encode())
            await writer.drain()

        case 'ECHO':
            writer.write(args[0].serialize().encode())
            await writer.drain()

        case 'SET':
            key = str(args[0])
            val = args[1]
            database[key] = val
            writer.write(SimpleString('OK').serialize().encode())
            await writer.drain()

        case 'GET':
            key = str(args[0])
            if key in database:
                val = database[key]
                writer.write(val.serialize().encode())
                await writer.drain()
            else:
                val = BulkString()
                writer.write(val.serialize().encode())
                await writer.drain()
    

async def run_server():
    server = await asyncio.start_server(handle_request, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())