import logging
from os import path
from cfg_lia import Configuration, default_log_dir, default_log_name
import api_util
import lia_server
import asyncio
import client_test

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        filename=f'{path.abspath(default_log_dir)}\\{default_log_name}',
                        filemode='w')
    cfg_cls = Configuration()
    cfg_dict = cfg_cls.get_config()
    server = lia_server.Serv(cfg_dict)
    asyncio.run(server.start_server())
    asyncio.run(client_test.receive_cfg_and_send_msg(server))






