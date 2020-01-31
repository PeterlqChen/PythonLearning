
import sys
import requests
import time

import concurrent.futures
import threading # pre-emptive multitasking
import asyncio # cooperative multitasking
import aiohttp # aio version of http requests
import multiprocessing #

# =============================================================================
# https://realpython.com/python-concurrency/
# =============================================================================

# downloading web pages, Synchronous Version

def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)

sites = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80
start_time = time.time()
download_all_sites(sites)
duration = time.time() - start_time
print(f"Downloaded {len(sites)} in {duration} seconds")

# downloading web pages, threading Version

# creates an object that is specific to each individual thread
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        # any data that is shared between the threads needs to be protected, 
        # or thread-safe. requests.Session() is not thread-safe,
        # so we need one session for each thread.
        # each thread creates a single session the first time it gets called
        thread_local.session = requests.Session() 
    return thread_local.session

def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    # high level controller, takes care of lower level start, join, lock, etc.
    # Some experimentation is required to get the optimal number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_site, sites)

sites = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80
start_time = time.time()
download_all_sites(sites)
duration = time.time() - start_time
print(f"Downloaded {len(sites)} in {duration} seconds")

# race conditions example

counter = 0 # shared across threads, not protected

def increment_counter(fake_value):
    global counter
    for _ in range(100):
        counter += 1

fake_data = [x for x in range(5000)]
with concurrent.futures.ThreadPoolExecutor(max_workers=5000) as executor:
    executor.map(increment_counter, fake_data)
counter # can be less than 5000*100 but with low probability, hard to reproduce

# downloading web pages, asyncio Version
# Use asyncio when you can, threading when you must.

async def download_site(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))

async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            # takes far fewer resources and less time to create tasks than a thread
            # creates a separate task for each site to download
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        # keep the session context alive until all of the tasks have complete
        await asyncio.gather(*tasks, return_exceptions=True)

sites = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80
start_time = time.time()
asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
duration = time.time() - start_time
print(f"Downloaded {len(sites)} sites in {duration} seconds")

# downloading web pages, multiprocessing Version
# I/O-bound problems are not really why multiprocessing exists

session = None

def set_global_session():
    global session
    if not session:
        session = requests.Session()

def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)

sites = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80
start_time = time.time()
download_all_sites(sites)
duration = time.time() - start_time
print(f"Downloaded {len(sites)} in {duration} seconds")

# CPU-Bound, Synchronous Version

def cpu_bound(number):
    return sum(i * i for i in range(number))

def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)

numbers = [5_000_000 + x for x in range(20)]

start_time = time.time()
find_sums(numbers)
duration = time.time() - start_time
print(f"Duration {duration} seconds")

# CPU-Bound, multiprocessing Version

def cpu_bound(number):
    return sum(i * i for i in range(number))

def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)

numbers = [5_000_000 + x for x in range(20)]

start_time = time.time()
find_sums(numbers)
duration = time.time() - start_time
print(f"Duration {duration} seconds")










































    

