from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import random
import time
import requests
import json
import os


def load_config():
    f = open('configuracoes.json', encoding='utf-8')
    config = json.load(f)
    f.close()
    return config

def clean_name(name:str):
    char_remove = ['.', ':', '"', '”', '>', '<', '\\', '?', '|']
    name = name.replace('/', '-')
    for char in char_remove:
        name = name.replace(char, '')
    return name.strip()[:122]


def wait_loading(driver:'WebDriver'):
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )


def wait_sleep(a, b):
    time.sleep(random.randint(a, b))


def click_point(driver:'WebDriver', elem):
    ac = ActionChains(driver)
    ac.move_to_element(elem).move_by_offset(1, 1).click().perform()


def create_root_folder(root:str, name:str):
    path = Path(f'{root}{os.sep}{clean_name(name)}')
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_folder(path:'Path', name:str):
    path = path / clean_name(name)
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
    file = open(path / f"{clean_name(name)[:55]}.pdf", 'wb')
    file.write(response.content)
    file.close()


def download_video(url, name, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    s = requests.session()
    s.headers.update(headers)
    response = s.get(url)
    file = open(path / f"{clean_name(name)[:55]}.mp4", 'wb')
    file.write(response.content)
    file.close()


def check_already_file(path, name, type_):
    path = path / f"{clean_name(name)[:55]}.{type_}"
    return os.path.isfile(path)