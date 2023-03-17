from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path
import random
import time
import requests


def wait_loading(driver):
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )


def wait_sleep(a, b):
    time.sleep(random.randint(a, b))


def create_root_folder(name:str):
    names = name.split('-')
    if len(names) > 1:
        path = Path(f'data/{names[0]}/{names[1]}')
    else:
        path = Path(name)
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
    file = open(path / f"{name.strip()}.pdf", 'wb')
    file.write(response.content)
    file.close()