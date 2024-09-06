import os
import random
from utils.ton_station import TonStation
from utils.core import logger
import datetime
import pandas as pd
from utils.core.telegram import Accounts
from aiohttp.client_exceptions import ContentTypeError
import asyncio
from data import config


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    tons = TonStation(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    await tons.login()

    # for task in await tons.get_tasks():
    #     if not task['active']: continue

    #     await tons.task_start(task['project'], task['id'])
    #     await asyncio.sleep(*config.DELAYS['TASK'])

    while True:
        try:
            farming = await tons.farming_running()
            if farming is False:
                if await tons.farming_start():
                    logger.success(f"Chủ đề {thread} | {account} | Bắt đầu farming")
                else:
                    logger.warning(f"Chủ đề {thread} | {account} | Không thể bắt đầu farming")

            if farming is not False and tons.iso_to_unix_time(farming['timeEnd']) > tons.current_time():
                sleep = tons.iso_to_unix_time(farming['timeEnd']) - tons.current_time() + random.uniform(*config.DELAYS['CLAIM'])
                logger.info(f"Chủ đề {thread} | {account} | Ngủ {round(sleep, 1)} Giây")
                await asyncio.sleep(sleep)

            if farming is not False and tons.iso_to_unix_time(farming['timeEnd']) < tons.current_time():
                await tons.login()
                farming = await tons.farming_claim(farming["_id"])
                if farming:
                    logger.success(f"Chủ đề {thread} | {account} | Claim farming! Balance: {farming.get('amount')}")
                else:
                    logger.warning(f"Chủ đề {thread} | {account} | không thể claim farming")

            await asyncio.sleep(random.uniform(*config.DELAYS['REPEAT']))

        except Exception as e:
            logger.error(f"Chủ đề {thread} | {account} | Error: {e}")
            await asyncio.sleep(1)

    await tons.logout()


async def stats():
    accounts = await Accounts().get_accounts()

    tasks = []
    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(TonStation(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy).stats()))

    data = await asyncio.gather(*tasks)

    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Phone number', 'Name', 'Balance', 'Referrals', 'Proxy (login:password@ip:port)']

    if not os.path.exists('statistics'): os.mkdir('statistics')
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')

    logger.success(f"Thống kê đã lưu vào {path}")
