import socket
import lia_server
import asyncio
from cfg_lia import Configuration
msg_format = 'utf-8'
header = lia_server.header
disconnect_message = lia_server.disconnect_message


async def receive_cfg_and_send_msg(cls, msg: str):
    address = cls.address
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    await send(client, msg)


async def send(client, msg):
    message = msg.encode(msg_format)
    msg_length = len(message)
    send_length = str(msg_length).encode(msg_format)
    send_length += b' ' * (header - len(send_length))
    client.send(message)


def main():
    cfg_cls = Configuration()
    cfg_dict = cfg_cls.get_config()
    server = lia_server.LiaServer(cfg_dict)
    asyncio.run(receive_cfg_and_send_msg(server, "Hello World"))
    asyncio.run(receive_cfg_and_send_msg(server, disconnect_message))
    print("Disconnected")


if __name__ == "__main__":
    main()
