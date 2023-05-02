import os
from dotenv import load_dotenv
from mta_manager import MTA
import threading
import time
from time import sleep
from pprint import pprint

load_dotenv()

api_key = os.getenv('MTA_API_KEY', '')
mtaController = MTA(
    api_key,
    ["A", "C", "E", "1", "2", "3"],
    ["127S", "127N", "A27N", "A27S"]
)

async def mta_callback(trains):
    print("We are inside of the call back now")
    print(len(trains))
    pprint([str(route) for route in trains])
    pprint(mtaController.get_time_arriving_at_stations(trains))

class threadWrapper(threading.Thread):
    def __init__(self, run):
        threading.Thread.__init__(self)
        self.run = run

    def run(self):
        self.run()

def start_mta():
    mtaController.add_callback(mta_callback)
    mtaController.start_updates()

def stop_mta():
    sleep(10)
    mtaController.stop_updates()

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = threadWrapper(start_mta)
thread2 = threadWrapper(stop_mta)


thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")
