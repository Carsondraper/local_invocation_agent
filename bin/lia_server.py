import logging
import socket
import threading
header = 1024
msg_format = 'utf-8'
disconnect_message = "BYE"
server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(conn, addr):
    """ The Function that handles all the connections """
    logging.info(f'[New Connection] {addr} connected')

    connected = True
    while connected:
        msg_length = conn.recv(header).decode(msg_format)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(msg_format)
            if msg == disconnect_message:
                logging.info(f'{disconnect_message} was received.')
                logging.info(f'[Disconnecting Connection]')
                connected = False
            logging.info(f'[{addr}] {msg}')
            conn.send("Message Received".encode(msg_format))
            logging.info(f'Message Received...')
    conn.close()
    logging.info(f'[Active Connections] {threading.activeCount() - 1}')


class Serv:
    def __init__(self, cfg_dict):
        self.server = cfg_dict["local_host_addr"]
        self.port = cfg_dict["local_host_port"]
        self.address = (self.server, self.port)
        server_instance.bind(self.address)

    async def start_server(self):
        """
        Function used to start the socket server
        """
        logging.info(f'Starting server on {self.server}:{self.port}')
        server_instance.listen()
        # Looping
        while True:
            conn, addr = server_instance.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            logging.info(f'[Active Connections] {threading.activeCount() - 1}')
