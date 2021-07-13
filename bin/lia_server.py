import logging
import asyncio

header = 1024
msg_format = 'utf-8'
disconnect_message = "BYE"


async def handle_client(reader, writer):
    request = None
    while request != disconnect_message:
        request = (await reader.read()).decode(msg_format)
        logging.info(f'[Message Received] {request}')
        response = str(request)
        writer.write(response.encode(msg_format))
        await writer.drain()
    writer.close()


class LiaServer:
    def __init__(self, cfg_dict):
        self.server = cfg_dict["local_host_addr"]
        self.port = cfg_dict["local_host_port"]
        self.address = (self.server, self.port)
        logging.info(f'LiaServer Class object has been created with values of {self.server}:{self.port}')

    async def run_server(self):
        logging.info(f'[Server Start] Attempting to start the server now')
        self.server_instance = await asyncio.start_server(handle_client, self.server, self.port)
        async with self.server_instance:
            logging.info(f'[Server Start] Server is now LISTENING on {self.server}:{self.port}')
            await self.server_instance.serve_forever()

    def stop_server(self):
        logging.info(f'[Server Stop] Attempting to stop the server now')
        pass


if __name__ == "__main__":
    print(f'Lia_server.py is not supposed to be started as __main__. '
          f'Please refer to the docs for more information')
    exit(1)
