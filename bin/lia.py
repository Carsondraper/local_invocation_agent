import logging
from os import path
from cfg_lia import Configuration, default_log_dir, default_log_name
import lia_server
import asyncio


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        filename=f'{path.abspath(default_log_dir)}\\{default_log_name}',
                        filemode='w')
    cfg_cls = Configuration()
    cfg_dict = cfg_cls.get_config()
    server_obj = lia_server.LiaServer(cfg_dict)
    task_server = asyncio.create_task(server_obj.run_server())
    await task_server


if __name__ == '__main__':
    asyncio.run(main())
