import json
import os
import sys
import random
import win32api
import win32con
import webbrowser
import logging
from threading import Thread
from datetime import datetime

WAIT_TIME_MINS = 15
SLEEP_TIME = 60

def check_dir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_json(json_file) -> dict:
    try:
        with open(json_file) as of:
            data = json.load(of)
    except:
        data = {}
    return data

def save_json(json_file: str, data: dict):
    path = "/".join(json_file.split("/")[:-1])
    if path != "":
        check_dir(path)

    with open(json_file, "w") as f:
        f.write(json.dumps(data, indent=4))

def get_sleep_time() -> int:
    return SLEEP_TIME + random.randint(0, 10)

def get_wait_time() -> int:
    return WAIT_TIME_MINS * 60

def pc_alert(title: str, msg: str, link: str=""):  # pragma: no cover
    def walert():
        if link == "":
            win32api.MessageBox(0, msg, title, 0x00001000)
        else:
            answer = win32api.MessageBox(0, msg + "\nOpen on cardmarket?", title, win32con.MB_YESNO | 0x00001000)
            if answer == win32con.IDYES:
                webbrowser.open(link, new=2)
    
    worker = Thread(target=walert)
    worker.daemon = True
    worker.start()

def create_logger(name, filename="log.txt"):
    formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    path = "/".join(filename.split("/")[:-1])
    if path != "":
        check_dir(path)
    handler = logging.FileHandler(filename, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

def pretty_price(price):
    str_price = str(price)
    leading = "" if price >= 10 else "0"
    if "." not in str_price:
        following = ".00"
    else:
        following = "" if len(str_price.split(".")[1]) >= 2 else "0"
        str_price = str_price[:str_price.index(".") + 3]
    return f"{leading}{str_price}{following}"

def get_formatted_time():
    return ":".join(str(datetime.now()).split(":")[:2])