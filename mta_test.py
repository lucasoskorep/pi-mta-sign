import os
from dotenv import load_dotenv
from mta import MTA

load_dotenv()


async def mta_callback(data):
    print("We are inside of hte call back now boizzzz")
    print(data)


api_key = os.getenv('MTA_API_KEY', '')
mtaController = MTA(api_key)
mtaController.add_callback(mta_callback)

mtaController.start_updates()
