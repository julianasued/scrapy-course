from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import random
import time
import requests
import json
import os


def load_config():
    f = open('configuracoes.json')
    config = json.load(f)
    f.close()
    return config


def wait_loading(driver:'WebDriver'):
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )


def wait_sleep(a, b):
    time.sleep(random.randint(a, b))


def create_root_folder(root:str, name:str):
    path = Path(f'{root}{os.sep}{name}')
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_folder(path:'Path', name:str):
    path = path / name.strip()
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_file(driver:'WebDriver', url:str, path:'Path', name:str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    s = requests.session()
    s.headers.update(headers)
    s.cookies.update( {c['name']:c['value'] for c in driver.get_cookies()} )
    response = s.get(url)
    name = name.replace('/', '-')
    file = open(path / f"{name.strip()}.pdf", 'wb')
    file.write(response.content)
    file.close()


def download_video(url, name, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    s = requests.session()
    s.headers.update(headers)
    response = s.get(url)
    name = name.replace('/', '-')
    file = open(path / f"{name.strip()}.mp4", 'wb')
    file.write(response.content)
    file.close()

    