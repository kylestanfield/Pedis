import asyncio
from resp_types import *

HOST = 'localhost'
PORT = 6379

database = {}

def parse(message):
    return Array(message, 0)

def serializeSimple(s):
    respStr = SimpleString(s)
    return respStr.serialize()

def serializeBulk(s):
    respStr = BulkString(s)
    return respStr.serialize()

async def echo(args, writer):
    if len(args) > 0:
        message = args[0]
    else:
        message = BulkString(None)
    writer.write(message.serialize().encode())
    await writer.drain()

async def get(args, writer):
    key = str(args[0])
    response = database.get(key, None)
    writer.write(serializeBulk(response).encode())
    await writer.drain()

async def set(args, writer):
    key = str(args[0])
    val = str(args[1])
    database[key] = val
    success = True

    if success:
        writer.write(serializeSimple('OK').encode())
    else:
        writer.write(serializeBulk(None).encode())
    await writer.drain()
    
async def ping(args, writer):
    if len(args) > 0:
        writer.write(args[0].serialize().encode())
    else:
        writer.write(serializeSimple('PONG').encode())
    await writer.drain()


functions = {'echo':echo,
             'get':get,
             'set':set,
             'ping':ping,}

async def handle_request(reader, writer):
    request = (await reader.read(1024)).decode('utf8')
    command = parse(request)
    procedure = str(command[0])
    args = command[1:]
    await functions[str(procedure).lower()](args, writer)
    

async def run_server():
    server = await asyncio.start_server(handle_request, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(run_server())